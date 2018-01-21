# encoding=utf-8
from selenium import webdriver
from selenium.webdriver import ActionChains
import time
import json
import logging
logger = logging.getLogger(__name__)
logging.getLogger("selenium").setLevel(logging.WARNING)  # 将selenium的日志级别设成WARNING，太烦人
from PIL import ImageGrab
import pytesser3
driver=webdriver.Chrome('C:\develop_tools\chromedriver_win32\chromedriver')
driver.maximize_window()
driver.get('http://www.baidu.com')
time.sleep(2)
driver.get('http://www.qichacha.com/user_login')
# driver.delete_all_cookies()
time.sleep(2)
driver.get('http://www.qichacha.com/user_login')
# username = driver.find_element_by_name("nameNormal")
# username.clear()
# username.send_keys("13951022018")
# psd = driver.find_element_by_xpath('//input[@type="password"]')
# psd.clear()
# psd.send_keys("940826lb")
# time.sleep(3)
# fuck=driver.find_element_by_xpath("//*[@id='nc_1_n1z']")
# action=ActionChains(driver)
# action.click_and_hold(fuck)
# action.move_by_offset(308,0)
# action.release().perform()
# time.sleep(10)
# if driver.find_element_by_xpath("//*[@id='nc_1_scale_submit']/span"):
#     print(11111111111111111111111111)
#     print(driver.find_element_by_xpath("//*[@id='nc_1_scale_submit']/span"))
#     text1 = driver.find_element_by_xpath("//*[@id='nc_1_scale_submit']/span")
#     print(text1)
#     if text1.text.startswith(u'提交'):
#         addr = 'bb.png'
#         im = ImageGrab.grab((0, 415, 385, 440))
#         im.save(addr, 'png')

# if driver.find_element_by_xpath("//*[@id='nc_1__scale_text']"):
#     text2 = driver.find_element_by_xpath("//*[@id='nc_1__scale_text']")
#     print(222222222222222222222222222)
#     print(text2)
#     print(text2.text.startswith(u'请点击图中的'))
#     if text2.text.startswith(u'请点击图中的'):
#         addr = 'bb.png'
#         im = ImageGrab.grab((1117, 600, 1363, 830))
#         im.save(addr, 'png')

# driver.find_element_by_xpath('//*[@id="user_login_normal"]/button').click()
# cookie = {}
# if "企查查-企业注册信息查询|企业工商信息查询|企业信用信息查询查询系统" in driver.title:
#     print(1111111111111111111111)
#     for elem in driver.get_cookies():
#         cookie[elem["name"]] = elem["value"]
#     logger.warning("Get Cookie Success!( Account:18264502806 )")
# print("cookie------------------------------")
# print(json.dumps(cookie))



        # if text2.text.startswith(u'请点击图中的'):
# if driver.find_element_by_xpath("//*[@id='nc_1__scale_text']/span"):
#     print(33333333333333333333333333333)
#     text=driver.find_element_by_xpath("//*[@id='nc_1__scale_text']/span")
#     print(text)
#     print(text.text.startswith(u'请按住滑块，拖动到最右边'))
#     print(text.text.startswith(u'验证通过'))