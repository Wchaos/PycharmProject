import urllib.request

Cookie = "UM_distinctid=160fd15721a9c9-071aff60ca647f-7b113d-1fa400-160fd15721bc1c; _uab_collina=151609163784756238080354; acw_tc=AQAAANwIZhO0pAMA01TheaMKJ/4EztGO; hasShow=1; PHPSESSID=9s800680tofhjn2fdtfbjvr552; zg_did=%7B%22did%22%3A%20%22160fd15722d136-0d486f5fca1888-7b113d-1fa400-160fd15722ea15%22%7D; CNZZDATA1254842228=918165069-1516073157-null%7C1516240667; _umdata=55F3A8BFC9C50DDA6D5B01D1A2C4BD594729A3C2F0A1F368B20B7C98FE1BB44573933CC5503128B8CD43AD3E795C914CDB578452826F1A2810689DF00059E9A6; zg_de1d1a35bfa24ce29bbf2c7eb17e6c4f=%7B%22sid%22%3A%201516244097614%2C%22updated%22%3A%201516245509558%2C%22info%22%3A%201516074529331%2C%22superProperty%22%3A%20%22%7B%7D%22%2C%22platform%22%3A%20%22%7B%7D%22%2C%22utm%22%3A%20%22%7B%7D%22%2C%22referrerDomain%22%3A%20%22%22%2C%22cuid%22%3A%20%22076ec19e42d4f48979bef4ad1a1450a5%22%7D"

url = "http://www.qichacha.com/"

headers = {
    'User-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/62.0.3202.94 Safari/537.36',
    'Cookie': Cookie,
    'Connection': 'keep-alive',
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8',
    # 'Accept-Encoding': 'gzip, deflate',
    'Accept-Language': 'zh-CN,zh;q=0.9',
    'Host': 'www.qichacha.com',
    'Referer': 'http://www.qichacha.com/user_login'
}

req = urllib.request.Request(url=url, data=None, headers=headers)
response = urllib.request.urlopen(req)
the_page = response.read()
print(the_page.decode("utf8"))