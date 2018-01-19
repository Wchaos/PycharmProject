from urllib.request import urlretrieve as ult
import os

f = open("dev_urls.txt")
face_path = "face_image/train"
face_path_rect = "face_image_rect/train"
begin_index = 10587
for _ in range(begin_index):
    f.readline()
line = f.readline()
if not os.path.exists(face_path):
    os.makedirs(face_path)
for i in range(begin_index, 11000):
    print("line: ", i)
    if line[0] != "#":
        ary = line.split()
        url = ary[3]
        name = face_path + "/" + ary[0] + "_" + ary[1] + "_" + ary[2] + "."+url.split(".")[-1]
        if os.path.exists(name):
            print("file has existed")
            pass
        else:
            try:
                ult(url, name)
                print(name, "download success")
            except Exception as e:
                print('下载失败', e)
    line = f.readline()
f.close()
