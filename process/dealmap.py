from __future__ import absolute_import, unicode_literals
from celery import Celery,Task
import time,json,requests

app=Celery('process')
app.config_from_object('celeryconfig')

class DebugTask(Task):

    def __call__(self, *args, **kwargs):
        # print('TASK STARTING: {0.name}[{0.request.id}]'.format(self))
        return super(DebugTask, self).__call__(*args, **kwargs)


app.Task = DebugTask



def isRayIntersectsSegment(poi,s_poi,e_poi): #[x,y] [lng,lat]
    #输入：判断点，边起点，边终点，都是[lng,lat]格式数组
    if s_poi[1]==e_poi[1]: #排除与射线平行、重合，线段首尾端点重合的情况
        return False
    if s_poi[1]>poi[1] and e_poi[1]>poi[1]: #线段在射线上边
        return False
    if s_poi[1]<poi[1] and e_poi[1]<poi[1]: #线段在射线下边
        return False
    if s_poi[1]==poi[1] and e_poi[1]>poi[1]: #交点为下端点，对应spoint
        return False
    if e_poi[1]==poi[1] and s_poi[1]>poi[1]: #交点为下端点，对应epoint
        return False
    if s_poi[0]<poi[0] and e_poi[1]<poi[1]: #线段在射线左边
        return False

    xseg=e_poi[0]-(e_poi[0]-s_poi[0])*(e_poi[1]-poi[1])/(e_poi[1]-s_poi[1]) #求交
    if xseg<poi[0]: #交点在射线起点的左侧
        return False
    return True  #排除上述情况之后

@app.task(name='process.dealmap.isPoiWithinPoly',queue='isPoiWithinPoly')
def isPoiWithinPoly(poi,poly):
    sinsc=0 #交点个数
    for epoly in poly: #循环每条边的曲线->each polygon 是二维数组[[x1,y1],…[xn,yn]]
        for i in range(len(epoly)-1): #[0,len-1]
            s_poi=epoly[i]
            e_poi=epoly[i+1]
            if isRayIntersectsSegment(poi,s_poi,e_poi):
                sinsc+=1 #有交点就加1

    return True if sinsc%2==1 else  False




if __name__ == '__main__':

    # jsonfile = '/Volumes/did/2019/Z2019023/02-采集-留证/5.22取点json/星选.json'
    # openfile = open(jsonfile, 'r', encoding='utf-8')
    # data = openfile.readlines()
    # num=0
    # for a in data:
    #     num=num+1
    #     eachjson=json.loads(a)
    #     name=eachjson['name']
    #     url=eachjson['url']
    #     print(str(num) + ',' + name + ',' + url)



    '''
    ===================================美团=======================================================
    # '''
    polylineApi = 'http://127.0.0.1:5000/Map/polyline'

    polyline_req = requests.post(url=polylineApi, data={
        "citycode": '021',
        "name": '青浦区'
    })
    poly_response = json.loads(polyline_req.text)
    polyline = poly_response['polyline']

    deal_polyline = polyline.split(';')
    polylinelist = []
    eachline = []
    for c in deal_polyline:
        c_list = c.split(',')
        flo = list(map(float, c_list))

        polylinelist.append(flo)


    jsonfile = '/Volumes/did/2019/Z2019023/02-采集-留证/5.22取点json/美团.json'
    openfile = open(jsonfile, 'r', encoding='utf-8')
    data = openfile.readlines()
    num=0
    for each in data:

        eachjson=json.loads(each)
        address=eachjson['address']

        target='https://restapi.amap.com/v3/geocode/geo?parameters'



        prams={
            'key':'e750606528a385d4fc94c1587f7f98fa',
            'address':address,
            'city':'上海'


        }
        a=requests.get(target,params=prams)
        ajson=a.json()
        geocodes=ajson['geocodes']
        name=eachjson['name']
        url=eachjson['url']
        address=eachjson['address']

        if len(geocodes)==1:
            for b in geocodes:
                # eachjson['location']=b['location']
                poi = b['location'].split(',')
                plist=[]
                for pi in poi:

                    newpi=float(pi)
                    plist.append(newpi)
                polyresult = isPoiWithinPoly(plist, [polylinelist])
                # print (plist)
                if polyresult == True:
                    num = num + 1
                    print(str(num) + ',' + name + ',' + url+','+address)


        else:
            pass
    '''
    ============================================================================================
    '''








    '''
===============================饿了么==========================================
'''
    # polylineApi='http://127.0.0.1:5000/Map/polyline'
    #
    #
    # polyline_req = requests.post(url=polylineApi, data={
    #     "citycode": '021',
    #     "name": '青浦区'
    # })
    # poly_response = json.loads(polyline_req.text)
    # polyline = poly_response['polyline']
    #
    # deal_polyline = polyline.split(';')
    # polylinelist = []
    # eachline = []
    # for c in deal_polyline:
    #     c_list = c.split(',')
    #     flo = list(map(float, c_list))
    #
    #     polylinelist.append(flo)
    #
    # jsonfile='/Volumes/did/2019/Z2019023/02-采集-留证/5.22取点json/饿了么.json'
    # openfile = open(jsonfile, 'r', encoding='utf-8')
    # data = openfile.readlines()
    # num = 0
    # for a in data:
    #     eachjson=json.loads(a)
    #     # print (eachjson)
    #     longitude=eachjson['longitude']
    #     latitude=eachjson['latitude']
    #     poi=[longitude,latitude]
    #     polyresult = isPoiWithinPoly(poi, [polylinelist])
    #
    #     if polyresult==True:
    #         num=num+1
    #         name=eachjson['name']
    #         url=eachjson['url']
    #         print (str(num)+','+name+','+url)
'''
============================================================================================
'''



