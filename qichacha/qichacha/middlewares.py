# -*- coding: utf-8 -*-

# Define here the models for your spider middleware
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/spider-middleware.html
import json
import random
import pymongo
import requests

from scrapy.conf import settings
from scrapy.exceptions import IgnoreRequest
from scrapy.log import logger

from qichacha.user_agent import agents
from qichacha.cookies import get_cookie_from_mongodb

class UserAgentMiddleware(object):
    def process_request(self,request,spider):
        agent = random.choice(agents)
        request.headers["User-Agent"] = agent


class CookiesMiddleware(object):

    def process_request(self,request,spider):
        cookies = get_cookie_from_mongodb()
        cookie = random.choice(cookies)
        cookie = dict(elem.strip().split('=') for elem in cookie.split(';'))
        request.cookies = cookie


class ProxyMiddleware(object):
    """ 换IP """

    def getproxy(self):
        url = "http://192.168.117.96:5010/get/"
        # url = "http://api.ip.data5u.com/dynamic/get.html?order=facac5444919f53d283037d813d3bc83&sep=3"
        response = requests.get(url)
        ip = response.content.decode("utf-8")
        print(ip)
        return ip
    def process_request(self, request, spider):
        try:
            ip = self.getproxy()
        except Exception as e:
            ip = None
        request.meta['proxy'] = ip

    def process_response(self, request, response, spider):
        if response.status != 200:
            if "fail_times" not in  request.meta:
                request.meta['fail_times'] = 0
                return request
            elif request.meta['fail_times'] < 4:
                request.meta['fail_times'] += 1
                return request
            else:
                raise IgnoreRequest
        else:
            return response





