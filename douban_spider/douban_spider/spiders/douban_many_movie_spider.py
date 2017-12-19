from scrapy.spiders import Spider
from scrapy.http import Request
from scrapy.selector import Selector
from scrapy.spiders import Rule,CrawlSpider
from scrapy.linkextractors import LinkExtractor
from douban_spider.items import DoubanSpiderItem

class DoubanSpider(CrawlSpider):

    name="douban_many_movie_spider"
    download_delay=1
    allowed_domains=["http://movie.douban.com"]
    start_urls=[
        'http://movie.douban.com/top250'
    ]

    # rules=(
    #     Rule(LinkExtractor(allow=(r'http://movie\.douban\.com/top250?start=\d+&filter=')),callback='parse',follow=True),
    # )

    def parse(self,response):

        # print(response)

        sel=Selector(response)

        item=DoubanSpiderItem()

        movie_name=sel.xpath('//span[@class="title"][1]/text()').extract()
        star=sel.xpath('//div[@class="star"]/span[@class="rating_num"]/text()').extract()
        quote=sel.xpath('//p[@class="quote"]/span[@class="inq"]/text()').extract()

        item['movie_name']=[n for n in movie_name]
        item['star']=[n for n in star]
        item['quote']=[n for n in quote]

        yield item

        # print(item)
        next_url = response.xpath('//span[@class="next"]/a/@href').extract()
        if next_url:
            next_url = 'https://movie.douban.com/top250' + next_url[0]
            print(next_url)
            yield Request(next_url, callback=self.parse)
