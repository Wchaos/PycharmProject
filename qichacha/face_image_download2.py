from urllib.request import urlretrieve as ult
import os

f = open("dev_urls.txt")
face_path = "face_image/train"
face_path_rect = "face_image_rect/train"
line_list = []
if not os.path.exists(face_path):
    os.makedirs(face_path)
while 1:
    line = f.readline()
    if not line:
        break
    line_list.append(line)
for i in range(9285,10000):
    try:
        line = line_list[i]
        print("line: ", i)
        if line[0] != "#":
            ary = line.split()
            url = ary[3]
            name = face_path + "/" + ary[0] + "_" + ary[1] + "_" + ary[2] + "." + url.split(".")[-1]
            if os.path.exists(name):
                print("file has existed")
                pass
            else:
                try:
                    ult(url, name)
                    print(name, "download success")
                except Exception as e:
                    print('下载失败', e)
                    pass
    except Exception as e:
        print("=====Exception======")
        print(e)
        pass

f.close()
