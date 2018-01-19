# -*- coding: utf-8 -*-

# Define here the models for your spider middleware
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/spider-middleware.html
import json
import random

import time
from qichacha_webdriver.user_agent import agents
from qichacha_webdriver.user_agent import cookies
from scrapy.http import HtmlResponse
from selenium import webdriver


class CookiesMiddleware(object):
    def process_request(self,request,spider):
        cookie = random.choice(cookies)
        cookie = dict(elem.strip().split('=') for elem in cookie.split(';'))
        spider.browser.delete_all_cookies()
        for key, value in cookie.items():
            dic = {
                'domain': 'www.qichacha.com',
                'name': str(key),
                'value': str(value),
                'path': '/',
                'secure': True,
            }
            spider.browser.add_cookie(dic)
            time.sleep(1)


class JavaScriptMiddleware(object):
    def process_request(self, request, spider):
        spider.browser.get(request.url)
        print("页面渲染中····开始自动下拉页面")
        indexPage = 1000
        while indexPage < spider.browser.execute_script("return document.body.offsetHeight"):
            spider.browser.execute_script("scroll(0," + str(indexPage) + ")")
            indexPage = indexPage + 1000
            print(indexPage)
            time.sleep(1)

        rendered_body = spider.browser.page_source
        if r'charset="GBK"' in rendered_body or r'charset=gbk' in rendered_body:
            coding = 'gbk'
        else:
            coding = 'utf-8'
            print("=======in middleware=======")
        print(rendered_body)
        return HtmlResponse(url=spider.browser.current_url, body=rendered_body, encoding=coding,request=request)

