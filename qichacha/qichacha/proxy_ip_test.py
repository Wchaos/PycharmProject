from urllib import request as request
import datetime
import os

ip_list_dir = "ip_list.txt"
avail_ips_dir = "avail_ips.txt"
f = open(ip_list_dir, encoding='UTF-8')
ips_file = open(avail_ips_dir, 'a', encoding='UTF-8')
headers = {
    'user-agent': 'Mozilla/5.0 (Linux; Android 6.0; Nexus 5 Build/MRA58N) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/61.0.3128.0 Mobile Safari/537.36'
}
begin_index = 115
for i in range(begin_index):
    line = f.readline()
index = begin_index
while 1:
    try:
        line = f.readline()
        if not line:
            break
    except Exception as e:
        print(e)
        break
    index = index+1
    print("line: ", index)
    if line[0] != "#":
        ary = line.split()
        ip = ary[0]
        ip_type = ary[1]
        print(ip_type)
        print(ip)
        # address = ary[2]
        print({ip_type: ip})
        httpproxy_handler = request.ProxyHandler({ip_type: ip})
        opener = request.build_opener(httpproxy_handler)
        req = request.Request("http://www.qichacha.com/firm_3dd3f527dd7c3a81d73291eeb847aad1.html", headers=headers)
        for j in range(3):
            try:
                start_time = datetime.datetime.now()  # 开始计时
                response = opener.open(req, timeout=10)
                response.read()
                print("proxy ip is available! ", ip)
                end_time = datetime.datetime.now()
                duration = (end_time-start_time).microseconds
                ips_file.write(ip+" "+ip_type+" "+str(duration)+" \n")
                ips_file.flush()
                break
            except Exception as e:
                print("网址打开失败", e)

f.close()
ips_file.close()


