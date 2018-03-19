import os

import sys

from scrapy import signals

from taobaomm.myexceptions import ExtractError


class PauseExtension(object):
    @classmethod
    def from_crawler(cls, crawler):
        return cls(crawler)

    def __init__(self,crawler):
        crawler.signals.connect(self.spider_error, signal=signals.spider_error)

    def spider_error(self, failure, response, spider):
        print("========in extension===========")
        print(spider.name)
        exception = failure.value
        if isinstance(exception, ExtractError):
            print(exception.reason)
        print("Error on {0}, traceback: {1}".format(response.url, failure.getTraceback()))




