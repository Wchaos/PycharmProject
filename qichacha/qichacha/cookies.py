import requests
import time

from bs4 import BeautifulSoup
from scrapy import Selector
from selenium import webdriver

if __name__ == '__main__':
    # browser = webdriver.Chrome()
    # browser = webdriver.Firefox()
    # browser.set_window_size(1050, 840)
    # browser.maximize_window()
    # browser.get('http://www.qichacha.com/user_login')
    # time.sleep(2)
    # phone_num = browser.find_element_by_id('nameNormal')
    # password = browser.find_element_by_id('pwdNormal')
    #
    # phone_num.send_keys('13951022018')
    # password.send_keys('940826lb')


    chromeOptions = webdriver.ChromeOptions();
    #设置为 headless 模式 （必须）
    chromeOptions.add_argument("--headless");
    #设置浏览器窗口打开大小  （非必须）
    chromeOptions.add_argument("--window-size=1920,1080")
    browser = webdriver.Chrome(chrome_options=chromeOptions)
    browser.get("http://www.baidu.com")
    title = browser.title
    print(title)
    browser.close()


