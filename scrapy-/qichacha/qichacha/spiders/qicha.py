# -*- coding: utf-8 -*-
import scrapy
from scrapy.http import FormRequest
from selenium import webdriver
from scrapy.xlib.pydispatch import dispatcher
from scrapy import signals
class QichaSpider(scrapy.Spider):
    name = "qichacha"
    allowed_domains = ["qichacha.com"]
    start_urls = ['http://www.qichacha.com/user_login']

    def __init__(self):
        self.browser = webdriver.Chrome()
        super(QichaSpider,self).__init__()


        dispatcher.connect(self.spider_closed,signals.spider_closed)


    def spider_closed(self,spider):
        #当爬虫退出的时候 关闭chrome
        print ("spider closed")
      # self.browser.quit()

    def parse(self, response):
          print(response.body.decode)

