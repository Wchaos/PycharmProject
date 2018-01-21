# encoding=utf-8
import random
from Sina_spider2.user_agents import agents
from Sina_spider2.cookies import cookies


class UserAgentMiddleware(object):
    """ 换User-Agent """

    def process_request(self, request, spider):
        agent = random.choice(agents)
        request.headers["User-Agent"] = agent


class CookiesMiddleware(object):
    """ 换Cookie """

    def process_request(self, request, spider):
        cookie = random.choice(cookies)
        print("====cookie=====")
        print(cookie)
        request.cookies = cookie
