from spider.onlinehtml import desilting
from spider.onlinehtml import seconddesilting
import time
import csv
import requests




csvfile=csv.reader(open('./text/024C.csv','r',encoding=' UTF-8-sig'))
for a in csvfile:
    id =a[0]
    name=a[1]
    url=a[2]
    if '.taobao.com' in url or '.tmall.com' in url or '.1688.com' in url:
        time.sleep(5)
    result = desilting.delay(url)
    desilt = result.get()
    if desilt['status']=='need':
        result1 = seconddesilting.delay(url)
        desilt1 = result1.get()
        print(str(a[0]) + '   ' + str(desilt1))
    else:
        print(str(a[0]) + '   ' + str(desilt))