import json
import random
import re
import urllib

import time
from scrapy import Selector, Request, signals
from scrapy.spiders import CrawlSpider
from bs4 import BeautifulSoup
from selenium import webdriver
from scrapy.xlib.pydispatch import dispatcher

from qichacha_webdriver.items import BusinessInfoItem



class Spider(CrawlSpider):
    name = "qichacha_webdriver"
    allowed_domains = ["qichacha.com"]
    host = "http://www.qichacha.com"
    start_url = "https://www.qichacha.com/gongsi_area.shtml"
    prov_list = ['AH', 'BJ', 'CQ', 'FJ', 'GS', 'GD', 'GX', 'GZ', 'HAIN', 'HB', 'HLJ', 'HEN', 'HUB', 'HUN',\
                 'JS', 'JX', 'JL', 'LN', 'NMG', 'NX', 'QH', 'SD', 'SH', 'SX', 'SAX', 'SC', 'TJ', 'XJ',\
                 'XZ', 'YN', 'ZJ']


    def __init__(self):
        """初始化时候，给爬虫新开一个浏览器"""
        chrome_options = webdriver.ChromeOptions()
        # chrome_options.add_argument("--headless")  # 设置headless，隐藏浏览器界面
        self.browser = webdriver.Chrome(chrome_options=chrome_options)
        self.browser.maximize_window()
        super(Spider, self).__init__()
        dispatcher.connect(self.spider_closed, signals.spider_closed)#绑定信号和需要执行的方法
        self.browser.get("https://www.baidu.com")#打开一个没有缓存浏览器，直接范访问企查查页面，可能会出现405，此操作以便后续请求refer to 百度

    def spider_closed(self, spider):
        """当爬虫退出的时候关闭chrome"""
        print("spider closed")
        self.browser.quit()

    def start_requests(self):
        """
        重写start_requests方法，构造初始请求。
        此处指爬取了一个省的公司数据，要爬所有的可以将切片改为self.prov_list[0:-1]
        """
        for prov in self.prov_list[0:1]:
            for page in range(1, 501):
                query_url = self.start_url + "?prov=" + prov + "&p=" + str(page)
                yield Request(url=query_url,callback=self.parse2)


    def parse2(self, response):
        """提取页面中的公司url"""
        selector = Selector(response)
        company_list = selector.xpath('//div[@class="col-md-12"]// section[@class="panel panel-default" and @id="searchlist"]/a/@href').extract()
        for company_url in company_list:
            company_url = self.host + company_url
            yield Request(url= company_url,callback= self.parse3)

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
        for example list = [<td>key1</td>，<td>val1</td>，<td>key2</td>，<td>val2</td>]，
                   json is {'key1':'val','key2':'val2'}
        将提取的列表转化为json格式数据
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
