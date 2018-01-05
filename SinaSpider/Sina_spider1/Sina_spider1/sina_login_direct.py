# 这种登陆方式是参考别的网友的，虽然效率很高，但我觉得普适性不强
import json
import time
import base64
from urllib import request

import rsa
import math
import random
import binascii
import requests
import re
from urllib.parse import quote_plus

from scrapy.selector import Selector
from scrapy.http import Request
# from code_verification import code_verificate

# 构造 Request headers
agent = 'Mozilla/5.0 (Windows NT 6.3; WOW64; rv:41.0) Gecko/20100101 Firefox/41.0'
headers = {
    'User-Agent': agent
}

session = requests.session()

# 访问 初始页面带上 cookie
index_url = "http://weibo.com/login.php"
yundama_username = 'wchaos'
yundama_password = ',.12506wc'
verify_code_path = './pincode.png'


def get_pincode_url(pcid):
    size = 0
    url = "http://login.sina.com.cn/cgi/pin.php"
    pincode_url = '{}?r={}&s={}&p={}'.format(url, math.floor(random.random() * 100000000), size, pcid)
    return pincode_url


def get_img(url):
    resp = requests.get(url, headers=headers, stream=True)
    with open(verify_code_path, 'wb') as f:
        for chunk in resp.iter_content(1000):
            f.write(chunk)


def get_su(username):
    """
    对 email 地址和手机号码 先 javascript 中 encodeURIComponent
    对应 Python 3 中的是 urllib.parse.quote_plus
    然后在 base64 加密后decode
    """
    username_quote = quote_plus(username)
    username_base64 = base64.b64encode(username_quote.encode("utf-8"))
    return username_base64.decode("utf-8")


# 预登陆获得 servertime, nonce, pubkey, rsakv
def get_server_data(su):
    pre_url = "http://login.sina.com.cn/sso/prelogin.php?entry=weibo&callback=sinaSSOController.preloginCallBack&su="
    pre_url = pre_url + su + "&rsakt=mod&checkpin=1&client=ssologin.js(v1.4.18)&_="
    prelogin_url = pre_url + str(int(time.time() * 1000))
    pre_data_res = session.get(prelogin_url, headers=headers)

    sever_data = eval(pre_data_res.content.decode("utf-8").replace("sinaSSOController.preloginCallBack", ''))

    return sever_data


# 这一段用户加密密码，需要参考加密文件
def get_password(password, servertime, nonce, pubkey):
    rsaPublickey = int(pubkey, 16)
    key = rsa.PublicKey(rsaPublickey, 65537)  # 创建公钥,
    message = str(servertime) + '\t' + str(nonce) + '\n' + str(password)  # 拼接明文js加密文件中得到
    message = message.encode("utf-8")
    passwd = rsa.encrypt(message, key)  # 加密
    passwd = binascii.b2a_hex(passwd)  # 将加密信息转换为16进制。
    return passwd


def login(username, password):
    # su 是加密后的用户名
    su = get_su(username)
    sever_data = get_server_data(su)
    servertime = sever_data["servertime"]
    nonce = sever_data['nonce']
    rsakv = sever_data["rsakv"]
    pubkey = sever_data["pubkey"]
    password_secret = get_password(password, servertime, nonce, pubkey)

    postdata = {
        'entry': 'weibo',
        'gateway': '1',
        'from': '',
        'savestate': '7',
        'useticket': '1',
        'pagerefer': "http://login.sina.com.cn/sso/logout.php?entry=miniblog&r=http%3A%2F%2Fweibo.com%2Flogout.php%3Fbackurl",
        'vsnf': '1',
        'su': su,
        'service': 'miniblog',
        'servertime': servertime,
        'nonce': nonce,
        'pwencode': 'rsa2',
        'rsakv': rsakv,
        'sp': password_secret,
        'sr': '1366*768',
        'encoding': 'UTF-8',
        'prelt': '115',
        'url': 'http://weibo.com/ajaxlogin.php?framelogin=1&callback=parent.sinaSSOController.feedBackUrlCallBack',
        'returntype': 'META'
        }

    # need_pin = sever_data['showpin']
    # if need_pin == 1:
    #     # 你也可以改为手动填写验证码
    #     if not yundama_username:
    #         raise Exception('由于本次登录需要验证码，请配置顶部位置云打码的用户名{}和及相关密码'.format(yundama_username))
    #     pcid = sever_data['pcid']
    #     postdata['pcid'] = pcid
    #     img_url = get_pincode_url(pcid)
    #     get_img(img_url)
    #     verify_code = code_verificate(yundama_username, yundama_password, verify_code_path)
    #     postdata['door'] = verify_code
    #登录操作
    login_url = 'http://login.sina.com.cn/sso/login.php?client=ssologin.js(v1.4.18)'
    login_page = session.post(login_url, data=postdata, headers=headers)
    # print(login_page.content.decode("GBK"))

    #访问登录之后重定向的页面
    login_loop = (login_page.content.decode("GBK"))
    # pa = r'location\.replace\([\'"](.*?)[\'"]\)'
    # loop_url = re.findall(pa, login_loop)[0]
    # # print("loop_url====",loop_url)
    # login_index = session.get(loop_url, headers=headers)

    #访问访问登录返回页面中js访问过的三个url，能扩展session访问微博其他平台页面的权限
    pb = r'[\'"]arrURL[\'"]:\[(.*?)\]'
    cross_url_str = re.findall(pb, login_loop)[0]
    # print(cross_url_str)
    get_crossdomainlist(cross_url_str)

    # print(session.cookies.get_dict())
    # print(login_index.content)
    # uuid = login_index.text
    # uuid_pa = r'"uniqueid":"(.*?)"'
    # uuid_res = re.findall(uuid_pa, uuid, re.S)[0]
    # web_weibo_url = "http://weibo.com/%s/profile?topnav=1&wvr=6&is_all=1" % uuid_res
    # weibo_page = session.get(web_weibo_url, headers=headers)
    # print(session.cookies.get_dict())
    # # return json.dumps(session.cookies.get_dict())
    # weibo_pa = r'<title>(.*?)</title>'
    # user_name = re.findall(weibo_pa, weibo_page.content.decode("utf-8", 'ignore'), re.S)[0]
    # print('登陆成功，你的用户名为：'+user_name)
def get_crossdomainlist(domainstr):
    # domainlist = domainstr.split(",")
    # for cross_url in domainlist:
    #     cross_url = cross_url.replace('"','')
    #     cross_url= cross_url.replace("\/","/")
    #     # print(cross_url)
    #     response = session.get(cross_url,headers=headers)
    #     # print(response.content.decode("utf-8"))

    test_login()

def test_login():
    test_url = "https://weibo.cn/5235640836/profile?filter=1&page=1"
    test_url2= "http://weibo.com/5235640836/profile?topnav=1&wvr=6&is_all=1"
    test_url3 = 'https://m.weibo.cn/u/5837697857?uid=5837697857'

    response = session.get(test_url, headers=headers)
    # print(session.headers)
    print(response.content.decode(("GBK")))

    # pa = r'location\.replace\([\'"](.*?)[\'"]\)'
    # redirect_url = re.findall(pa, response.content.decode(("GBK")))[0]
    # print("redirect_url====", redirect_url)
    # true_response = session.get(redirect_url, headers=headers)
    # print(true_response.content.decode("utf-8"))

    # cookieList = []
    # for name, value in session.cookies.get_dict().items():
    #     cookieList.append(str(name)+"="+str(value))
    #
    # cookies = ";".join(cookieList)
    # print(cookies)
    # headers1 = {
    #     'User-Agent': agent,
    #     'Cookie': cookies,
    # }
    # req = request.Request(test_url3,headers = headers1)
    # page = request.urlopen(req).read().decode("utf-8")
    # print(page)





if __name__ == "__main__":
    # username = input('微博用户名：')
    # password = input('微博密码：')
    username = '17084633974'
    password = 'haha123456'
    login(username, password)