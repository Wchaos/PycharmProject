import scrapy
from scrapy.crawler import CrawlerProcess
from Sina_spider2.spiders.informationSpider import Spider1
from Sina_spider2.spiders.tweetsSpider import Spider2



process = CrawlerProcess()
process.crawl(Spider1)
process.crawl(Spider2)
process.start() # the script will block here until all crawling jobs are finished