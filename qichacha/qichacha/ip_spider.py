import time

from bs4 import BeautifulSoup
from scrapy import Selector
from scrapy.http import HtmlResponse
from selenium import webdriver


# chromeOptions = webdriver.ChromeOptions();
# 设置为 headless 模式
# chromeOptions.add_argument("--headless")
# browser = webdriver.Chrome(chrome_options=chromeOptions)
browser = webdriver.Chrome()

for page in range(1, 2):
    url = 'http://www.goubanjia.com/free/index%s.shtml' % page
    # print(url)
    time.sleep(1)
    browser.get(url)
    time.sleep(2)
    print(browser.title)
    if"免费代理IP" in browser.title:
        res = browser.page_source
        response = HtmlResponse(url=url, body=res, encoding="utf-8")
        selector = Selector(response)
        ip_block_list = selector.xpath('//div[@id="list"]/table/tbody//tr/td[@class="ip"]').extract()
        print(ip_block_list)
        for ip_block in ip_block_list:
            soup = BeautifulSoup(ip_block,"lxml")
            span_list = soup.find_all({'span','div'})
            digital_list = []

            for span in span_list:
                digital = span.get_text()
                digital_list.append(digital)

            digital_list.insert(-1, ':')
            ip = ''.join(digital_list)
            print(ip)

    else:
        print('访问页面出错')



