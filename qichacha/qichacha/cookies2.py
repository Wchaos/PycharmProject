import json

import requests
import time

from bs4 import BeautifulSoup
from scrapy import Selector
from scrapy.http import HtmlResponse
from selenium import webdriver

cookie1 = "UM_distinctid=160fd15721a9c9-071aff60ca647f-7b113d-1fa400-160fd15721bc1c; _uab_collina=151609163784756238080354; acw_tc=AQAAANwIZhO0pAMA01TheaMKJ/4EztGO; hasShow=1; zg_did=%7B%22did%22%3A%20%22160fd15722d136-0d486f5fca1888-7b113d-1fa400-160fd15722ea15%22%7D; CNZZDATA1254842228=918165069-1516073157-null%7C1516240667; _umdata=55F3A8BFC9C50DDA6D5B01D1A2C4BD594729A3C2F0A1F368B20B7C98FE1BB44573933CC5503128B8CD43AD3E795C914CDB578452826F1A2810689DF00059E9A6; zg_de1d1a35bfa24ce29bbf2c7eb17e6c4f=%7B%22sid%22%3A%201516244097614%2C%22updated%22%3A%201516245509558%2C%22info%22%3A%201516074529331%2C%22superProperty%22%3A%20%22%7B%7D%22%2C%22platform%22%3A%20%22%7B%7D%22%2C%22utm%22%3A%20%22%7B%7D%22%2C%22referrerDomain%22%3A%20%22%22%2C%22cuid%22%3A%20%22076ec19e42d4f48979bef4ad1a1450a5%22%7D; PHPSESSID=9s800680tofhjn2fdtfbjvr552"
cookie2 = "UM_distinctid=160e2d81c50990-02b5c26ad8127a-3c60460e-1fa400-160e2d81c519ff; zg_did=%7B%22did%22%3A%20%22160e2d81ca8a30-063c6b9592827f-3c60460e-1fa400-160e2d81ca989a%22%7D; _uab_collina=151563431335470821865698; PHPSESSID=qn1ke5nq0nv5fcegjltl7oi8i1; acw_tc=AQAAAHNYHSxr5gYAiVTheeshgZdyOOe+; hasShow=1; _umdata=6AF5B463492A874DE2AC1E797FCC27F90AFBA28B4D91C5BCA88672C32B307E8CD48E4705FB32E472CD43AD3E795C914C63CEDD25106C13EF09FD716D916572C6; CNZZDATA1254842228=1095774501-1515630171-https%253A%252F%252Fwww.baidu.com%252F%7C1516589397; acw_sc__=5a65602086ef556cd3c59065258a0309a69fdc43; zg_de1d1a35bfa24ce29bbf2c7eb17e6c4f=%7B%22sid%22%3A%201516593186885%2C%22updated%22%3A%201516593302954%2C%22info%22%3A%201516243108512%2C%22superProperty%22%3A%20%22%7B%7D%22%2C%22platform%22%3A%20%22%7B%7D%22%2C%22utm%22%3A%20%22%7B%7D%22%2C%22referrerDomain%22%3A%20%22www.qichacha.com%22%2C%22cuid%22%3A%20%221808beafd3fccded98b033ef2c545779%22%7D"
cookie3 = "UM_distinctid=160e2d81c50990-02b5c26ad8127a-3c60460e-1fa400-160e2d81c519ff; zg_did=%7B%22did%22%3A%20%22160e2d81ca8a30-063c6b9592827f-3c60460e-1fa400-160e2d81ca989a%22%7D; _uab_collina=151563431335470821865698; PHPSESSID=qn1ke5nq0nv5fcegjltl7oi8i1; acw_tc=AQAAAHNYHSxr5gYAiVTheeshgZdyOOe+; hasShow=1; _umdata=6AF5B463492A874DE2AC1E797FCC27F90AFBA28B4D91C5BCA88672C32B307E8CD48E4705FB32E472CD43AD3E795C914C63CEDD25106C13EF09FD716D916572C6; CNZZDATA1254842228=1095774501-1515630171-https%253A%252F%252Fwww.baidu.com%252F%7C1516589397; acw_sc__=5a65602086ef556cd3c59065258a0309a69fdc43; zg_de1d1a35bfa24ce29bbf2c7eb17e6c4f=%7B%22sid%22%3A%201516593186885%2C%22updated%22%3A%201516593578375%2C%22info%22%3A%201516243108512%2C%22superProperty%22%3A%20%22%7B%7D%22%2C%22platform%22%3A%20%22%7B%7D%22%2C%22utm%22%3A%20%22%7B%7D%22%2C%22referrerDomain%22%3A%20%22www.qichacha.com%22%2C%22cuid%22%3A%20%22e32a678ad71a4de858ed4639c6a3e2dc%22%7D"

cookie4 = "UM_distinctid=160e2d81c50990-02b5c26ad8127a-3c60460e-1fa400-160e2d81c519ff; zg_did=%7B%22did%22%3A%20%22160e2d81ca8a30-063c6b9592827f-3c60460e-1fa400-160e2d81ca989a%22%7D; _uab_collina=151563431335470821865698; PHPSESSID=qn1ke5nq0nv5fcegjltl7oi8i1; acw_tc=AQAAAIiELzGizAAAwVThedNluMUMTm5P; hasShow=1; _umdata=6AF5B463492A874DE2AC1E797FCC27F90AFBA28B4D91C5BCA88672C32B307E8CD48E4705FB32E472CD43AD3E795C914C02936B82A50B993778445F2FDDECFC10; zg_de1d1a35bfa24ce29bbf2c7eb17e6c4f=%7B%22sid%22%3A%201516675757923%2C%22updated%22%3A%201516675757925%2C%22info%22%3A%201516243108512%2C%22superProperty%22%3A%20%22%7B%7D%22%2C%22platform%22%3A%20%22%7B%7D%22%2C%22utm%22%3A%20%22%7B%7D%22%2C%22referrerDomain%22%3A%20%22www.qichacha.com%22%2C%22cuid%22%3A%20%221808beafd3fccded98b033ef2c545779%22%7D; CNZZDATA1254842228=1095774501-1515630171-https%253A%252F%252Fwww.baidu.com%252F%7C1516672569"
cookie5 = "UM_distinctid=160e2d81c50990-02b5c26ad8127a-3c60460e-1fa400-160e2d81c519ff; zg_did=%7B%22did%22%3A%20%22160e2d81ca8a30-063c6b9592827f-3c60460e-1fa400-160e2d81ca989a%22%7D; _uab_collina=151563431335470821865698; PHPSESSID=qn1ke5nq0nv5fcegjltl7oi8i1; acw_tc=AQAAAIiELzGizAAAwVThedNluMUMTm5P; hasShow=1; _umdata=6AF5B463492A874DE2AC1E797FCC27F90AFBA28B4D91C5BCA88672C32B307E8CD48E4705FB32E472CD43AD3E795C914C02936B82A50B993778445F2FDDECFC10; CNZZDATA1254842228=1095774501-1515630171-https%253A%252F%252Fwww.baidu.com%252F%7C1516672569; zg_de1d1a35bfa24ce29bbf2c7eb17e6c4f=%7B%22sid%22%3A%201516675757923%2C%22updated%22%3A%201516677932888%2C%22info%22%3A%201516243108512%2C%22superProperty%22%3A%20%22%7B%7D%22%2C%22platform%22%3A%20%22%7B%7D%22%2C%22utm%22%3A%20%22%7B%7D%22%2C%22referrerDomain%22%3A%20%22www.qichacha.com%22%2C%22cuid%22%3A%20%22e32a678ad71a4de858ed4639c6a3e2dc%22%7D"

cookie6 = "acw_tc=AQAAAPJvDBvZTQAAiVTheVLX32iSxPtY; UM_distinctid=1611bb9bbd352a-02733741f0e779-75173c42-1fa400-1611bb9bbd4a11; _uab_collina=151659313712339102345809; PHPSESSID=im6ark3qg4jff2gb20aqu55ot5; zg_did=%7B%22did%22%3A%20%221611bb9bc01100-0fea0a24fb01ee-75173c42-1fa400-1611bb9bc05ef%22%7D; CNZZDATA1254842228=1122088146-1516584510-https%253A%252F%252Fwww.baidu.com%252F%7C1516677972; hasShow=1; _umdata=55F3A8BFC9C50DDA08D80CAC1D80C31E078E97414F872D2D41C792FF6E6F17F146D3E291CDCEA200CD43AD3E795C914C12DDA337D13C4972ABDADF648C59E35F; zg_de1d1a35bfa24ce29bbf2c7eb17e6c4f=%7B%22sid%22%3A%201516678844379%2C%22updated%22%3A%201516678870462%2C%22info%22%3A%201516588612621%2C%22superProperty%22%3A%20%22%7B%7D%22%2C%22platform%22%3A%20%22%7B%7D%22%2C%22utm%22%3A%20%22%7B%7D%22%2C%22referrerDomain%22%3A%20%22www.baidu.com%22%2C%22cuid%22%3A%20%22e32a678ad71a4de858ed4639c6a3e2dc%22%7D"
cookie7 = "acw_tc=AQAAAPJvDBvZTQAAiVTheVLX32iSxPtY; UM_distinctid=1611bb9bbd352a-02733741f0e779-75173c42-1fa400-1611bb9bbd4a11; _uab_collina=151659313712339102345809; PHPSESSID=im6ark3qg4jff2gb20aqu55ot5; zg_did=%7B%22did%22%3A%20%221611bb9bc01100-0fea0a24fb01ee-75173c42-1fa400-1611bb9bc05ef%22%7D; hasShow=1; _umdata=55F3A8BFC9C50DDA08D80CAC1D80C31E078E97414F872D2D41C792FF6E6F17F146D3E291CDCEA200CD43AD3E795C914C12DDA337D13C4972ABDADF648C59E35F; CNZZDATA1254842228=1122088146-1516584510-https%253A%252F%252Fwww.baidu.com%252F%7C1516689502; zg_de1d1a35bfa24ce29bbf2c7eb17e6c4f=%7B%22sid%22%3A%201516692040320%2C%22updated%22%3A%201516692067143%2C%22info%22%3A%201516588612621%2C%22superProperty%22%3A%20%22%7B%7D%22%2C%22platform%22%3A%20%22%7B%7D%22%2C%22utm%22%3A%20%22%7B%7D%22%2C%22referrerDomain%22%3A%20%22www.baidu.com%22%2C%22cuid%22%3A%20%221808beafd3fccded98b033ef2c545779%22%7D"

cookie8 = "UM_distinctid=160e2d81c50990-02b5c26ad8127a-3c60460e-1fa400-160e2d81c519ff; zg_did=%7B%22did%22%3A%20%22160e2d81ca8a30-063c6b9592827f-3c60460e-1fa400-160e2d81ca989a%22%7D; _uab_collina=151563431335470821865698; PHPSESSID=qn1ke5nq0nv5fcegjltl7oi8i1; acw_tc=AQAAAIiELzGizAAAwVThedNluMUMTm5P; hasShow=1; _umdata=6AF5B463492A874DE2AC1E797FCC27F90AFBA28B4D91C5BCA88672C32B307E8CD48E4705FB32E472CD43AD3E795C914C02936B82A50B993778445F2FDDECFC10; zg_de1d1a35bfa24ce29bbf2c7eb17e6c4f=%7B%22sid%22%3A%201516693249899%2C%22updated%22%3A%201516693249901%2C%22info%22%3A%201516243108512%2C%22superProperty%22%3A%20%22%7B%7D%22%2C%22platform%22%3A%20%22%7B%7D%22%2C%22utm%22%3A%20%22%7B%7D%22%2C%22referrerDomain%22%3A%20%22www.qichacha.com%22%2C%22cuid%22%3A%20%22e32a678ad71a4de858ed4639c6a3e2dc%22%7D; CNZZDATA1254842228=1095774501-1515630171-https%253A%252F%252Fwww.baidu.com%252F%7C1516688067"
def test_cookie1(cookie):

    headers = {
        'Accept': 'text / html, application / xhtml + xml, application / xml;\
                  q = 0.9, image / webp, image / apng, * / *;q = 0.8',
        'Accept - Encoding': 'gzip, deflate',
        'Accept - Language': 'zh - CN, zh;q = 0.9',
        'Cache - Control': 'max - age = 0',
        'Connection': 'keep - alive',
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/63.0.3239.108 Safari/537.36',
        'Cookie': cookie,
    }
    url = 'https://www.qichacha.com/firm_3dd3f527dd7c3a81d73291eeb847aad1.html'
    response = requests.get(url=url, headers=headers)
    print(response.content.decode("utf-8"))

def test_cookie2(cookie):
    browser = webdriver.Chrome()
    browser.set_window_size(1050, 840)
    # driver = webdriver.Chrome()
    # driver.maximize_window()

    url = 'https://www.qichacha.com/firm_3dd3f527dd7c3a81d73291eeb847aad1.html'
    cookie = dict(elem.strip().split('=') for elem in cookie.split(';'))
    browser.get(url=url)
    time.sleep(2)
    browser.delete_all_cookies()
    for key, value in cookie.items():
        dic = {
            'domain': 'www.qichacha.com',
            'name': str(key),
            'value': str(value),
            'path': '/',
            'secure': True,
        }
        browser.add_cookie(dic)
    browser.get(url=url)
    time.sleep(2)
    res = browser.page_source
    print(res)

def cmp_cookie(cookie_one,cookie_two):
    cookie_one = dict(elem.strip().split('=') for elem in cookie_one.split(';'))
    cookie_two = dict(elem.strip().split('=') for elem in cookie_two.split(';'))
    key1s = set(cookie_one.keys())
    key2s = set(cookie_two.keys())
    for key in key1s | key2s:
        if key in key1s:
            result1 = cookie_one[key]
        else:
            result1 = "none"
        print(key + " : " + result1 )
        if key in key2s:
            result2 = cookie_two[key]
        else:
            result2 = "none"
        print(key + " : " + result2)
        if result1 != result2:
            print("different")
        print("==============")






if __name__ == '__main__':
    # test_cookie1(cookie7)
    test_cookie2(cookie8)
    # cmp_cookie(cookie7,cookie8)



















    # chromeOptions = webdriver.ChromeOptions();
    # # 设置为 headless 模式 （必须）
    # chromeOptions.add_argument("--headless");
    # # 设置浏览器窗口打开大小  （非必须）
    # chromeOptions.add_argument("--window-size=1920,1080")
    # browser = webdriver.Chrome(chrome_options=chromeOptions)
    # browser.get("http://www.baidu.com")
    # title = browser.title
    # print(title)
    # browser.close()




