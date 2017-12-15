import urllib
import urllib.parse
import urllib.request
import time
import http.client


# GET
def http_get(url,debug=False):
    headers = {'Content-type': 'application/x-www-form-urlencoded', 'Accept': 'text/plain',
               'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64; Trident/7.0; rv:11.0) like Gecko' ,
               }
    urlparsestr = urllib.parse.urlparse(url)
    conn = http.client.HTTPConnection(urlparsestr.netloc)
    if debug == True:
        conn.set_debuglevel(1)
    conn.request("GET", urlparsestr.path + "?" +urlparsestr.query, "", headers)
    reasult = conn.getresponse()
    data = reasult.read()
    return {"status":reasult.status,"data":data,"cookie":reasult.getheader("Set-Cookie") }

#登录
#一个dama_360token可以取多个号
#作者们在使用多线程的时候，无需要重复调试登录接口
#正常返回        1|dama_360token|余额
#错误返回        0|错误原因
def loginIn(dama_360Uname,dama_360Pwd,author_uid):
    url = "http://api.360yzm.com/user.do!loginIn?uname=" + dama_360Uname  + "&pwd=" + dama_360Pwd + "&author_uid=" + author_uid
    html = ""
    try:
        html = http_get(url)["data"]
    except Exception as e:
        time.sleep(1)
        html = http_get(url)["data"]
    return html

#取手机号码
#手机号码|dama_360token
#成功返回: 1|手机号码
#失败返回: 0|失败原因
def getPhone(dama_360token,dama_360Pid):
    url = "http://api.360yzm.com/user.do!getPhone?pid="+ dama_360Pid + "&token=" + dama_360token
    html = ""
    i = 0
    while i<=5:
        try:
            i = i+1
            html = http_get(url)["data"]
            break
        except Exception as e:
            if i> 6:
                break
            continue
    return html


#取手机号码[多参数]
#phoneType 取值为1,2,3  {1代表[移动] 2代表[联通] 3代表[电信]}
#wantCount  想要取多少个号码   多个用分号分隔 
#area 号码是哪个城市的，直接传想要的城市名字
#channelKey  和卡商对接的密钥      格式：项目ID-随机数
#成功返回: 1|手机号码
#失败返回: 0|失败原因
def getPhones(dama_360token,dama_360Pid,wantCount,wantPhone,area,phoneType,channelKey):
    url = "http://api.360yzm.com/user.do!getPhone?pid="+ dama_360Pid + "&token=" + dama_360token+"&count="+wantCount+"&phone="+wantPhone+"&area="+area+"&phoneType="+phoneType+"&channelKey="+channelKey
    html = ""
    i = 0
    while i<=5:
        try:
            i = i+1
            html = http_get(url)["data"]
            break
        except Exception as e:
            if i> 6:
                break
            continue
    return html

#取短信
#成功返回: 1|短信内容
#失败返回: 0|暂无
def getMessage(dama_360token,dama_360Pid,phone):
    # url = "http://api.360yzm.com/user.do!getMessage?token="+dama_360token+"&pid="+dama_360Pid+"&phone="+phone
    url = "http://api.360yzm.com/user.do!getMessage?token=%s&pid=%s&phone=%s"%(dama_360token,dama_360Pid,phone)
    html = ""
    i = 0
    while i<=5:
        try:
            i = i+1
            html = http_get(url)["data"]
            break
        except Exception as e:
            if i> 6:
                break
            continue
    return html

#释放手机号码
#只有当做的项目类型是   【发送类型  多条接受】  的时候，用户才需要主动释放！！！！！！！！！！！！！！！！！！！！！！！！！！！！！
#单条接收的项目，无需调用此方法！！！！！！！
#成功返回: 1|成功
#失败返回: 0|失败原因
def releasePhone(dama_360token,dama_360Pid,phone):
    url = "http://api.360yzm.com/user.do!releasePhone?token="+dama_360token+"&pid="+dama_360Pid+"&phone=%s"%phone
    html = ""
    i = 0
    while i<=5:
        try:
            i = i+1
            html = http_get(url)["data"]
            break
        except Exception as e:
            if i> 6:
                break
            continue
    return html

#释放所有号码，很少用到哦
#程序写的混乱的时候可能会用到-_-
#成功返回: 1|成功
#失败返回: 0|失败原因
def releaseAllPhone(dama_360token):
    url = "http://api.360yzm.com/user.do!releaseAllPhone?token="+dama_360token
    html = ""
    i = 0
    while i<=5:
        try:
            i = i+1
            html = http_get(url)["data"]
            break
        except Exception as e:
            if i> 6:
                break
            continue
    return html

#添加到黑名单
#取完手机号，不不不不不不用调用此接口，系统取完会自动帮你加入系统的黑名单
#此接口一般是在你有检测是否注册过的接口时候用到的。
#成功返回: 1|成功
#失败返回: 0|失败原因
def addBlack(dama_360token,dama_360Pid,phone):
    url = "http://api.360yzm.com/user.do!addBlack?token="+dama_360token+"&pid="+dama_360Pid+"&phone=%s"%phone
    html = ""
    i = 0
    while i<=5:
        try:
            i = i+1
            html = http_get(url)["data"]
            break
        except Exception as e:
            if i> 6:
                break
            continue
    return html


#发送短信
#成功返回: 1|成功
#失败返回: 0|失败原因
def sendMessage(dama_360token,dama_360Pid,phone,msgContent):
    url = "http://api.360yzm.com/user.do!sendMessage?token="+dama_360token+"&pid="+dama_360Pid+"&phone="+phone+"&msg="+msgContent
    html = ""
    i = 0
    while i<=5:
        try:
            i = i+1
            html = http_get(url)["data"]
            break
        except Exception as e:
            if i> 6:
                break
            continue
    return html
