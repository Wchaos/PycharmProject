import json
import re
import urllib

from scrapy import Selector, Request
from scrapy.spiders import CrawlSpider
from bs4 import BeautifulSoup

from qichacha.items import BusinessInfoItem


class Spider(CrawlSpider):
    name = "qichacha"
    allowed_domains = ["qichacha.com"]
    host = "http://www.qichacha.com"
    # start_urls = ["http://www.qichacha.com"]
    start_url = "https://www.qichacha.com/gongsi_area.shtml"
    prov_list = ['AH', 'BJ', 'CQ', 'FJ', 'GS', 'GD', 'GX', 'GZ', 'HAIN', 'HB', 'HLJ', 'HEN', 'HUB', 'HUN',\
                 'JS', 'JX', 'JL', 'LN', 'NMG', 'NX', 'QH', 'SD', 'SH', 'SX', 'SAX', 'SC', 'TJ', 'XJ',\
                 'XZ', 'YN', 'ZJ']

    def start_requests(self):
        for prov in self.prov_list[0:2]:
            for page in range(1, 501):
                query_url = self.start_url + "?prov=" + prov + "&p=" + str(page)
                yield Request(url=query_url,callback=self.parse2)

    # def parse(self, response):
    #     selector = Selector(response)
    #
    #     area_list = selector.xpath('//div[@class="tab-pane fade" and @id="area"]/ul//li/a/@href').extract()
    #     for area_url in area_list:
    #         area_url = self.host + area_url
    #         yield Request(url= area_url,callback=self.parse2)
        # yield Request(url=self.host+area_list[0], callback=self.parse2)

    def parse2(self, response):
        selector = Selector(response)
        company_list = selector.xpath('//div[@class="col-md-12"]// section[@class="panel panel-default" and @id="searchlist"]/a/@href').extract()
        for company_url in company_list:
            company_url = self.host + company_url
            yield Request(url= company_url,callback= self.parse3)
        # yield Request(url=self.host+company_list[0], callback=self.parse3)

    def parse3(self,response):
        """抓取公司名称、地址等基本属性信息"""
        businessInfoItem = BusinessInfoItem()
        selector = Selector(response)
        cret_url = selector.xpath('//div[@class="logo"]/div[2]/a[@class="c-renling"]/@href').extract_first()
        # company_name = selector.xpath('//div[@class="content"]/div[@class="row title"]/text()').extract_first()
        phone_num = selector.xpath('//div[@class="content"]/div[2]/span[@class= "cvlu"]/span/text()').extract_first()
        official_web = selector.xpath('//div[@class="content"]/div[3]/span[2]/a/text()').extract_first()
        email = selector.xpath('//div[@class="content"]/div[3]/span[4]/a/text()').extract_first()
        address = selector.xpath('//div[@class="content"]/div[4]/span[@class= "cvlu"]/a[@id= "mapPreview"]/text()').extract_first()

        businessInfoItem["phone_num"] = phone_num
        businessInfoItem["official_web"] = official_web
        businessInfoItem["email"] = email
        businessInfoItem["address"] = address
        if cret_url:
            _id = re.findall(r'companykey=(.*?)&',cret_url)[0]
            company_name = re.findall(r'companyname=(\S*)',cret_url)[0]
            if _id and company_name:
                businessInfoItem["_id"] = _id
                businessInfoItem["company_name"] = company_name

        """抓取基本信息中的工商信息表格"""
        legal_person = selector.xpath('//div[@class="boss-td"]/div//div/a[@class="bname"]/text()').extract_first()
        print("========")
        print(legal_person)
        table = selector.xpath('//section/table[2]').extract_first()
        soup = BeautifulSoup(table, "lxml")
        td_list = soup.find_all('td')
        business_info = self.list_to_json(td_list)

        businessInfoItem["legal_person"] = legal_person
        businessInfoItem['business_info'] = business_info

        yield businessInfoItem
        print(businessInfoItem)




    def list_to_json(self,list):
        """
        for example list = [key1，val1，key2，val2]，
                   json is {'key1':'val','key2':'val2'}
        """
        odd_list = []
        even_list = []
        for i in range(0, len(list)):
            text = list[i].get_text().strip().strip('：').strip(':')
            if i % 2 == 0:
                odd_list.append(text)
            else:
                even_list.append(text)
        dic_info = dict(zip(odd_list, even_list))
        json_info = json.dumps(dic_info, ensure_ascii=False)
        return json_info