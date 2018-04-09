# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

from scrapy import Item, Field


class BusinessInfoItem(Item):
    _id = Field() #公司ID
    company_name = Field() #公司名称
    phone_num = Field() #电话
    official_web = Field() #官网
    email = Field() #邮箱
    address = Field() #地址
    legal_person = Field() #法人
    business_info = Field() #工商/登记信息
    # registered_capital = Field() #注册资本
    # established_date = Field() #成立日期
    # manage_state = Field() #经营状态
    # social_credit_code = Field() #统一社会信用代码
    # taxpayer_identity_num = Field() #纳税人识别号
    # register_num = Field() #注册号
    # organization_code = Field() #组织结构代码
    # company_type = Field() #公司类型
    # staff_size = Field() #人员规模
    # term_of_validity = Field() #营业期限
    # register_institution = Field() #登记机关
    # approved_date = Field() #核准日期
    # company_eng_name = Field() #英文名
    # name_used_before = Field() #曾用名
    # sup_province = Field() #所属地区
    # sup_industry = Field() #所属行业
    # business_scope = Field() #经营范围

