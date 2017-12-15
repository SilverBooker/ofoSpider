#### 接口现在返回的单车id都是6666...
#### 360验证码平台被封，注册机暂时也不能用了。

ofo共享单车地图爬虫
====================

```
感谢您的支持
朋友要做城市数据的一些研究，拜托我写ofo地图的小爬虫
最初的看到了derekhe大神写的单车地图，觉得非常的优秀。
但是单车地图由于官方不断封杀爬虫的行为，被迫关闭了。
derekhe写的爬虫也没办法使用了，于是参考了derekhe的代码。
对现在ofo的api进行了分析，甚至还写了个ofo的token注册机，
实现了对ofo附近单车位置的爬取。

如果这个程序帮助到了你，请动动手指，给个Star！
```

该爬虫为ofo附近单车爬虫
* 新增ofo注册机
* 目前只支持ofo
* 多线程爬取
* 自动去重
* 输出csv文件，存放在db/【日期】/【日期】-【时间】-【品牌】.csv文件内
* gzip压缩存储

# 运行环境
* Python3
* Linux/Mac/Windows

请根据你的需要修改配置文件config.ini，请查看内置说明。

## Linux/Mac
* 下载[最新代码](https://github.com/SilverBooker/ofoSpider/archive/master.zip)并解压
* 修改config.ini确保坐标和区域等参数正确
* 运行：
```
pip3 install -r requirements.txt
python3 run.py
```

## Windows
* 下载[最新代码](https://github.com/SilverBooker/ofoSpider/archive/master.zip)并解压
* 安装好python3.5.3
* 在cmd中执行pip install -r requirements.txt
* 修改config.ini确保坐标和区域等参数正确
* 在cmd执行python run.py

# 输出格式

输出格式：CSV

每行格式：时间戳，单车编号，纬度，经度

# 关于token
```
很多人来问我token的取法，问得人多了，我就认识到了写好文档的重要性
token是发出获取附近单车请求的必要字段，保存在ofo账号登录后cookie，
具体获取方法如下所示
```
* 使用chrome浏览器访问https://common.ofo.so/newdist/?Login&~next=%22%3FJourney%22
* 输入你的账号验证码成功登陆后（强烈建议使用没有押金的小号，被封后果自负）
* 点击地址栏左边“安全”查看当前网站cookie信息
* 然后我们就可以在ofo.so域下发现我们当前账号的token

![图1](/image/1.png)
![图2](/image/2.png)

# 关于批量获取token——ofo注册机
```
这个注册机写的不是很好，毕竟用到了个人不喜欢的selenium，
打码，接码，记录token能够全部自动化，
日后可能会再修改。
```
* 确保你安装了chrome浏览器，之后打开设置->关于chrome查看chrome的版本
* 访问http://blog.csdn.net/huilan_same/article/details/51896672 查看版本对应的chromedriver
* 访问http://chromedriver.storage.googleapis.com/index.html 下载对应的chromedriver
* 修改ofoRegister/login.py下start()函数中chromedriver你所放置的路径
* 访问http://www.360yzm.com/ 360验证码平台注册账号，进行充值（1个账号1毛钱），并在login.py对应的位置填入你的账号密码
* 访问http://www.ruokuai.com/ 若快打码平台注册账号，进行充值（识别一条验证码好像是一分钱），并在login.py对应的位置填入账号密码
* 按需修改ofoRegister/login.py下start()函数中for循环的次数，每次循环生成一个账号
* 最后，在ofoRegister目录下执行python login.py(提示缺少哪个包就用pip安装哪个包)
* 最后就会在ofoRegister目录下生成一个写有token的txt文件
