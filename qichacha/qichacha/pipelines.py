# -*- coding: utf-8 -*-
import pymongo

from qichacha.items import BusinessInfoItem


class MongoDBPipleline(object):
    def __init__(self, database):
        self.BusinessInfoItem = database["BusinessInfoItem"]

    @classmethod
    def from_settings(cls, settings):
        '''1、@classmethod声明一个类方法，而对于平常我们见到的则叫做实例方法。
           2、类方法的第一个参数cls（class的缩写，指这个类本身），而实例方法的第一个参数是self，表示该类的一个实例
           3、可以通过类来调用，就像C.f()，相当于java中的静态方法'''

        host=settings['MONGO_HOST']  # 读取settings中的配置
        port=int(settings['MONGO_PORT'])
        dbname = settings['MONGO_DBNAME']

        print("==========")
        print(host,port,dbname)

        client = pymongo.MongoClient(host=host,port=port)  # **表示将字典扩展为关键字参数,相当于host=xxx,db=yyy....
        database = client[dbname]
        return cls(database)  # 相当于dbpool付给了这个类，self中可以得到


    def process_item(self, item, spider):
        """ 判断item的类型，并作相应的处理，再入数据库 """
        if isinstance(item, BusinessInfoItem):
            try:
                self.BusinessInfoItem.insert(dict(item))
            except Exception as e:
                print(e)
        return item

if __name__ == "__main__":
     item = BusinessInfoItem()
     item["company_name"] = "测试"
     mongo = MongoDBPipleline()
     mongo.BusinessInfoItem.insert(dict(item))