#coding: utf-8
import os
import urllib

number = 0

def download(url):
                global number
                number += 1
                savePath = '/Users/Apple/Pictures/girls/%d.jpg' % (number)
                if(os.path.exists(savePath) == False):
                        print('正在下载...',url)
                        try:
                                u = urllib.requert.urlopen(url)
                                r = u.read()
                                downloadFile = open(savePath,'wb')
                                downloadFile.write(r)
                                u.close()
                                downloadFile.close()
                        except:
                                print(savePath,'can not download.')
                        
                        
for line in  open("grils"):
    download(line)
