import time

from scrapy import Selector
from scrapy.http import HtmlResponse
from selenium import webdriver

browser = webdriver.Chrome()
prov_list = ['AH', 'BJ', 'CQ', 'FJ', 'GS', 'GD', 'GX', 'GZ', 'HAIN', 'HB', 'HLJ', 'HEN', 'HUB', 'HUN',\
             'JS', 'JX', 'JL', 'LN', 'NMG', 'NX', 'QH', 'SD', 'SH', 'SX', 'SAX', 'SC', 'TJ', 'XJ',\
             'XZ', 'YN', 'ZJ']
query_url = "https://www.qichacha.com/gongsi_area.shtml"
print(prov_list[0:1])
for prov in prov_list[0:1]:
    for page in range(1, 501):
        url = query_url + "?prov=" + prov + "&p=" + str(page)
        time.sleep(1)
        browser.get(url)
        time.sleep(2)
        res = browser.page_source
        if"信息查询系统" in browser.title:
            print("in company list page")
            response = HtmlResponse(url=url, body=res, encoding="utf-8")
            selector = Selector(response)
            company_list = selector.xpath(
                '//div[@class="col-md-12"]// section[@class="panel panel-default" and @id="searchlist"]/a/@href').extract()
            for company_url in company_list:
                company_url = 'http://www.qichacha.com' + company_url
                time.sleep(3)
                browser.get(company_url)




