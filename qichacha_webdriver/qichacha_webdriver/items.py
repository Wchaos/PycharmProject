# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

from scrapy import Item, Field


class BusinessInfoItem(Item):
    _id = Field()  # 公司ID
    company_name = Field()  # 公司名称
    phone_num = Field()  # 电话
    official_web = Field()  # 官网
    email = Field()  # 邮箱
    address = Field()  # 地址
    legal_person = Field()  # 法人
    business_info = Field()  # 工商/登记信息（列表信息）



