from spider.onlinehtml import getdownhtml
from spider.offlinehtml import scrapynormal
from bs4 import BeautifulSoup



target='https://search.jd.com/Search?keyword=%E7%BE%8E%E7%99%BD%E9%9D%A2%E8%86%9C&enc=utf-8&qrst=1&rt=1&stop=1&vt=2&wq=%E7%BE%8E%E7%99%BD%E9%9D%A2%E8%86%9C&stock=1&page=3&s=56&click=0'


response=getdownhtml.delay(target)
responsetext=response.get()
print (responsetext)