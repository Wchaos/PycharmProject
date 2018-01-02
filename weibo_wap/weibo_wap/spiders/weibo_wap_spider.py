# -*- coding: utf-8 -*-
import re
from scrapy.spiders import CrawlSpider
from scrapy.selector import Selector
from scrapy.http import Request
from weibo_wap.items import TweetsItems

Account_Cookies = {"Cookie":"_T_WM=1612ee2cc20773a545dbb166d6637efb; ALF=1516330484; SCF=AtVVGfRA7BkkBL4uw9ZKGPuVpOGF5HXkxJHZhWH4dnps0mKjXEuPYBFesYEZKq75I4gnnWgK_1yNJpEbJtty8m8.; SUB=_2A253PaFXDeRhGeBK6FIY9yfIzjWIHXVUwc8frDV6PUJbktBeLU3BkW1NHetkT2BW0jEmkCLav2anFcZrELnkSyIw; SUBP=0033WrSXqPxfM725Ws9jqgMF55529P9D9W5yr_ZnLBpnU8ukEmFss4rU5JpX5K-hUgL.FoqXe054S0.XSK.2dJLoI05LxKqL1KMLBKMLxKnLBK2L1KMLxK.L1hML12eLxKML1-2L1hBLxK.L1h-L1Kz_PEXt; SUHB=0nlu1eqcEpL8Lf"}
Header = {
    "Host" : "weibo.cn",
    "Accept" : "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8",
    "Accept-Language" : "zh-CN,zh;q=0.9",
    "Accept-Encoding" : "gzip, deflate, br",
    "Connection":"keep-alive",
    "DNT" : "1",
    "Upgrade-Insecure-Requests" : "1",
    "User-Agent" : "Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/63.0.3239.108 Safari/537.36",
}



class Spider(CrawlSpider):
    name = "weibo_wap_spider"
    host = "https://weibo.cn"
    allowed_domains = ["weibo.cn"]
    start_urls = [
        5235640836, 5871897095, 2139359753, 5579672076, 5778999829, 5780802073, 2159807003,
        1756807885, 3378940452, 5762793904, 1885080105, 5778836010, 5722737202, 3105589817, 5882481217, 5831264835,
        2717354573, 3637185102, 1934363217, 5336500817, 1431308884, 5818747476, 5073111647, 5398825573, 2501511785,
    ]
    scrawl_ID = set(start_urls)  # 记录待爬的微博ID
    finish_ID = set()  # 记录已爬的微博ID

    def start_requests(self):
        while self.scrawl_ID.__len__():
            ID = self.scrawl_ID.pop()
            self.finish_ID.add(ID)
            ID = str(ID)

            url_tweets = "https://weibo.cn/%s/profile?filter=1&page=1" % ID
            yield Request(url=url_tweets,meta={"ID":ID},callback=self.parse)

    def parse(self,response):
        """抓取微博数据"""
        sel = Selector(response)
        tweets = sel.xpath('body/div[@class="c" and @id]')
        for tweet in tweets:
            tweetsItems = TweetsItems()

            data_id = tweet.xpath('@id').extract_first() #微博ID
            content = tweet.xpath('div/span[@class="ctt"]/text()').extract_first() #微博内容
            cooridinates = tweet.xpath('div/a/@herf').extract_first() #定位坐标
            like = re.findall(u'\u8d5e\[(\d+)\]', tweet.extract())  # 点赞数
            transfer = re.findall(u'\u8f6c\u53d1\[(\d+)\]', tweet.extract())  # 转载数
            comment = re.findall(u'\u8bc4\u8bba\[(\d+)\]', tweet.extract())  # 评论数
            others = tweet.xpath('div/span[@class="ct"]/text()').extract_first()  # 求时间和使用工具（手机或平台）

            tweetsItems["ID"] = response.meta["ID"]
            tweetsItems["_id"] = response.meta["ID"] + "-" +data_id
            tweetsItems["Content"]=''
            tweetsItems["Co_oridinates"] = ''
            tweetsItems["Like"] = 0
            tweetsItems["Transfer"] = 0
            tweetsItems["Comment"] = 0
            tweetsItems["PubTime"] = ''
            tweetsItems["Tools"] = ''
            if content:
                tweetsItems["Content"] = content.strip(u"[\u4f4d\u7f6e]")  # 去掉最后的"[位置]"
            if cooridinates:
                cooridinates = re.findall('center=([\d|.|,]+)', cooridinates)
                if cooridinates:
                    tweetsItems["Co_oridinates"] = cooridinates[0]
            if like:
                tweetsItems["Like"] = int(like[0])
            if transfer:
                tweetsItems["Transfer"] = int(transfer[0])
            if comment:
                tweetsItems["Comment"] = int(comment[0])
            if others:
                others = others.split(u"\u6765\u81ea")
                tweetsItems["PubTime"] = others[0]
                if len(others) == 2:
                    tweetsItems["Tools"] = others[1]
            print(tweetsItems)
            yield tweetsItems

        # url_next = sel.xpath(
        #     u'body/div[@class="pa" and @id="pagelist"]/form/div/a[text()="\u4e0b\u9875"]/@href').extract()
        # if url_next:
        #     yield Request(url=self.host + url_next[0], meta={"ID": response.meta["ID"]}, callback=self.parse)







