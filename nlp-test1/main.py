from __future__ import division
import nltk
import urllib.request
from bs4 import BeautifulSoup

url = "http://news.bbc.co.uk/2/hi/health/2284783.stm"
html = urllib.request.urlopen(url).read()
# print(html[:60])
# print(html)
raw1 = BeautifulSoup(html,"lxml")
raw = raw1.get_text()
print(raw)

#from nltk import clean_html
# from bs4 import BeautifulSoup
# from BeautifulSoup import BeautifulStoneSoup
#
# raw = BeautifulSoup.get_text(html)
