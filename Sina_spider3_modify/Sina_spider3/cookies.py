# encoding=utf-8
# ------------------------------------------
#   版本：3.0
#   日期：2016-12-01
#   作者：九茶<http://blog.csdn.net/bone_ace>
# ------------------------------------------

import base64
import os
import requests
import time
import json
from selenium import webdriver
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities
import logging
import random
import numpy
import sys
from PIL import Image
from math import sqrt
from Sina_spider3.ims import ims
from selenium import webdriver
from selenium.webdriver.remote.command import Command
from selenium.webdriver.common.action_chains import ActionChains
from Sina_spider3.wap_login_direct import wap_login
from Sina_spider3.yumdama import identify

IDENTIFY = 1  # 验证码输入方式:        1:看截图aa.png，手动输入     2:云打码
COOKIE_GETWAY =2 # 0 代表从https://login.sina.com.cn/sso/login.php?client=ssologin.js(v1.4.18) 获取cookie   # 1 代表从https://weibo.cn/login/获取Cookie
dcap = dict(DesiredCapabilities.PHANTOMJS)  # PhantomJS需要使用老版手机的user-agent，不然验证码会无法通过
dcap["phantomjs.page.settings.userAgent"] = (
    "Mozilla/5.0 (Linux; U; Android 2.3.6; en-us; Nexus S Build/GRK39F) AppleWebKit/533.1 (KHTML, like Gecko) Version/4.0 Mobile Safari/533.1"
)
logger = logging.getLogger(__name__)
logging.getLogger("selenium").setLevel(logging.WARNING)  # 将selenium的日志级别设成WARNING，太烦人

"""
    输入你的微博账号和密码，可去淘宝买，一元5个。
    建议买几十个，实际生产建议100+，微博反爬得厉害，太频繁了会出现302转移。
"""
myWeiBo = [
      # {'no': '18264502806', 'psw': 'cgghovf3'},
    ('18264502806', 'cgghovf3'),
     # ('17077126433', 'ddyqht69011'),
]
PIXELS = []

def getCookie(account, password):
    if COOKIE_GETWAY == 0:
        return get_cookie_from_login_sina_com_cn(account, password)
    elif COOKIE_GETWAY ==1:
        return get_cookie_from_weibo_cn(account, password)
    elif COOKIE_GETWAY == 2:
        return wap_login(account, password)
    else:
        logger.error("COOKIE_GETWAY Error!")

def get_cookie_from_login_sina_com_cn(account, password):
    """ 获取一个账号的Cookie """
    loginURL = "https://login.sina.com.cn/sso/login.php?client=ssologin.js(v1.4.18)"
    username = base64.b64encode(account.encode("utf-8")).decode("utf-8")
    postData = {
        "entry": "sso",
        "gateway": "1",
        "from": "null",
        "savestate": "30",
        "useticket": "0",
        "pagerefer": "",
        "vsnf": "1",
        "su": username,
        "service": "sso",
        "sp": password,
        "sr": "1440*900",
        "encoding": "UTF-8",
        "cdult": "3",
        "domain": "sina.com.cn",
        "prelt": "0",
        "returntype": "TEXT",
    }
    session = requests.Session()
    r = session.post(loginURL, data=postData)
    jsonStr = r.content.decode("gbk")
    info = json.loads(jsonStr)
    if info["retcode"] == "0":
        logger.warning("Get Cookie Success!( Account:%s )" % account)
        cookie = session.cookies.get_dict()
        return json.dumps(cookie)
    else:
        logger.warning("Failed!( Reason:%s )" % info["reason"])
        return ""


def getExactly(im):
    """ 精确剪切"""
    imin = -1
    imax = -1
    jmin = -1
    jmax = -1
    row = im.size[0]
    col = im.size[1]
    for i in range(row):
        for j in range(col):
            if im.load()[i, j] != 255:
                imax = i
                break
        if imax == -1:
            imin = i

    for j in range(col):
        for i in range(row):
            if im.load()[i, j] != 255:
                jmax = j
                break
        if jmax == -1:
            jmin = j
    return (imin + 1, jmin + 1, imax + 1, jmax + 1)


def getType(browser):
    """ 识别图形路径 """
    ttype = ''
    time.sleep(3.5)
    # im0 = Image.open(io.BytesIO(browser.get_screenshot_as_png()))
    browser.save_screenshot("aa.png")
    im0 = Image.open("aa.png")
    box = browser.find_element_by_id('patternCaptchaHolder')#获取图形验证码对话框部分
    # im = im0.crop((int(box.location['x']) + 10, int(box.location['y']) + 100, int(box.location['x']) + box.size['width'] - 10, int(box.location['y']) + box.size['height'] - 10)).convert('L')
    im0.crop((int(box.location['x']) + 10, \
              int(box.location['y']) + 100, \
              int(box.location['x']) + box.size['width'] - 10, \
              int(box.location['y']) + box.size['height'] - 10)).save("bb.png")#（left, upper, right, lower）
    im = Image.open("bb.png").convert("L")#转换为灰色图像
    im.save("cc.png")
    newBox = getExactly(im)
    im.crop(newBox).save("dd.png")
    im = im.crop(newBox)
    width = im.size[0]
    height = im.size[1]
    min_dist = sys.maxsize#python int类型支持的最大值
    for png in ims.keys():
        # isGoingOn = True
        distance = 0
        for i in range(width):
            for j in range(height):
                distance += numpy.square(im.load()[i, j] - ims[png][i][j])# numpy.square计算各元素的平方

        if (distance != 0):
            distance = numpy.sqrt(distance)#sqrt计算平方根
        if (distance <= min_dist):
            min_dist = distance
            ttype = png
        # for i in range(width):
        #     for j in range(height):
        #         if ((im.load()[i, j] >= 245 and ims[png][i][j] < 245) or (im.load()[i, j] < 245 and ims[png][i][j] >= 245)) and abs(ims[png][i][j] - im.load()[i, j]) > 10: # 以245为临界值，大约245为空白，小于245为线条；两个像素之间的差大约10，是为了去除245边界上的误差
        #             isGoingOn = False
        #             break
        #     if isGoingOn is False:
        #         ttype = ''
        #         break
        #     else:
        #         ttype = png
        # else:
        #     break

    px0_x = box.location['x'] + 40 + newBox[0]
    px1_y = box.location['y'] + 130 + newBox[1]
    PIXELS.append((px0_x, px1_y))
    PIXELS.append((px0_x + 100, px1_y))
    PIXELS.append((px0_x, px1_y + 100))
    PIXELS.append((px0_x + 100, px1_y + 100))
    return ttype


def move(browser, coordinate, coordinate0):
    """ 从坐标coordinate0，移动到坐标coordinate """
    time.sleep(0.05)
    length = sqrt((coordinate[0] - coordinate0[0]) ** 2 + (coordinate[1] - coordinate0[1]) ** 2)  # 两点直线距离
    if length < 4:  # 如果两点之间距离小于4px，直接划过去
        ActionChains(browser).move_by_offset(coordinate[0] - coordinate0[0], coordinate[1] - coordinate0[1]).perform()
        return
    else:  # 递归，不断向着终点滑动
        step = random.randint(3, 5)
        x = int(step * (coordinate[0] - coordinate0[0]) / length)  # 按比例
        y = int(step * (coordinate[1] - coordinate0[1]) / length)
        ActionChains(browser).move_by_offset(x, y).perform()
        move(browser, coordinate, (coordinate0[0] + x, coordinate0[1] + y))


def draw(browser, ttype):
    """ 滑动 """
    if len(ttype) == 4:
        px0 = PIXELS[int(ttype[0]) - 1]
        login = browser.find_element_by_id('loginAction')
        ActionChains(browser).move_to_element(login).move_by_offset(px0[0] - login.location['x'] - int(login.size['width'] / 2), px0[1] - login.location['y'] - int(login.size['height'] / 2)).perform()
        browser.execute(Command.MOUSE_DOWN, {})

        px1 = PIXELS[int(ttype[1]) - 1]
        move(browser, (px1[0], px1[1]), px0)

        px2 = PIXELS[int(ttype[2]) - 1]
        move(browser, (px2[0], px2[1]), px1)

        px3 = PIXELS[int(ttype[3]) - 1]
        move(browser, (px3[0], px3[1]), px2)
        browser.execute(Command.MOUSE_UP, {})
    else:
        print ('Sorry! Failed! Maybe you need to update the code.')



def get_cookie_from_weibo_cn(account, password):
    """ 获取一个账号的Cookie """
    try:
        browser = webdriver.Chrome()
        browser.set_window_size(1050, 840)
        browser.get('https://passport.weibo.cn/signin/login?entry=mweibo&r=https://weibo.cn/。')
        time.sleep(1)
        name = browser.find_element_by_id('loginName')
        psw = browser.find_element_by_id('loginPassword')
        login = browser.find_element_by_id('loginAction')
        name.send_keys(account)  # 测试账号
        psw.send_keys(password)
        login.click()

        ttype = getType(browser)  # 识别图形路径
        print('Result: %s!' % ttype)
        draw(browser, ttype)  # 滑动破解
        time.sleep(20)
        cookie = {}

        # print("111111111111111111")
        # print("我的首页" in browser.title)
        if "我的首页" in browser.title:
            for elem in browser.get_cookies():
                cookie[elem["name"]] = elem["value"]
            logger.warning("Get Cookie Success!( Account:18264502806 )")
        print(json.dumps(cookie))
        return json.dumps(cookie)


        # browser = webdriver.PhantomJS(desired_capabilities=dcap)
        # browser.get("https://weibo.cn/login/")
        # time.sleep(1)
        #
        # failure = 0
        # while "微博" in browser.title and failure < 5:
        #     failure += 1
        #     browser.save_screenshot("aa.png")
        #     username = browser.find_element_by_name("mobile")
        #     username.clear()
        #     username.send_keys(account)
        #
        #     psd = browser.find_element_by_xpath('//input[@type="password"]')
        #     psd.clear()
        #     psd.send_keys(password)
        #     try:
        #         code = browser.find_element_by_name("code")
        #         code.clear()
        #         if IDENTIFY == 1:
        #             code_txt = raw_input("请查看路径下新生成的aa.png，然后输入验证码:")  # 手动输入验证码
        #         else:
        #             from PIL import Image
        #             img = browser.find_element_by_xpath('//form[@method="post"]/div/img[@alt="请打开图片显示"]')
        #             x = img.location["x"]
        #             y = img.location["y"]
        #             im = Image.open("aa.png")
        #             im.crop((x, y, 100 + x, y + 22)).save("ab.png")  # 剪切出验证码
        #             code_txt = identify()  # 验证码打码平台识别
        #         code.send_keys(code_txt)
        #     except Exception, e:
        #         pass
        #
        #     commit = browser.find_element_by_name("submit")
        #     commit.click()
        #     time.sleep(3)
        #     if "我的首页" not in browser.title:
        #         time.sleep(4)
        #     if '未激活微博' in browser.page_source:
        #         print ('账号未开通微博')
        #         return {}
        #
        # cookie = {}
        # if "我的首页" in browser.title:
        #     for elem in browser.get_cookies():
        #         cookie[elem["name"]] = elem["value"]
        #     logger.warning("Get Cookie Success!( Account:%s )" % account)
        # return json.dumps(cookie)
    except :
        logger.warning("Failed %s!" % account)
        return ""
    finally:
        try:
            browser.quit()
        except:
            pass


def initCookie(rconn, spiderName):
    """ 获取所有账号的Cookies，存入Redis。如果Redis已有该账号的Cookie，则不再获取。 """
    for weibo in myWeiBo:
        if rconn.get("%s:Cookies:%s--%s" % (spiderName, weibo[0], weibo[1])) is None:  # 'SinaSpider:Cookies:账号--密码'，为None即不存在。
            cookie = getCookie(weibo[0], weibo[1])
            if len(cookie) > 0:
                rconn.set("%s:Cookies:%s--%s" % (spiderName, weibo[0], weibo[1]), cookie)
    cookieNum ="".join(rconn.keys()).count("SinaSpider:Cookies")#b''是一个空字节,使用空字节把字节列表连接在一起，成为一个新的字节串
    logger.warning("The num of the cookies is %s" % cookieNum)
    if cookieNum == 0:
        logger.warning('Stopping...')
        os.system("pause")


def updateCookie(accountText, rconn, spiderName):
    """ 更新一个账号的Cookie """
    account = accountText.split("--")[0]
    password = accountText.split("--")[1]
    cookie = getCookie(account, password)
    if len(cookie) > 0:
        logger.warning("The cookie of %s has been updated successfully!" % account)
        rconn.set("%s:Cookies:%s" % (spiderName, accountText), cookie)
    else:
        logger.warning("The cookie of %s updated failed! Remove it!" % accountText)
        removeCookie(accountText, rconn, spiderName)


def removeCookie(accountText, rconn, spiderName):
    """ 删除某个账号的Cookie """
    rconn.delete("%s:Cookies:%s" % (spiderName, accountText))
    cookieNum ="".join(rconn.keys()).count("SinaSpider:Cookies")  # b''是一个空字节,使用空字节把字节列表连接在一起，成为一个新的字节串
    # cookieNum = "".join(rconn.keys()).count("SinaSpider:Cookies")
    logger.warning("The num of the cookies left is %s" % cookieNum)
    if cookieNum == 0:
        logger.warning("Stopping...")
        os.system("pause")