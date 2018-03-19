# -*- coding: utf-8 -*-

# Define here the models for your spider middleware
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/spider-middleware.html
import random
import time

from scrapy.http import HtmlResponse


class JavaScriptMiddleware(object):
    """
    使用webdriver驱动的浏览器 替换 scrapy内置的下载器，
    将浏览器渲染好的page_source封装成Response对象返回
    """
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
        # print(rendered_body)
        return HtmlResponse(url=spider.browser.current_url, body=rendered_body, encoding=coding,request=request)



cookies = [
    # "UM_distinctid=160e2d81c50990-02b5c26ad8127a-3c60460e-1fa400-160e2d81c519ff; zg_did=%7B%22did%22%3A%20%22160e2d81ca8a30-063c6b9592827f-3c60460e-1fa400-160e2d81ca989a%22%7D; _uab_collina=151563431335470821865698; PHPSESSID=qn1ke5nq0nv5fcegjltl7oi8i1; acw_tc=AQAAAPMWnhZebwwA01TheRVXh69Gwu1x; CNZZDATA1254842228=1095774501-1515630171-https%253A%252F%252Fwww.baidu.com%252F%7C1516235019; hasShow=1; _umdata=6AF5B463492A874DE2AC1E797FCC27F90AFBA28B4D91C5BCA88672C32B307E8CD48E4705FB32E472CD43AD3E795C914CDB578452826F1A28B78BDA5953496167; acw_sc__=5a5ff4023f04f698678f4be7439be5e339ce3729; zg_de1d1a35bfa24ce29bbf2c7eb17e6c4f=%7B%22sid%22%3A%201516236444579%2C%22updated%22%3A%201516237826590%2C%22info%22%3A%201515634302125%2C%22superProperty%22%3A%20%22%7B%7D%22%2C%22platform%22%3A%20%22%7B%7D%22%2C%22utm%22%3A%20%22%7B%7D%22%2C%22referrerDomain%22%3A%20%22www.baidu.com%22%2C%22cuid%22%3A%20%221808beafd3fccded98b033ef2c545779%22%7D",
    "UM_distinctid=160fd15721a9c9-071aff60ca647f-7b113d-1fa400-160fd15721bc1c; _uab_collina=151609163784756238080354; acw_tc=AQAAANwIZhO0pAMA01TheaMKJ/4EztGO; hasShow=1; zg_did=%7B%22did%22%3A%20%22160fd15722d136-0d486f5fca1888-7b113d-1fa400-160fd15722ea15%22%7D; CNZZDATA1254842228=918165069-1516073157-null%7C1516240667; _umdata=55F3A8BFC9C50DDA6D5B01D1A2C4BD594729A3C2F0A1F368B20B7C98FE1BB44573933CC5503128B8CD43AD3E795C914CDB578452826F1A2810689DF00059E9A6; zg_de1d1a35bfa24ce29bbf2c7eb17e6c4f=%7B%22sid%22%3A%201516244097614%2C%22updated%22%3A%201516245509558%2C%22info%22%3A%201516074529331%2C%22superProperty%22%3A%20%22%7B%7D%22%2C%22platform%22%3A%20%22%7B%7D%22%2C%22utm%22%3A%20%22%7B%7D%22%2C%22referrerDomain%22%3A%20%22%22%2C%22cuid%22%3A%20%22076ec19e42d4f48979bef4ad1a1450a5%22%7D; PHPSESSID=9s800680tofhjn2fdtfbjvr552"
]

class CookiesMiddleware(object):
    """
    尝试替换cookie，来获得浏览器的登录状态，
    但是频繁的切换会出问题，此类暂时弃用。

    本爬虫使用游客身份访问页面进行爬取
    """

    def process_request(self, request, spider):
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
