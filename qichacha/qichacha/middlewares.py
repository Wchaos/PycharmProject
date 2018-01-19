# -*- coding: utf-8 -*-

# Define here the models for your spider middleware
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/spider-middleware.html
import json
import random

from qichacha.user_agent import agents
from qichacha.user_agent import cookies

class UserAgentMiddleware(object):
    def process_request(self,request,spider):
        agent = random.choice(agents)
        request.headers["User-Agent"] = agent


class CookiesMiddleware(object):
    def process_request(self,request,spider):
        cookie = random.choice(cookies)
        cookie = dict(elem.strip().split('=') for elem in cookie.split(';'))
        request.cookies = cookie


