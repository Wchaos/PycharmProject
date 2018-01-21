import requests
import time
from selenium import webdriver

if __name__ == '__main__':
    browser = webdriver.Chrome()
    browser.set_window_size(1050, 840)
    # driver = webdriver.Chrome()
    # driver.maximize_window()

    url = 'https://www.qichacha.com/firm_3dd3f527dd7c3a81d73291eeb847aad1.html'
    cookie = 'UM_distinctid=160fd15721a9c9-071aff60ca647f-7b113d-1fa400-160fd15721bc1c; _uab_collina=151609163784756238080354; acw_tc=AQAAANwIZhO0pAMA01TheaMKJ/4EztGO; hasShow=1; zg_did=%7B%22did%22%3A%20%22160fd15722d136-0d486f5fca1888-7b113d-1fa400-160fd15722ea15%22%7D; CNZZDATA1254842228=918165069-1516073157-null%7C1516240667; _umdata=55F3A8BFC9C50DDA6D5B01D1A2C4BD594729A3C2F0A1F368B20B7C98FE1BB44573933CC5503128B8CD43AD3E795C914CDB578452826F1A2810689DF00059E9A6; zg_de1d1a35bfa24ce29bbf2c7eb17e6c4f=%7B%22sid%22%3A%201516244097614%2C%22updated%22%3A%201516245509558%2C%22info%22%3A%201516074529331%2C%22superProperty%22%3A%20%22%7B%7D%22%2C%22platform%22%3A%20%22%7B%7D%22%2C%22utm%22%3A%20%22%7B%7D%22%2C%22referrerDomain%22%3A%20%22%22%2C%22cuid%22%3A%20%22076ec19e42d4f48979bef4ad1a1450a5%22%7D; PHPSESSID=9s800680tofhjn2fdtfbjvr552'
    cookie = dict(elem.strip().split('=') for elem in cookie.split(';'))
    browser.get(url=url)
    time.sleep(3)
    print("get_cookies=======================")
    print(browser.get_cookies())
    browser.delete_all_cookies()
    dic = dict()

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






















    # headers = {
    #     "User-Agent": "Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/63.0.3239.108 Safari/537.36",
    #     "Cookie": cookie,
    #     # "Host": "www.qichacha.com",
    #     # "Referer": "http://www.qichacha.com/",
    #     # "Connection": "keep-alive",
    #     # "DNT": "1",
    #     # "Upgrade-Insecure-Requests": "1"
    # }
    # res = requests.get(url=url,headers=headers)
    # print(res.content.decode("utf-8"))




