from spider.offlinehtml import scrapyNormal
from spider.onlinehtml import getdownhtml
from process.searchonhtml import classify
import csv,re,time
from manualpreservation.taskconf import config
from celery import *

key = []
with open('./text/024fenlei.txt', 'r',encoding='utf-8') as b:
    line = b.readline()
    while line:
        line = re.sub('\n', '', line)
        key.append(line)
        line = b.readline()



csvfile=csv.reader(open('./text/024Calive.csv','r',encoding=' UTF-8-sig'))
for a in csvfile:
    id =a[0]
    name=a[1]
    url=a[2]
    time.sleep(5)
    response=getdownhtml.delay(url)
    responsetext=response.get()

    if type(responsetext) != dict:
        result = classify.delay(responsetext, key)
        classiftion = result.get()
        print (id+'----'+str(classiftion))



