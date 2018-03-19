from scrapy import cmdline
import os

launch_method = 1

if launch_method==1:
    cmdline.execute("scrapy crawl taobaomm".split())
elif launch_method == 2:
    os.system("scrapy crawl taobaomm")