import time

from bs4 import BeautifulSoup
from scrapy import Selector
from scrapy.http import HtmlResponse
from selenium import webdriver


chromeOptions = webdriver.ChromeOptions();
# 设置为 headless 模式
chromeOptions.add_argument("--headless")
browser = webdriver.Chrome(chrome_options=chromeOptions)
# browser = webdriver.Chrome()
ips_file_dir = "ip_list.txt"
ips_file = open(ips_file_dir, 'a', encoding='UTF-8')

for page in range(1, 99):
    url = 'http://www.goubanjia.com/free/gngn/index%s.shtml' % page
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
        type_block_list = selector.xpath('//div[@id="list"]/table/tbody//tr/td[3]/a/text()').extract()
        cnt = len(ip_block_list)
        for i in range(cnt):
            ip_block = ip_block_list[i]
            soup = BeautifulSoup(ip_block, "lxml")
            span_list = soup.find_all({'span', 'div'})
            digital_list = []
            for span in span_list:
                digital = span.get_text()
                digital_list.append(digital)
            digital_list.insert(-1, ':')
            ip = ''.join(digital_list)
            ips_file.write(ip+" "+type_block_list[i].split(",")[-1]+" \n")
        print("第%d页完成" % page)
    else:
        print('访问页面出错')
ips_file.close()



