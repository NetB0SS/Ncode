from __future__ import absolute_import, unicode_literals
from celery import Celery,Task
import time,json,re,os,csv
from bs4 import BeautifulSoup





'''
============================================================================================
'''

app=Celery('process')
app.config_from_object('celeryconfig')

class DebugTask(Task):

    def __call__(self, *args, **kwargs):
        # print('TASK STARTING: {0.name}[{0.request.id}]'.format(self))
        return super(DebugTask, self).__call__(*args, **kwargs)


app.Task = DebugTask


'''
============================================================================================
'''

'''

处理文件相关的

'''


@app.task(name='process.dealfile.readelejson',queue='readelejson')
def readelejson(filepath):
    resultreturn=[]
    openfile=open(filepath,'r',encoding='utf-8')
    data = openfile.readlines()
    for a in data:
        eachline=json.loads(a)
        for b in eachline:
            name = b['name']
            id_history = (b['id'])
            address = (b['address'])
            phone = (b['phone'])
            flavors = (b['flavors'])
            latitude = b['latitude']
            longitude = b['longitude']
            url='https://www.ele.me/shop/'+id_history

            resultjson={'name':name,'id_history':id_history,'address':address,'phone':phone,'flavors':flavors,'latitude':latitude,'longitude':longitude,'url':url}
            # print(resultjson)
            resultreturn.append(resultjson)

    return resultreturn

@app.task(name='process.dealfile.readxingxuanjson',queue='readxingxuanjson')
def readxingxuanjson(filepath):
    resultreturn = []
    openfile = open(filepath, 'r', encoding='utf-8')
    data = openfile.readlines()
    for a in data:
        eachline=json.loads(a)
        # print(eachline)
        result=eachline['result']
        shopinfo=result['shop_info']
        for b in shopinfo:
            name=(b['shop_name'])
            id=b['release_id']
            latitude = b['shop_lat']
            longitude = b['shop_lng']
            url='https://star.ele.me/waimai/shop/'+id
            resultjson={'name':name,'id':id,'latitude':latitude,'longitude':longitude,'url':url}
            # print(resultjson)
            resultreturn.append(resultjson)

    return resultreturn

@app.task(name='process.dealfile.readmeituanjson',queue='readmeituanjson')
def readmeituanjson(filepath):
    resultreturn = []
    openfile = open(filepath, 'r', encoding='utf-8')
    data = openfile.readlines()
    for a in data:
        eachline = json.loads(a)
        # print(eachline)
        result = eachline['data']
        shopinfo = result['shopList']

        for b in shopinfo:
            name = (b['shopName'])
            id = b['mtWmPoiId']
            # latitude = b['shop_lat']
            # longitude = b['shop_lng']
            url = 'http://h5.waimai.meituan.com/waimai/mindex/menu?mtShopId=' + id
            address = b['address']
            resultjson = {'name': name, 'id': id, 'url': url,'address':address}
            # print(resultjson)
            resultreturn.append(resultjson)

    return resultreturn



@app.task(name='process.dealfile.readtmallhtml',queue='readtmallhtml')
def readtmallhtml(htmlread):
    '''
    对于天猫的搜索页|店铺搜索页，对elements里面的商品的搜索页，id为J_ItemList是搜索页商品列表
                                                        div  class:J_TItems是店铺页的商品列表
    :param filepath:
    :return:
    '''
    resultlist=[]
    soup = BeautifulSoup(htmlread, 'lxml')
    listcontect=soup.find('div',{'id':'J_ItemList'})
    if listcontect ==None:
        listcontect = soup.find('div', {'class': 'J_TItems'})
        if listcontect !=None:
            items=soup.find_all('dl',{'class':'item '})
        else:
            return {'error':'这东西不对！！！'}

    else:
        items=soup.find_all('div',{'class':'product  '})

    for item in items:
        itemid=item.get('data-id')
        url='https://detail.tmall.com/item.htm?id='+itemid
        itemjson={'itemid':itemid,'url':url}
        resultlist.append(itemjson)
    return resultlist

@app.task(name='process.dealfile.readtmallhtml',queue='readtmallhtml')
def readtmallhtml(htmlread):
    '''
    对于天猫的搜索页|店铺搜索页，对elements里面的商品的搜索页，id为J_ItemList是搜索页商品列表
                                                        div  class:J_TItems是店铺页的商品列表
    :param filepath:
    :return:
    '''
    resultlist=[]
    soup = BeautifulSoup(htmlread, 'lxml')
    listcontect=soup.find('div',{'id':'J_ItemList'})
    if listcontect ==None:
        listcontect = soup.find('div', {'class': 'J_TItems'})
        if listcontect !=None:
            items=soup.find_all('dl',{'class':'item '})
        else:
            return {'error':'这东西不对！！！'}

    else:
        items=soup.find_all('div',{'class':'product  '})

    for item in items:
        itemid=item.get('data-id')
        url='https://detail.tmall.com/item.htm?id='+itemid
        itemjson={'itemid':itemid,'url':url}
        resultlist.append(itemjson)
    return resultlist


if __name__ == '__main__':
    # htmlpath='/Users/netboss/program/Ncode/text/testtm.html'
    # htmlfile = open(htmlpath, 'r', encoding='utf-8')
    # readhtml = htmlfile.read()
    # print (readtmallhtml(readhtml))
    readelejson('/Volumes/did/2019/Z2019023/02-采集-留证/5.22取点json/饿了么.json')

