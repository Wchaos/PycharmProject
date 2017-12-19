# -*- coding: utf-8 -*-
import json
import os
import urllib

from scrapy.http import FormRequest
from scrapy.spiders import Spider

from taobaomm.items import tbModelItem


class tbmmSpider(Spider):
    name = "taobaomm"
    allow_domians = ["mm.taobao.com"]

    def start_requests(self):
        url = "https://mm.taobao.com/tstar/search/tstar_model.do?_input_charset=utf-8"
        for i in range(1, 60):
            formdata = {"q": "",
                        "viewFlag": "A",
                        "sortType": "default",
                        "searchStyle": "",
                        "searchRegion": "city:",
                        "searchFansNum": "",
                        "currentPage": str(i),
                        "pageSize": "100"}
            yield FormRequest(url, callback=self.parse_model, formdata=formdata)



    def parse_model(self, response):
        jsonBody = json.loads(response.body.decode('gbk').encode('utf-8'))
        models = jsonBody['data']['searchDOList']

        for dict in models:
            modelItem = tbModelItem()
            modelItem['avatarUrl'] = dict['avatarUrl']
            modelItem['cardUrl'] = dict['cardUrl']
            modelItem['city'] = dict['city']
            modelItem['height'] = dict['height']
            modelItem['identityUrl'] = dict['identityUrl']
            modelItem['modelUrl'] = dict['modelUrl']
            modelItem['realName'] = dict['realName']
            modelItem['totalFanNum'] = dict['totalFanNum']
            modelItem['totalFavorNum'] = dict['totalFavorNum']
            modelItem['userId'] = dict['userId']
            modelItem['viewFlag'] = dict['viewFlag']
            modelItem['weight'] = dict['weight']

            yield modelItem
            self.downloadImage(modelItem['cardUrl'], modelItem['userId'])

    def downloadImage(self,imgUrl,userId):
        if imgUrl and userId:
            realUrl = "http:"+imgUrl
            file_name = u"%s.jpg" %userId
            path = os.path.join("C:\spider_file\\tbmm_pic",file_name)
            urllib.request.urlretrieve(realUrl, path)


