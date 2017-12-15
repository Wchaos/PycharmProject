# coding=utf-8
from scrapy.spider import Spider
from scrapy.http import Request
from scrapy.selector import Selector
from weibo_user.items import InformationItem, TweetsItem
import re
import requests
from bs4 import BeautifulSoup


class Weibo(Spider):
    name = "weibospider"
    redis_key = 'weibospider:start_urls'
    # 可以从多个用户的关注列表中获取这些用户的关注对象信息和关注对象的微博信息
    start_urls = ['http://weibo.cn/0123456789/follow', 'http://weibo.cn/0123456789/follow']
    # 如果通过用户的分组获取关注列表进行抓取数据，需要调整parse中如id和nextlink的多个参数
    # strat_urls = ['http://weibo.cn/attgroup/show?cat=user¤tPage=2&rl=3&next_cursor=20&previous_cursor=10&type=opening&uid=1771329897&gid=201104290187632788&page=1']
    url = 'http://weibo.cn'
    # group_url = 'http://weibo.cn/attgroup/show'
    # 把已经获取过的用户ID提前加入Follow_ID中避免重复抓取
    Follow_ID = ['0123456789']
    TweetsID = []

    def parse(self, response):
        # 用户关注者信息
        informationItems = InformationItem()
        selector = Selector(response)

        print(selector)
        Followlist = selector.xpath('//tr/td[2]/a[2]/@href').extract()
        print("输出关注人ID信息")
        print(len(Followlist))

        for each in Followlist:
            # 选取href字符串中的id信息
            followId = each[(each.index("uid") + 4):(each.index("rl") - 1)]
            print(followId)
            follow_url = "http://weibo.cn/%s" % followId
            # 通过筛选条件获取需要的微博信息,此处为筛选原创带图的微博
            needed_url = "http://weibo.cn/%s/profile?hasori=1&haspic=1&endtime=20160822&advancedfilter=1&page=1" % followId
            print(follow_url)
            print(needed_url)
            # 抓取过数据的用户不再抓取：
            while followId not in self.Follow_ID:
                yield Request(url=follow_url, meta={"item": informationItems, "ID": followId, "URL": follow_url},
                              callback=self.parse1)
                yield Request(url=needed_url, callback=self.parse2)
                self.Follow_ID.append(followId)

        nextLink = selector.xpath('//div[@class="pa"]/form/div/a/@href').extract()
        # 查找下一页，有则循环
        if nextLink:
            nextLink = nextLink[0]
            print(nextLink)
            yield Request(self.url + nextLink, callback=self.parse)
        else:
            # 没有下一页即获取完关注人列表之后输出列表的全部ID
            print(self.Follow_ID)
            # yield informationItems

    def parse1(self, response):
        """ 通过ID访问关注者信息 """
        # 通过meta把parse中的对象变量传递过来
        informationItems = response.meta["item"]
        informationItems['_id'] = response.meta["ID"]
        informationItems['HomePage'] = response.meta["URL"]
        selector = Selector(response)
        # info = ";".join(selector.xpath('//div[@class="ut"]/text()').extract())  # 获取标签里的所有text()
        info = selector.xpath('//div[@class="ut"]/span[@class="ctt"]/text()').extract()
        # 用/分开把列表中的各个元素便于区别不同的信息
        allinfo = '  /  '.join(info)
        try:
            # exceptions.TypeError: expected string or buffer
            informationItems['Info'] = allinfo
        except:
            pass
            # text2 = selector.xpath('body/div[@class="u"]/div[@class="tip2"]').extract()
        num_tweets = selector.xpath('body/div[@class="u"]/div[@class="tip2"]/span/text()').extract()  # 微博数
        num_follows = selector.xpath('body/div[@class="u"]/div[@class="tip2"]/a[1]/text()').extract()  # 关注数
        num_fans = selector.xpath('body/div[@class="u"]/div[@class="tip2"]/a[2]/text()').extract()  # 粉丝数
        # 选取'[' ']'之间的内容
        if num_tweets:
            informationItems["Num_Tweets"] = (num_tweets[0])[
                                             ((num_tweets[0]).index("[") + 1):((num_tweets[0]).index("]"))]
        if num_follows:
            informationItems["Num_Follows"] = (num_follows[0])[
                                              ((num_follows[0]).index("[") + 1):((num_follows[0]).index("]"))]
        if num_fans:
            informationItems["Num_Fans"] = (num_fans[0])[((num_fans[0]).index("[") + 1):((num_fans[0]).index("]"))]

        yield informationItems

        # 获取关注人的微博内容相关信息

    def parse2(self, response):

        selector = Selector(response)
        tweetitems = TweetsItem()
        # 可以直接用request的meta传递ID过来更方便
        IDhref = selector.xpath('//div[@class="u"]/div[@class="tip2"]/a[1]/@href').extract()
        ID = (IDhref[0])[1:11]
        Tweets = selector.xpath('//div[@class="c"]')

        # 跟parse1稍有不同，通过for循环寻找需要的对象
        for eachtweet in Tweets:
            # 获取每条微博唯一id标识
            mark_id = eachtweet.xpath('@id').extract()
            print(mark_id)
            # 当id不为空的时候加入到微博获取列表
            if mark_id:
                # 去重操作，对于已经获取过的微博不再获取
                while mark_id not in self.TweetsID:
                    content = eachtweet.xpath('div/span[@class="ctt"]/text()').extract()
                    timelocation = eachtweet.xpath('div[2]/span[@class="ct"]/text()').extract()
                    pic_url = eachtweet.xpath('div[2]/a[2]/@href').extract()
                    like = eachtweet.xpath('div[2]/a[3]/text()').extract()
                    transfer = eachtweet.xpath('div[2]/a[4]/text()').extract()
                    comment = eachtweet.xpath('div[2]/a[5]/text()').extract()

                    tweetitems['_id'] = ID
                    # 把列表元素连接且转存成字符串
                    allcontents = ''.join(content)
                    # 内容可能为空 需要先判定
                    if allcontents:
                        tweetitems['Content'] = allcontents
                    else:
                        pass
                    if timelocation:
                        tweetitems['Time_Location'] = timelocation[0]
                    if pic_url:
                        tweetitems['Pic_Url'] = pic_url[0]
                        # 返回字符串中'[' ']'里的内容
                    if like:
                        tweetitems['Like'] = (like[0])[((like[0]).index("[") + 1):((like[0]).index("]"))]
                    if transfer:
                        tweetitems['Transfer'] = (transfer[0])[
                                                 ((transfer[0]).index("[") + 1):((transfer[0]).index("]"))]
                    if comment:
                        tweetitems['Comment'] = (comment[0])[((comment[0]).index("[") + 1):((comment[0]).index("]"))]
                        # 把已经抓取过的微博id存入列表
                    self.TweetsID.append(mark_id)
                    yield tweetitems
            else:
                # 如果selector语句找不到id 查看当前查询语句的状态
                print(eachtweet)

        tweet_nextLink = selector.xpath('//div[@class="pa"]/form/div/a/@href').extract()
        if tweet_nextLink:
            tweet_nextLink = tweet_nextLink[0]
            print(tweet_nextLink)
            yield Request(self.url + tweet_nextLink, callback=self.parse2)