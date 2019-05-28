from spider.onlinehtml import desilting
import csv




csvfile=csv.reader(open('./text/024.csv','r',encoding=' UTF-8-sig'))
for a in csvfile:
    result=desilting.delay(a[2])
    desilt=result.get()
    print (str(a[0])+'   '+str(desilt))
