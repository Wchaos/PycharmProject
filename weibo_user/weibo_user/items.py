# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

import scrapy
from scrapy.item import Item, Field


class InformationItem(Item):
    #关注对象的相关个人信息
    _id = Field()  # 用户ID
    Info = Field() # 用户基本信息
    Num_Tweets = Field()  # 微博数
    Num_Follows = Field()  # 关注数
    Num_Fans = Field()  # 粉丝数
    HomePage = Field() #关注者的主页

class TweetsItem(Item):
    #微博内容的相关信息
    _id = Field()  # 用户ID
    Content = Field()  # 微博内容
    Time_Location = Field()  # 时间地点
    Pic_Url = Field()  # 原图链接
    Like = Field()  # 点赞数
    Transfer = Field()  # 转载数
    Comment = Field()  # 评论数

