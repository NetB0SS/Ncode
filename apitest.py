import requests




target='http://10.0.6.151:5000/netobject'

parm={
    'condition':{},
    'need':['ID'],
    'limit':1,
    'page_num':1
}


a=requests.get(target,params=parm)
print (a)