import re
import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.support import expected_conditions as EC


def login(account, passwd, url):
    # 如果driver没加入环境变量中，那么就需要明确指定其路径
    # 验证于2017年4月11日
    # 直接登陆新浪微博
    driver = webdriver.Chrome()
    driver.maximize_window()
    # locator = (By.)
    driver.get(url)
    time.sleep(1)
    print('开始登陆')
    name_field = driver.find_element_by_id('username')
    name_field.clear()
    name_field.send_keys(account)
    password_field = driver.find_element_by_id('password')
    password_field.clear()
    password_field.send_keys(passwd)

    # submit = driver.find_element_by_xpath('//*[@id="pl_login_form"]/div/div[3]/div[6]/a/span')
    submit = driver.find_element_by_xpath('//div[@class = "btn_mod"]/input')
    # submit = driver.find_element_by_id('loginAction')
    ActionChains(driver).double_click(submit).perform()
    time.sleep(5)
    # WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.CLASS_NAME, 'WB_miniblog')))

    source = driver.page_source
    print(source)

    if is_login(source):
        print('登录成功')

    sina_cookies = driver.get_cookies()
    driver.quit()
    return sina_cookies


def is_login(source):
    rs = re.search("CONFIG\['islogin'\]='(\d)'", source)
    if rs:
        return int(rs.group(1)) == 1
    else:
        return False


if __name__ == '__main__':
    # url = 'http://weibo.com/login.php'
    url = 'https://login.sina.com.cn/signup/signin.php?entry=sso'

    # name_input = input('请输入你的账号17084633974\n')
    name_input = '17084633974'
    passwd_input = 'a601751'
    # passwd_input = input('请输入你的密码a601751\n')
    cookies = login(name_input, passwd_input, url)
    print("===cookies17084633974====")
    print(cookies)








