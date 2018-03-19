# # -*- coding: utf-8 -*-
#
# # Define here the models for your spider middleware
# #
# # See documentation in:
# # http://doc.scrapy.org/en/latest/topics/spider-middleware.html
#
# from scrapy import signals
#
#
# class TaobaommSpiderMiddleware(object):
#     # Not all methods need to be defined. If a method is not defined,
#     # scrapy acts as if the spider middleware does not modify the
#     # passed objects.
#
#     @classmethod
#     def from_crawler(cls, crawler):
#         # This method is used by Scrapy to create your spiders.
#         s = cls()
#         crawler.signals.connect(s.spider_opened, signal=signals.spider_opened)
#         return s
#
#     def process_spider_input(self, response, spider):
#         # Called for each response that goes through the spider
#         # middleware and into the spider.
#
#         # Should return None or raise an exception.
#         return None
#
#     def process_spider_output(self, response, result, spider):
#         # Called with the results returned from the Spider, after
#         # it has processed the response.
#
#         # Must return an iterable of Request, dict or Item objects.
#         for i in result:
#             yield i
#
#     def process_spider_exception(self, response, exception, spider):
#         # Called when a spider or process_spider_input() method
#         # (from other spider middleware) raises an exception.
#
#         # Should return either None or an iterable of Response, dict
#         # or Item objects.
#         pass
#
#     def process_start_requests(self, start_requests, spider):
#         # Called with the start requests of the spider, and works
#         # similarly to the process_spider_output() method, except
#         # that it doesn’t have a response associated.
#
#         # Must return only requests (not items).
#         for r in start_requests:
#             yield r
#
#     def spider_opened(self, spider):
#         spider.logger.info('Spider opened: %s' % spider.name)
from scrapy.exceptions import CloseSpider

from taobaomm.myexceptions import ExtractError


class TestMiddleware(object):
    def __init__(self,crawler):
        self.crawler = crawler
        self.count = 0


    @classmethod
    def from_crawler(cls, crawler):
        return cls(crawler)

    # def process_spider_input(self,response,spider):
    #     self.count += 1
    #     if(self.count==5):
    #         print("======in test middleware========")
    #         raise CloseSpider("in exception")
            # raise Exception("test exception in middleware")


    def process_spider_exception(self, response, exception, spider):
        print("=======in spider exception==========")
        if isinstance(exception,ExtractError):
            print(exception.reason)
        pause_method = 2
        if pause_method == 2:
            self.crawler.engine.close_spider(spider, 'closespider_blee')
        elif pause_method == 3:
            self.crawler._signal_shutdown(9, 0)

