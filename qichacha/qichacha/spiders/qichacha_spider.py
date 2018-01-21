import re
import urllib

from scrapy import Selector, Request
from scrapy.spiders import CrawlSpider
from bs4 import BeautifulSoup

from qichacha.items import BusinessInfoItem


class Spider(CrawlSpider):
    name = "qichacha"
    allowed_domains = ["qichacha.com"]
    host = "http://www.qichacha.com"
    start_urls = ["http://www.qichacha.com"]
    # start_url = "https://www.qichacha.com/gongsi_area.shtml"
    # prov_list = ['AH', 'BJ', 'CQ', 'FJ', 'GS', 'GD', 'GX', 'GZ', 'HAIN', 'HB', 'HLJ', 'HEN', 'HUB', 'HUN',\
    #              'JS', 'JX', 'JL', 'LN', 'NMG', 'NX', 'QH', 'SD', 'SH', 'SX', 'SAX', 'SC', 'TJ', 'XJ',\
    #              'XZ', 'YN', 'ZJ']
    #
    # def start_requests(self):
    #     for prov in self.prov_list:
    #         for page in range(1, 501):
    #             query_url = self.start_url + "?prov=" + prov + "&p=" + str(page)
    #             yield Request(url=query_url,callback=self.parse2)


    def parse(self, response):
        selector = Selector(response)
        area_list =selector.xpath('//div[@class="tab-pane fade" and @id="area"]/ul//li/a/@href').extract()
        for area_url in area_list:
            area_url = self.host + area_url
            yield Request(url= area_url,callback=self.parse2)
        # yield Request(url=self.host+area_list[0], callback=self.parse2)

    def parse2(self, response):
        selector = Selector(response)
        company_list = selector.xpath('//div[@class="col-md-12"]// section[@class="panel panel-default" and @id="searchlist"]/a/@href').extract()
        for company_url in company_list:
            company_url = self.host + company_url
            yield Request(url= company_url,callback= self.parse3)
        # yield Request(url=self.host+company_list[0], callback=self.parse3)

    def parse3(self,response):
        """抓取公司名称、地址等基本属性信息"""
        businessInfoItem = BusinessInfoItem()
        selector = Selector(response)
        cret_url = selector.xpath('//div[@class="logo"]/div[@class="m-t-sm"]/a[@class="c-renling"]/@href').extract_first()
        # company_name = selector.xpath('//div[@class="content"]/div[@class="row title"]/text()').extract_first()
        phone_num = selector.xpath('//div[@class="content"]/div[2]/span[@class= "cvlu"]/span/text()').extract_first()
        official_web = selector.xpath('//div[@class="content"]/div[3]/span[2]/a/text()').extract_first()
        email = selector.xpath('//div[@class="content"]/div[3]/span[4]/a/text()').extract_first()
        address = selector.xpath('//div[@class="content"]/div[4]/span[@class= "cvlu"]/a[@id= "mapPreview"]/text()').extract_first()

        businessInfoItem["phone_num"] = phone_num
        businessInfoItem["official_web"] = official_web
        businessInfoItem["email"] = email
        businessInfoItem["address"] = address
        if cret_url:
            _id = re.findall(r'companykey=(.*?)&',cret_url)[0]
            company_name = re.findall(r'companyname=(\S*)',cret_url)[0]
            if _id and company_name:
                businessInfoItem["_id"] = _id
                businessInfoItem["company_name"] = company_name

                name = urllib.parse.quote(company_name)
                print(company_name)
                base_url = self.host + "/company_getinfos?unique="+ _id + "&companyname="+name+"&tab=base"
                print(base_url)
                yield Request(url=base_url , meta={"item": businessInfoItem}, callback=self.parse_base)


    def parse_base(self, response):
        """抓取基本信息中的工商信息表格"""
        businessInfoItem = response.meta["item"]
        selector = Selector(response)
        legal_person = selector.xpath('//div[@class="boss-td"]/div//div/a[@class="bname"]/text()').extract_first()
        print("========")
        print(legal_person)
        table = selector.xpath('//table[@class="m_changeList"]').extract()[1]
        soup =BeautifulSoup(table,"lxml")
        registered_capital = soup.find_all('tr')[0].find_all('td')[1].get_text()
        established_date = soup.find_all('tr')[0].find_all('td')[3].get_text()

        manage_state = soup.find_all('tr')[1].find_all('td')[1].get_text()
        social_credit_code = soup.find_all('tr')[1].find_all('td')[3].get_text()

        taxpayer_identity_num = soup.find_all('tr')[2].find_all('td')[1].get_text()
        register_num = soup.find_all('tr')[2].find_all('td')[3].get_text()

        organization_code = soup.find_all('tr')[3].find_all('td')[1].get_text()
        company_type = soup.find_all('tr')[3].find_all('td')[3].get_text()

        staff_size = soup.find_all('tr')[4].find_all('td')[1].get_text()
        term_of_validity = soup.find_all('tr')[4].find_all('td')[3].get_text()

        register_institution = soup.find_all('tr')[5].find_all('td')[1].get_text()
        approved_date = soup.find_all('tr')[5].find_all('td')[3].get_text()

        company_eng_name = soup.find_all('tr')[6].find_all('td')[1].get_text()
        name_used_before = soup.find_all('tr')[6].find_all('td')[3].get_text()

        sup_province = soup.find_all('tr')[7].find_all('td')[1].get_text()
        sup_industry = soup.find_all('tr')[7].find_all('td')[3].get_text()
        business_scope = soup.find_all('tr')[9].find_all('td')[1].get_text()

        businessInfoItem["legal_person"] = legal_person
        businessInfoItem["registered_capital"] = registered_capital
        businessInfoItem["established_date"] = established_date
        businessInfoItem["manage_state"] = manage_state
        businessInfoItem["social_credit_code"] = social_credit_code
        businessInfoItem["taxpayer_identity_num"] = taxpayer_identity_num
        businessInfoItem["register_num"] = register_num
        businessInfoItem["organization_code"] = organization_code
        businessInfoItem["company_type"] = company_type
        businessInfoItem["staff_size"] = staff_size
        businessInfoItem["term_of_validity"] = term_of_validity
        businessInfoItem["register_institution"] = register_institution
        businessInfoItem["approved_date"] = approved_date
        businessInfoItem["company_eng_name"] = company_eng_name
        businessInfoItem["name_used_before"] = name_used_before
        businessInfoItem["sup_province"] = sup_province
        businessInfoItem["sup_industry"] = sup_industry
        businessInfoItem["business_scope"] = business_scope

        yield businessInfoItem
        print(businessInfoItem)





