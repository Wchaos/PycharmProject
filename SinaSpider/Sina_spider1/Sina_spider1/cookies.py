# encoding=utf-8

import base64
import logging
import time
import json

import requests
from selenium import webdriver
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities
from Sina_spider1.yumdama import identify
from Sina_spider1.wap_login_direct import wap_login
from urllib import request

IDENTIFY = 1  # 验证码输入方式:        1:看截图aa.png，手动输入     2:云打码
COOKIE_GETWAY = 2 # 0 代表从https://login.sina.com.cn/sso/login.php?client=ssologin.js(v1.4.18) 获取cookie   # 1 代表从https://weibo.cn/login/获取Cookie
dcap = dict(DesiredCapabilities.PHANTOMJS)  # PhantomJS需要使用老版手机的user-agent，不然验证码会无法通过
dcap["phantomjs.page.settings.userAgent"] = (
    "Mozilla/5.0 (Linux; U; Android 2.3.6; en-us; Nexus S Build/GRK39F) AppleWebKit/533.1 (KHTML, like Gecko) Version/4.0 Mobile Safari/533.1"
)
logger = logging.getLogger(__name__)
logging.getLogger("selenium").setLevel(logging.WARNING)  # 将selenium的日志级别设成WARNING，太烦人


"""
输入你的微博账号和密码，可去淘宝买。
建议买几十个，微博限制的严，太频繁了会出现302转移。
或者你也可以把时间间隔调大点。
"""
myWeiBo = [
    {'no': '17084633974', 'psw': 'haha123456'},
]

def getCookie(account, password):
    if COOKIE_GETWAY == 0:
        return get_cookie_from_login_sina_com_cn(account, password)
    elif COOKIE_GETWAY ==1:
        return get_cookie_from_weibo_cn(account, password)
    elif COOKIE_GETWAY ==2:
        return wap_login(account, password)
    else:
        logger.error("COOKIE_GETWAY Error!")

def get_cookie_from_login_sina_com_cn(account, password):
    """ 获取一个账号的Cookie """
    # loginURL = "https://login.sina.com.cn/sso/login.php?client=ssologin.js(v1.4.18)"
    # username = base64.b64encode(account.encode("utf-8")).decode("utf-8")
    # postData = {
    #     "entry": "sso",
    #     "gateway": "1",
    #     "from": "null",
    #     "savestate": "30",
    #     "useticket": "0",
    #     "pagerefer": "",
    #     "vsnf": "1",
    #     "su": username,
    #     "service": "sso",
    #     "sp": password,
    #     "sr": "1440*900",
    #     "encoding": "UTF-8",
    #     "cdult": "3",
    #     "domain": "sina.com.cn",
    #     "prelt": "0",
    #     "returntype": "TEXT",
    # }
    # session = requests.Session()
    # r = session.post(loginURL, data=postData)
    # jsonStr = r.content.decode("gbk")
    # info = json.loads(jsonStr)
    # if info["retcode"] == "0":
    #     logger.warning("Get Cookie Success!( Account:%s )" % account)
    #     cookie = session.cookies.get_dict()
    #     return json.dumps(cookie)
    # else:
    #     logger.warning("Failed!( Reason:%s )" % info["reason"])
    #     return ""


def get_cookie_from_weibo_cn(account, password):
    """ 获取一个账号的Cookie """
    try:
        browser = webdriver.PhantomJS(desired_capabilities=dcap)
        browser.get("https://weibo.cn/login/")
        time.sleep(1)

        # failure = 0
        if "微博" in browser.title:
            # failure += 1
            browser.save_screenshot("aa.png")
            username = browser.find_element_by_id("loginName")
            username.clear()
            username.send_keys(account)

            psd = browser.find_element_by_xpath('//input[@type="password"]')
            psd.clear()
            psd.send_keys(password)
            # try:
            #     code = browser.find_element_by_id("loginVCode")
            #     code.clear()
            #     if IDENTIFY == 1:
            #         code_txt = input("请查看路径下新生成的aa.png，然后输入验证码:")  # 手动输入验证码
            #     else:
            #         from PIL import Image
            #         img = browser.find_element_by_xpath('//form[@method="post"]/div/img[@alt="请打开图片显示"]')
            #         x = img.location["x"]
            #         y = img.location["y"]
            #         im = Image.open("aa.png")
            #         im.crop((x, y, 100 + x, y + 22)).save("ab.png")  # 剪切出验证码
            #         code_txt = identify()  # 验证码打码平台识别
            #     code.send_keys(code_txt)
            # except Exception as e:
            #     pass

            commit = browser.find_element_by_id("loginAction")
            commit.click()
            time.sleep(3)
            if "我的首页" not in browser.title:
                time.sleep(4)
            if '未激活微博' in browser.page_source:
                print('账号未开通微博')
                return {}

        cookie = {}
        print(browser.title)
        cookieList = []
        if "我的首页" in browser.title:
            for elem in browser.get_cookies():
                cookie[elem["name"]] = elem["value"]
                cookieList.append(str(elem["name"])+"="+str(elem["value"]))
            logger.warning("Get Cookie Success!( Account:%s )" % account)
            test_url = "https://weibo.cn/5235640836/profile?filter=1&page=1"
            test_url2 = "http://weibo.com/5235640836/profile?topnav=1&wvr=6&is_all=1"
            cookies = ";".join(cookieList)
            print(cookies)
            headers1 = {
                'User-Agent': 'Mozilla/5.0 (Windows NT 6.3; WOW64; rv:41.0) Gecko/20100101 Firefox/41.0',
                'Cookie': cookies,
            }
            req = request.Request(test_url2, headers=headers1)
            page = request.urlopen(req).read().decode("utf-8")
            print(page)
        return json.dumps(cookie)
    except Exception as e:
        logger.warning("Failed %s!" % account)
        print(e)
        return ""
    finally:
        try:
            browser.quit()
        except Exception as e:
            pass



def getCookies(weibo):
    """ 获取Cookies """
    cookies = []
    for elem in weibo:
        account = elem['no']
        password = elem['psw']
        cookie  =  getCookie(account, password)
        if cookie != None:
            cookies.append(cookie)

    return cookies


cookies = getCookies(myWeiBo)
logger.warning("Get Cookies Finish!( Num:%d)" % len(cookies))

# if __name__ == '__main__':
#     cookies = getCookies(myWeiBo)
#     print("===cookies17084633974====")
#     print(cookies)
#     logger.warning("Get Cookies Finish!( Num:%d)" % len(cookies))
