#coding: utf-8


from scrapy.linkextractors import LinkExtractor
from scrapy.contrib.spiders import CrawlSpider, Rule
from scrapy.selector import Selector

from MySpider.items import legItem


class aalegSpider(CrawlSpider):
    name="aaleg"
    allowed_domains=["aaleg.com"]
    start_urls=["http://www.aaleg.com/"]
    custom_settings = {
    "ITEM_PIPELINES":{'scrapy.pipelines.images.ImagesPipeline': 1},
    "IMAGES_STORE":"/Users/Apple/Pictures/legs"
    }
 
    rules = (
        Rule(LinkExtractor(allow=('/\d*.html')),callback='parse_page',follow=True),
        Rule(LinkExtractor(allow=('/\d*.html/\d*')),callback='parse_page'),
    )
    
    
    def parse_page(self,response):
        self.log("find a page")
        sel = Selector(response)
        item = legItem()
        urls = sel.xpath("//div[@class='picsbox picsboxcenter']//img/@src").extract()
        imageUrls = []
        for url in urls:
            imageUrls.append(url)
        item['image_urls'] = imageUrls
        return item
        
        