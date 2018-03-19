from time import sleep

from selenium import webdriver

browser = webdriver.Chrome()
browser.maximize_window()
# browser.get("https://www.baidu.com")
# sleep(2)
url = "http://www.qichacha.com"
browser.get(url)
sleep(3)
content = browser.page_source
print(content)
# sleep(5)
