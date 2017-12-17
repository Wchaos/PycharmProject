# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

from scrapy import Item, Field


class tbModelItem(Item):
    avatarUrl = Field()
    cardUrl = Field()
    city = Field()
    height = Field()
    identityUrl = Field()
    modelUrl = Field()
    realName = Field()
    totalFanNum = Field()
    totalFavorNum = Field()
    userId = Field()
    viewFlag = Field()
    weight = Field()


