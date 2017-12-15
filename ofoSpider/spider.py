import requests
import datetime
import threading
import json
import os
import pandas as pd
import numpy as np
import time
import sqlite3
from configparser import ConfigParser
from requests.packages.urllib3.exceptions import InsecureRequestWarning
from requests_toolbelt.multipart.encoder import MultipartEncoder
from concurrent.futures import ThreadPoolExecutor
requests.packages.urllib3.disable_warnings(InsecureRequestWarning)


class Crawler:
	def __init__(self):
		self.start_time = datetime.datetime.now()
		self.db_name = "file:database?mode=memory&cache=shared"
		self.csv_path = "./db/" + datetime.datetime.now().strftime("%Y%m%d")
		os.makedirs(self.csv_path, exist_ok=True)
		self.csv_name = self.csv_path + "/" + datetime.datetime.now().strftime("%Y%m%d-%H%M%S")
		cfg = ConfigParser()
		cfg.read("config.ini", encoding='utf-8-sig')
		self.config = cfg
		self.lock = threading.Lock()
		self.total = 0
		self.done = 0
		self.bikes_count = 0

	def get_nearby_bikes(self,args):
		try:
			url = "https://san.ofo.so/ofo/Api/nearbyofoCar"

			headers = {
				'Accept': '*/*',
				'Accept-Encoding': 'gzip, deflate',
				'Accept-Language': 'zh-CN',
				'Content-Length': '524',
				'Content-Type': 'multipart/form-data; boundary=----ofo-boundary-MC40MjcxMzUw',
				'Host': 'san.ofo.so',
				'Origin': 'https://common.ofo.so',
				'Referer': 'https://common.ofo.so/newdist/?Journey',
				'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64; rv:50.0) Gecko/20100101 Firefox/50.0'
			}

			self.request(headers,args,url)
		except Exception as ex:
			print(ex)

	def request(self,headers,args,url):
		multipart_encoder = MultipartEncoder(
	fields={
		"token": str(args[2]),
		"source": "0",
		"source-version": "9999",
		# "lat": "39.928845",
		"lat": str(args[0]),
		# "lng":"116.422077"
		"lng":str(args[1])
		#file为路径
		},
		boundary='----ofo-boundary-MC40MjcxMzUw'
	)
		response = requests.request(
				"POST",url,headers=headers,
				timeout = self.config.getint("DEFAULT","timeout"), 
				verify=False,
				data=multipart_encoder
			)

		with self.lock:
			with self.connect_db() as c:
				try:
					decoded = json.loads(response.text)['values']['info']['cars']
					self.done += 1
					for x in decoded:
						self.bikes_count += 1
						c.execute("INSERT OR IGNORE INTO ofo VALUES (%d,'%s',%f,%f)" % (
							int(time.time()) * 1000, x['carno'], x['lat'], x['lng']))

					timespent = datetime.datetime.now() - self.start_time
					percent = self.done / self.total
					total = timespent / percent
					print("位置 %s, 未去重单车数量 %s, 进度 %0.2f%%, 速度 %0.2f个/分钟, 总时间 %s, 剩余时间 %s" % (
						args, self.bikes_count, percent * 100, self.done / timespent.total_seconds() * 60, total, total - timespent))
				except Exception as ex:
					print(ex)

	def connect_db(self):
		return sqlite3.connect(self.db_name, uri=True)

	def start(self):
		while True:
			self.__init__()

			try:
				with self.connect_db() as c:
					c.execute(self.generate_create_table_sql('ofo'))
			except Exception as ex:
				print(ex)
				pass

			executor = ThreadPoolExecutor(max_workers=self.config.getint('DEFAULT','workers'))
			print("Start")

			self.total = 0
			top_lng, top_lat = self.config.get("DEFAULT","top_left").split(",")
			bottom_lng, bottom_lat = self.config.get("DEFAULT", "bottom_right").split(",")
			lat_range = np.arange(float(top_lat), float(bottom_lat), -self.config.getfloat('DEFAULT','offset'))
			for lat in lat_range:
				lng_range = np.arange(float(top_lng), float(bottom_lng), self.config.getfloat('DEFAULT','offset'))
				for lon in lng_range:
					self.total += 1
					executor.submit(self.get_nearby_bikes, (lat, lon,self.config.get('DEFAULT','token')))

			executor.shutdown()
			self.group_data()

			if not self.config.getboolean("DEFAULT", 'always_run'):
				break

			waittime = self.config.getint("DEFAULT", 'wait_time')
			print("等待%s分钟后继续运行" % waittime)
			time.sleep(waittime * 60)

	def generate_create_table_sql(self, brand):
		return '''CREATE TABLE {0}
				(
					"Time" DATETIME,
					"bikeId" VARCHAR(12),
					lat DOUBLE,
					lon DOUBLE,
					CONSTRAINT "{0}_bikeId_lat_lon_pk"
						PRIMARY KEY (bikeId, lat, lon)
				);'''.format(brand)
				
	def group_data(self):
		print("正在导出数据")
		conn = self.connect_db()

		self.export_to_csv(conn, "ofo")

	def export_to_csv(self, conn, brand):
		df = pd.read_sql_query("SELECT * FROM %s" % brand, conn, parse_dates=True)
		print(brand, "去重后数量", len(df))
		df['Time'] = pd.to_datetime(df['Time'], unit='ms').dt.tz_localize('UTC').dt.tz_convert('Asia/Chongqing')
		compress = None
		csv_file = self.csv_name + "-" + brand + ".csv"
		if self.config.getboolean("DEFAULT","compress"):
			compress = 'gzip'
			csv_file = self.csv_name + "-" + brand + ".csv.gz"

		df.to_csv(csv_file, header=False, index=False, compression=compress)

if __name__ == '__main__':
	c = Crawler()
	c.start()
	print("完成")