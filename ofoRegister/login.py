import re
import time
import base64
import sys
import threading
import Api_360Yzm
from rk import *
# from multiprocessing import Pool
from selenium import webdriver
from selenium.webdriver import ActionChains



class Register:
    def __init__(self):
        self.rc = RClient('若快账号', '若快密码', '94468', '0a5cda058154411280029dc311a84011')
        options = webdriver.ChromeOptions()
        options.add_argument('--ignore-certificate-errors')
        options.add_argument('--ignore-ssl-errors')
        self.msg = ''
        while (True):
            retVal = Api_360Yzm.loginIn('360验证码账号', '360验证码密码', '24607')
            print(retVal)
            retValArr = retVal.decode("ascii").split("|")
            if (len(retValArr) == 3):
                self.dama_360token = retValArr[1]
                dama_money = retValArr[2]
                print("360Yzm login ok,token:" + self.dama_360token)
                print("money:" + dama_money)
                break
            else:
                print(retVal)
                print("360Yzm login error")
                # 重新拨号
                time.sleep(10)
                continue

    def get_phone(self):
        phone = Api_360Yzm.getPhone(self.dama_360token, "10597")
        phone = bytes.decode(phone)
        i = 0
        while i<3:
            if phone != '':
                phone = phone[2:]
                print("get phone ok:%s"%phone)
                self.phone = phone
                return phone
                break
            else:
                phone = Api_360Yzm.getPhone(self.dama_360token, "10597")
                i=i+1
        if i == 3:
            print("请检查360验证码余额")
            sys.exit(0)


    def get_message(self):
        i = 1
        msg = ""
        while (True):
            msg = Api_360Yzm.getMessage(self.dama_360token, "10597", self.phone)
            if (int(msg[0:1]) == 1):
                msg = re.search("\d{4}",str(msg)).group()
                self.msg = msg
                return msg
                break
            else:
                i = i + 1
                time.sleep(6)
                print("还没收到短信验证码，骚等一会")
                if i > 10:
                    print("等了一分钟还没收到短信验证码，不等了，拉黑")
                    Api_360Yzm.addBlack(self.dama_360token, "10597", self.phone)
                    return 0
        # 判断有没有收到短信验证码
        if (msg == ""):
            print("进入一个循环")
        # 收到了短信，进行下一步操作
        print("this is ok,next")

    def get_captcha(self):
        page = self.browser.page_source
        captcha = re.search(r"data:image/jpeg;base64,([a-z,A-Z,0-9,/,+]*[=]{0,})",page).group(1)
        # print(page)
        captcha = base64.b64decode(captcha.encode("utf-8"))
        with open("captcha.jpg","wb") as pic:
            pic.write(captcha)

    def input_number(self,number):
        phone = str(number)
        for i in phone:
            if(i == '1'):
                print(i,end='')
                ac = self.browser.find_element_by_xpath("//*[@id='app']/div/div[1]/div[2]/table/tbody/tr[1]/td[1]/div/canvas")
                ActionChains(self.browser).move_to_element(ac).click(ac).perform()
            elif(i == '2'):
                print(i,end='')
                ac = self.browser.find_element_by_xpath("//*[@id='app']/div/div[1]/div[2]/table/tbody/tr[1]/td[2]/div/canvas")
                ActionChains(self.browser).move_to_element(ac).click(ac).perform()
            elif(i == '3'):
                print(i,end='')
                ac = self.browser.find_element_by_xpath("//*[@id='app']/div/div[1]/div[2]/table/tbody/tr[1]/td[3]/div/canvas")
                ActionChains(self.browser).move_to_element(ac).click(ac).perform()
            elif(i == '4'):
                print(i,end='')
                ac = self.browser.find_element_by_xpath("//*[@id='app']/div/div[1]/div[2]/table/tbody/tr[2]/td[1]/div/canvas")
                ActionChains(self.browser).move_to_element(ac).click(ac).perform()
            elif(i == '5'):
                print(i,end='')
                ac = self.browser.find_element_by_xpath("//*[@id='app']/div/div[1]/div[2]/table/tbody/tr[2]/td[2]/div/canvas")
                ActionChains(self.browser).move_to_element(ac).click(ac).perform()
            elif(i == '6'):
                print(i,end='')
                ac = self.browser.find_element_by_xpath("//*[@id='app']/div/div[1]/div[2]/table/tbody/tr[2]/td[3]/div/canvas")
                ActionChains(self.browser).move_to_element(ac).click(ac).perform()
            elif(i == '7'):
                print(i,end='')
                ac = self.browser.find_element_by_xpath("//*[@id='app']/div/div[1]/div[2]/table/tbody/tr[3]/td[1]/div/canvas")
                ActionChains(self.browser).move_to_element(ac).click(ac).perform()
            elif(i == '8'):
                print(i,end='')
                ac = self.browser.find_element_by_xpath("//*[@id='app']/div/div[1]/div[2]/table/tbody/tr[3]/td[2]/div/canvas")
                ActionChains(self.browser).move_to_element(ac).click(ac).perform()
            elif(i == '9'):
                print(i,end='')
                ac = self.browser.find_element_by_xpath("//*[@id='app']/div/div[1]/div[2]/table/tbody/tr[3]/td[3]/div/canvas")
                ActionChains(self.browser).move_to_element(ac).click(ac).perform()
            elif(i == '0'):
                print(i,end='')
                ac = self.browser.find_element_by_xpath("//*[@id='app']/div/div[1]/div[2]/table/tbody/tr[4]/td[2]/div/canvas")
                ActionChains(self.browser).move_to_element(ac).click(ac).perform()

    def start(self):
        for i in range(5):
            self.browser = webdriver.Chrome(executable_path="D:/chromedriver/chromedriver.exe")
            self.browser.get("https://common.ofo.so/newdist/?Profile")
            time.sleep(3)
            self.input_number(self.get_phone())
            t = threading.Thread(target=self.get_message)
            t.start()
            while True:
                self.get_captcha()
                im = open('captcha.jpg', 'rb').read()
                captcha = self.rc.rk_create(im, 1040)['Result']
                print("验证码为{}".format(captcha))
                print()
                self.input_number(captcha)
                print()
                time.sleep(1)
                if "数字输入错误"  in self.browser.page_source:
                    print("验证码识别失败，开始重试")
                else:
                    break

            t.join()
            if self.msg:
                self.input_number(self.msg)
                ac = self.browser.find_element_by_xpath(
                    "//*[@id='app']/div/div[1]/div[1]/div[2]/div[4]/button")
                ActionChains(self.browser).move_to_element(ac).click(ac).perform()
                time.sleep(1)
                self.browser.get("https://common.ofo.so/newdist/?Profile")
                time.sleep(3)
                print(self.browser.get_cookies())
                for cookie in self.browser.get_cookies():
                    if cookie['name'] == 'ofo-tokened' and cookie['value']:
                        with open("token.txt", "a") as f:
                            f.write(cookie['value'])
                            f.write(",")
                            f.write("\n")
                self.browser.delete_all_cookies()
                self.browser.quit()
            else:
                print("获取手机验证码失败，开始下一个账号")
                self.browser.quit()

if __name__ == '__main__':
    l = Register()
    l.start()
