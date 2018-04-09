
import pymongo
import requests
import time

from qichacha.settings import MONGO_HOST, MONGO_PORT, MONGO_DBNAME


client = pymongo.MongoClient(MONGO_HOST, int(MONGO_PORT))
db = client[MONGO_DBNAME]
collection = db['cookies_pool']

def get_cookie_from_mongodb():
    cookies = [data.get('cookie') for data in collection.find()]
    return cookies

def save_cookie_into_mongodb(account,cookie):
    print("insert")
    insert_data = {}
    insert_data['_id'] = account
    insert_data['cookie'] = cookie
    insert_data['insert_time'] = time.strftime('%Y-%m-%d %H:%M:%S')
    insert_data['insert_timestamp'] = time.time()
    collection.insert(insert_data)

def delete_cookie_by_acc(account):
    collection.delete_one({'_id': account})


account = "15050581283"
# cookie = "UM_distinctid=160fd15721a9c9-071aff60ca647f-7b113d-1fa400-160fd15721bc1c; _uab_collina=151609163784756238080354; acw_tc=AQAAANwIZhO0pAMA01TheaMKJ/4EztGO; hasShow=1; zg_did=%7B%22did%22%3A%20%22160fd15722d136-0d486f5fca1888-7b113d-1fa400-160fd15722ea15%22%7D; CNZZDATA1254842228=918165069-1516073157-null%7C1516240667; _umdata=55F3A8BFC9C50DDA6D5B01D1A2C4BD594729A3C2F0A1F368B20B7C98FE1BB44573933CC5503128B8CD43AD3E795C914CDB578452826F1A2810689DF00059E9A6; zg_de1d1a35bfa24ce29bbf2c7eb17e6c4f=%7B%22sid%22%3A%201516244097614%2C%22updated%22%3A%201516245509558%2C%22info%22%3A%201516074529331%2C%22superProperty%22%3A%20%22%7B%7D%22%2C%22platform%22%3A%20%22%7B%7D%22%2C%22utm%22%3A%20%22%7B%7D%22%2C%22referrerDomain%22%3A%20%22%22%2C%22cuid%22%3A%20%22076ec19e42d4f48979bef4ad1a1450a5%22%7D; PHPSESSID=9s800680tofhjn2fdtfbjvr552"
# cookie = "UM_distinctid=160e2d81c50990-02b5c26ad8127a-3c60460e-1fa400-160e2d81c519ff; zg_did=%7B%22did%22%3A%20%22160e2d81ca8a30-063c6b9592827f-3c60460e-1fa400-160e2d81ca989a%22%7D; _uab_collina=151563431335470821865698; PHPSESSID=qn1ke5nq0nv5fcegjltl7oi8i1; acw_tc=AQAAAHNYHSxr5gYAiVTheeshgZdyOOe+; hasShow=1; _umdata=6AF5B463492A874DE2AC1E797FCC27F90AFBA28B4D91C5BCA88672C32B307E8CD48E4705FB32E472CD43AD3E795C914C63CEDD25106C13EF09FD716D916572C6; CNZZDATA1254842228=1095774501-1515630171-https%253A%252F%252Fwww.baidu.com%252F%7C1516589397; acw_sc__=5a65602086ef556cd3c59065258a0309a69fdc43; zg_de1d1a35bfa24ce29bbf2c7eb17e6c4f=%7B%22sid%22%3A%201516593186885%2C%22updated%22%3A%201516593302954%2C%22info%22%3A%201516243108512%2C%22superProperty%22%3A%20%22%7B%7D%22%2C%22platform%22%3A%20%22%7B%7D%22%2C%22utm%22%3A%20%22%7B%7D%22%2C%22referrerDomain%22%3A%20%22www.qichacha.com%22%2C%22cuid%22%3A%20%221808beafd3fccded98b033ef2c545779%22%7D"
cookie = "UM_distinctid=160e2d81c50990-02b5c26ad8127a-3c60460e-1fa400-160e2d81c519ff; zg_did=%7B%22did%22%3A%20%22160e2d81ca8a30-063c6b9592827f-3c60460e-1fa400-160e2d81ca989a%22%7D; _uab_collina=151563431335470821865698; PHPSESSID=qn1ke5nq0nv5fcegjltl7oi8i1; acw_tc=AQAAAHNYHSxr5gYAiVTheeshgZdyOOe+; hasShow=1; _umdata=6AF5B463492A874DE2AC1E797FCC27F90AFBA28B4D91C5BCA88672C32B307E8CD48E4705FB32E472CD43AD3E795C914C63CEDD25106C13EF09FD716D916572C6; CNZZDATA1254842228=1095774501-1515630171-https%253A%252F%252Fwww.baidu.com%252F%7C1516589397; acw_sc__=5a65602086ef556cd3c59065258a0309a69fdc43; zg_de1d1a35bfa24ce29bbf2c7eb17e6c4f=%7B%22sid%22%3A%201516593186885%2C%22updated%22%3A%201516593578375%2C%22info%22%3A%201516243108512%2C%22superProperty%22%3A%20%22%7B%7D%22%2C%22platform%22%3A%20%22%7B%7D%22%2C%22utm%22%3A%20%22%7B%7D%22%2C%22referrerDomain%22%3A%20%22www.qichacha.com%22%2C%22cuid%22%3A%20%22e32a678ad71a4de858ed4639c6a3e2dc%22%7D"
if __name__ == "__main__":
    # save_cookie_into_mongodb(account,cookie)
    # delete_cookie_by_acc(account)
    print(get_cookie_from_mongodb())

















# proxies = {
#     # 'http': 'http://121.237.136.88:18183',
#     'https': 'http://121.237.136.88:18183'
# }
# headers = {
#     'user-agent': 'Mozilla/5.0 (Linux; Android 6.0; Nexus 5 Build/MRA58N) '
#                   'AppleWebKit/537.36 (KHTML, like Gecko) Chrome/61.0.3128.0 Mobile Safari/537.36'
# }
#
# url = 'https://www.baidu.com/'
# session = requests.Session()
# try:
#     # html = requests.get(url, headers=headers, timeout=30, proxies=proxies)
#     response = session.get(url=url,headers=headers,proxies=proxies)
#     print(response.content)
# except Exception as e:
#     print("网站打开失败！", e)







