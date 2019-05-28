from __future__ import absolute_import, unicode_literals
from celery import Celery,Task
import time,json,requests,re
requests.packages.urllib3.disable_warnings()

app=Celery('spider')
app.config_from_object('celeryconfig')



cookie = ""
head = {
    "user-agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_14_3) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/73.0.3683.86 Safari/537.36",

}



class DebugTask(Task):

    def __call__(self, *args, **kwargs):
        # print('TASK STARTING: {0.name}[{0.request.id}]'.format(self))
        return super(DebugTask, self).__call__(*args, **kwargs)


app.Task = DebugTask


head={
    "User-Agent":"Mozilla/5.0 (Macintosh; Intel Mac OS X 10_14_3) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/73.0.3683.86 Safari/537.36",
}

#普通浏览页面
@app.task(name='spider.onlinehtml.getdownhtml',queue='getdownhtml')
def getdownhtml(url,cookie='null'):
    if cookie!='null':
        head['cookie']=cookie
    if 'http://'not in url and 'https://' not in url:
        newurl = 'http://' + url
    else:
        newurl = url
    try:
        response = requests.get(url=newurl, headers=head,timeout=30, verify=False, allow_redirects=False)
    except Exception as e:
        return {'url': url, 'license': '超时', 'code': str(e)}
    if 'taobao' in url :
        response.encoding='gbk'
    # elif '.jd.'in url:
    #     response.encoding='gbk'
    elif '.tmall.'in url:
        response.encoding='gbk'
    else:
        response.encoding = 'utf-8'

    return response.text

#这是个清淤
@app.task(name='spider.onlinehtml.desilting',queue='desilting')
def desilting(url):
    '''
    特殊亮照：
    1、淘宝要把url里的http换成https,应该不用带cookie
    2、1688要带cookie
    这次是禁止跳转
    :param url:
    :return:
    '''

    if '.taobao.com' in url:
        if 'http://' in url:
            newurl = re.sub('http://', 'https://', url)
        elif 'https://' not in url:
            newurl = 'https://' + url
        else:
            newurl = url
    elif '.1688.com' in url:
        if 'http://' in url:
            newurl = re.sub('http://', 'https://', url)
        elif 'https://' not in url:
            newurl = 'https://' + url
        else:
            newurl = url
        head[
            'cookie'] = "hng=CN%7Czh-CN%7CCNY%7C156; lid=%E9%9F%A9%E5%B0%8F%E7%BE%BFh; cna=n2/+FMX/nmMCAd2F84I8iHzB; dnk=%5Cu97E9%5Cu5C0F%5Cu7FBFh; tracknick=%5Cu97E9%5Cu5C0F%5Cu7FBFh; lgc=%5Cu97E9%5Cu5C0F%5Cu7FBFh; cookie2=701bc961fc359ccc10c2f3849c5ee779; t=92e8af1adbe155ab90d8a64ca0d3b9d5; _tb_token_=5e9eeeeee0b73; uc1=cookie16=WqG3DMC9UpAPBHGz5QBErFxlCA%3D%3D&cookie21=VFC%2FuZ9aiKCaj7AzMHh1&cookie15=VFC%2FuZ9ayeYq2g%3D%3D&existShop=false&pas=0&cookie14=UoTZ4tdmJgnySQ%3D%3D&tag=8&lng=zh_CN; uc3=vt3=F8dByEa3N4KvdkqiysU%3D&id2=Uone8mnDUf0FMA%3D%3D&nk2=2QtOmLuzPA%3D%3D&lg2=UtASsssmOIJ0bQ%3D%3D; _l_g_=Ug%3D%3D; unb=1852260910; cookie1=AQHw1nnECh%2Bzvr3jyuwbkAyZTflwO9rsrLglLKdxZWk%3D; login=true; cookie17=Uone8mnDUf0FMA%3D%3D; _nk_=%5Cu97E9%5Cu5C0F%5Cu7FBFh; sg=h06; csg=9b07a611; l=bBLU5Xymv-pnikm9BOCgSZZzz_7TOIRAguWbaAV6i_5CE1L_VKbOlQseaep6Vj5RsbTB4T0o1199-etXm; isg=BOLiUbwtyvij7NbDjJijN6BEM25OM-Clcpc8Fyx7J9UA_4N5FMAIXLN9K3umb17l"
    else:
        if 'http://' not in url and 'https://' not in url:
            newurl = 'http://' + url
        else:
            newurl = url
    try:
        response = requests.get(url=newurl, headers=head, timeout=30, verify=False, allow_redirects=False)
    except Exception as e:
        return {'url': url, 'error': 'timeout','status': 'timeout'}
    if response.status_code == 200:
        return {'url': url, 'status': 'alive'}
    else:
        return {'url': url, 'status': 'need'}

@app.task(name='spider.onlinehtml.seconddesilting',queue='seconddesilting')
def seconddesilting(url):
    '''
    所有的线上操作尽量都要判断一下是不是taobao
    如果是淘宝要休息一户
    在第一次亮照检查之后200的放过去
    其他的全部进行第二次检查
    这次不禁跳
    特殊情况淘宝会跳到https://store.taobao.com/shop/noshop.htm
    :param url:
    :return:
    '''
    if 'http://' not in url and 'https://' not in url:
        newurl = 'http://' + url
    else:
        newurl = url
    try:

        response = requests.get(url=newurl, headers=head, timeout=30, verify=False)



    except Exception as e:
        return {'url': url, 'error': 'timeout'}
    if response.status_code == 200:
        if response.url=='https://store.taobao.com/shop/noshop.htm' or response.url=='https://page.1688.com/shtml/static/wrongpage.html':
            return {'url': url, 'status': 'die'}
        return {'url': url, 'status': 'alive'}
    else:
        return {'url': url, 'status': 'die'}

if __name__ == '__main__':
    target = 'https://list.tmall.com/search_product.htm?spm=a220m.1000858.0.0.747ed6bcMeDTc2&s=0&q=%C3%C0%B0%D7%C3%E6%C4%A4&sort=s&style=g&from=.list.pc_1_searchbutton&type=pc#J_Filter'
    cookie = 'hng=CN%7Czh-CN%7CCNY%7C156; lid=%E9%9F%A9%E5%B0%8F%E7%BE%BFh; cna=n2/+FMX/nmMCAd2F84I8iHzB; _med=dw:2560&dh:1440&pw:2560&ph:1440&ist:0; enc=Qkh91%2Fr40QwldUNg%2FvSe7yxBPcOnFLAf1o7m5hEYBTp9KSeQvV0rOX1Cmxb5iwRi9nZwEZNOk%2F%2FK9gyBtkgF8A%3D%3D; _m_h5_tk=d77b6bd538bb9d73d08455f9b49807ff_1557214518132; _m_h5_tk_enc=daca4c58799a15ae917f168650a26f7b; t=92e8af1adbe155ab90d8a64ca0d3b9d5; tracknick=%5Cu97E9%5Cu5C0F%5Cu7FBFh; lgc=%5Cu97E9%5Cu5C0F%5Cu7FBFh; _tb_token_=367a3769eb3d7; cookie2=1c5671b7f1abe3556fe35d1c05fc29e3; uc1=cookie16=UIHiLt3xCS3yM2h4eKHS9lpEOw%3D%3D&cookie21=U%2BGCWk%2F7p4mBoUyS4E9C&cookie15=VT5L2FSpMGV7TQ%3D%3D&existShop=false&pas=0&cookie14=UoTZ48eLy1vxvQ%3D%3D&tag=8&lng=zh_CN; uc3=vt3=F8dByEa%2Fw%2BC62H8Ps5M%3D&id2=Uone8mnDUf0FMA%3D%3D&nk2=2QtOmLuzPA%3D%3D&lg2=VT5L2FSpMGV7TQ%3D%3D; _l_g_=Ug%3D%3D; ck1=""; unb=1852260910; cookie1=AQHw1nnECh%2Bzvr3jyuwbkAyZTflwO9rsrLglLKdxZWk%3D; login=true; cookie17=Uone8mnDUf0FMA%3D%3D; _nk_=%5Cu97E9%5Cu5C0F%5Cu7FBFh; uss=""; csg=08072822; skt=7737176e1d43c34e; cq=ccp%3D0; res=scroll%3A2540*5461-client%3A2540*1263-offset%3A2540*5461-screen%3A2560*1440; pnm_cku822=098%23E1hvrvvUvbpvUvCkvvvvvjiPRLSU1j3En2MhsjEUPmPO1jl8Psdvtj1nP2M9gjE2RphvCvvvphvCvpvVvUCvpvvvKphv8vvvpHwvvvvhvvCEipvvvSwvvhi8vvmmZvvvoyIvvUUivvCEipvv93%2FEvpvVvpCmpaspuphvmvvvporVF2tomphvLvbbUkUaACeK5uy6Bu7t%2B1wsRoYm24VQR4VzEhV9D46XeutiBXxreCAK5kx%2F1RmKDf8rwyCl%2BboJjCDsBb2XrqpAhjCbFO7t%2B3mXJ99Pvpvhvv2MMTwCvvpvvhHh; l=bBLU5Xymv-pni70DBOCwdZZzzobOSIRAguWbaAYXi_5I31T_l8_OlKtfTe96Vj5R_cYB4q4zI6J9-etbi; isg=BKmpgxqB0QlHGe3Oaz0Isq_puFMJdpvMSS_5UUueJRDPEskkk8ateJeA0PaBijXg'

    # print (requests.get('http://xaix.tmall.com/index.htm?spm=a1z10.5-b.w5002-3654538693.2.D7pHbB',headers=head, allow_redirects=False))
    # print (desilting('http://xaix.tmall.com/index.htm?spm=a1z10.5-b.w5002-3654538693.2.D7pHbB'))
    print(getdownhtml(target,cookie))