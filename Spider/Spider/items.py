# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

import scrapy
class PipeItem(scrapy.Item):
    Item_Type  = scrapy.Field()
    Datagram = scrapy.Field()
    Usr_ID = scrapy.Field()
class UsrInfo(scrapy.Item):
    Usr_ID = scrapy.Field() #用户ID
    Usr_Info = scrapy.Field() #用户信息
    Num_Post = scrapy.Field() #发送微博数量
    Num_Follows = scrapy.Field() #关注者数
    Follows_List = scrapy.Field() #关注列表
    Num_Fans = scrapy.Field() #粉丝数
    Fans_List = scrapy.Field() #粉丝列表

class PostInfo(scrapy.Item):
    Post_Usr_ID = scrapy.Field() #发帖人
    Content = scrapy.Field() #内容
    Pic_Url = scrapy.Field() #图片链接
    TimeStamp = scrapy.Field() #时间
    Num_Likes = scrapy.Field() #点赞数
    Likes_List = scrapy.Field() #点赞列表
    Num_Trans = scrapy.Field() #转发数
    Trans_List = scrapy.Field() #转发用户列表

class PostComment(scrapy.Item):
    Usr_ID = scrapy.Field() #评论者ID
    Content = scrapy.Field() #评论内容
    Likes_Num = scrapy.Field() #点赞人数
    Pic_Url = scrapy.Field() #评论图片
    #以后添加 @相关的情况