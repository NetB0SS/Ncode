from __future__ import absolute_import, unicode_literals
from celery import Celery,Task
import time,json,requests,re,os,csv
from bs4 import BeautifulSoup
requests.packages.urllib3.disable_warnings()




def deleteDuplicatedElement(l):
    ll = []
    for x in l:
        if x in ll:
            continue
        else:
            ll.append(x)
    return ll



def cut_sent(para):
    '''
    切句子脚本，输入一段text然后会切成句子的列表
    :param para:
    :return:list
    '''
    para = re.sub('([。！？\?])([^”’])', r"\1\n\2", para)  # 单字符断句符
    para = re.sub('(\.{6})([^”’])', r"\1\n\2", para)  # 英文省略号
    para = re.sub('(\…{2})([^”’])', r"\1\n\2", para)  # 中文省略号
    para = re.sub('([。！？\?][”’])([^，。！？\?])', r'\1\n\2', para)
    # 如果双引号前有终止符，那么双引号才是句子的终点，把分句符\n放到双引号后，注意前面的几句都小心保留了双引号
    para = para.rstrip()  # 段尾如果有多余的\n就去掉它
    # 很多规则中会考虑分号;，但是这里我把它忽略不计，破折号、英文双引号等同样忽略，需要的再做些简单调整即可。
    paralist=para.split("\n")
    for x in paralist:
        if x == '':
            paralist.remove('')
    last1 = deleteDuplicatedElement(paralist)
    return(last1)


def searchkey(keylist,text):
    '''
    这个是以句子为单位的关键词搜索，过程就是传过来一个句子直接搜索返回命中的关键词
    :param text:
    :return: list
    '''
    keys = keylist
    keyresult=[]
    # with open('/Users/netboss/Desktop/021/关键词.txt', 'r', encoding='utf-8') as b:
    #     line = b.readline()
    #     while line:
    #         line = re.sub('\n', '', line)
    #         keys.append(line)
    #         line = b.readline()
    for key in keys:
        pattern = re.compile(key)
        result = pattern.findall(text)
        if len(result) != 0:
            keyresult.append(key)
    return keyresult



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

#检查页面时是否有商城店铺
@app.task(name='process.searchonhtml.searchshop',queue='searchshop')
def searchshop(url,responsetext):

    soup = BeautifulSoup(responsetext, 'lxml')
    shoplink = soup.find('a', {'href': re.compile('(taobao|jd|tmall)')})
    shopurl=shoplink.get('href')
    return shopurl


#普通亮照
@app.task(name='process.searchonhtml.commonlicense',queue='commonlicense')
def commonlicense(url,responsetext):

    '''
    这边就只是页面上存在218.242.124.22或者www.sgs.gov.cn我就认为他亮照了，只是还是会进去看一下他这个域名对不对得上
    :param url:
    :param responsetext:
    :return:
    '''

    head = {
        "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_14_3) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/73.0.3683.86 Safari/537.36",
    }
    soup = BeautifulSoup(responsetext.text, 'lxml')
    licenselink = soup.find('a', {'href': re.compile(r'218\.242\.124\.22|www\.sgs\.gov\.cn')})

    if licenselink == None:
        alla = soup.find_all('a')
        a = None
        for eacha in alla:
            if '营业执照' in eacha.text:
                a = '自行亮照'
                return {'url': url,
                        'license': a}
        return {'url': url,
                'license': a}


    else:
        licenseurl = licenselink.get('href')
    head['Referer'] = responsetext.url
    licenseresponse = requests.get(licenseurl, headers=head, verify=False)
    licenseresponse.encoding = 'utf-8'
    licensesoup = BeautifulSoup(licenseresponse.text, 'lxml')
    licensepattern1 = re.compile('链接网站与工商亮照备案域名不一致')
    licenseresult = licensepattern1.findall(licensesoup.prettify())
    if len(licenseresult) == 0:
        return {'url': url, 'license': '已亮照'}
    else:
        return {'url': url, 'license': '已亮照，但与备案域名不一致'}


#深层次亮照
@app.task(name='process.searchonhtml.commonlicense',queue='commonlicense')
def deeplicense(url,responsetext):
    head = {
        "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_14_3) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/73.0.3683.86 Safari/537.36",
    }
    soup = BeautifulSoup(responsetext.text, 'lxml')
    alllink = soup.find_all('a')
    if len(alllink) == 0:
        return {'url': url,
                'license': None}
    # half=int(len(alllink)/2)
    newhref = alllink[0].get('href')
    if url not in newhref:
        withhead = re.findall(r'^/', newhref)
        if len(withhead) == 0:
            newhref = url + '/' + newhref
        else:
            newhref = url + newhref
    if 'http://' not in newhref and 'https://' not in newhref:
        newhref = 'http://' + newhref

    try:
        newresponse = requests.get(url=newhref, headers=head, verify=False)
    except Exception as e:
        return {'url': url,
                'license': '未知错误', 'code': e}
    newsoup = BeautifulSoup(newresponse.text, 'lxml')
    alla = newsoup.find_all('a')
    a = None
    for eacha in alla:

        if '上海工商' in eacha.text:
            a = '自行亮照'
            return {'url': url,
                    'license': a}
    return {'url': url,
            'license': a}


#关键词搜索，两个参，一个是关键词列表，一个是本地页面,这个是新的！！！
@app.task(name='process.searchonhtml.searchtext',queue='searchtext')
def searchtext(keylist,responsetext):
    '''
    单个页面关键词检查
    逻辑就是直接用正则在页面上findall
    :param keylist:
    :param date:
    :return resultlist:
    '''
    resultlist=[]
    resultkey=[]
    soup = BeautifulSoup(responsetext.text, 'lxml')
    content = re.sub('<[^>]*>', '', soup.prettify())
    content = re.sub(' ', '', content)

    last = cut_sent(content)
    for tex in last:
        a = searchkey(keylist,tex)
        if len(a) != 0:
                resultlist.append({'key': a, 'result': tex})

    return resultlist

#行业分类，本质上和关键词检查没差别，有一个行业分类的关键词表，希望做到的效果是，一个网站过来，输出，命中了多少关键词，命中率多少
@app.task(name='process.searchonhtml.classify',queue='classify')
def classify(responsetext,keylist):
    soup = BeautifulSoup(responsetext, 'lxml')
    content = re.sub('<[^>]*>', '', soup.prettify())
    content = re.sub(' ', '', content)
    resultlist=[]
    keycuount=0
    for key in keylist:

        pattern = re.compile(key)
        result = pattern.findall(content)
        onekey = len(result)
        if onekey != 0:
            keycuount=keycuount+1
            resultlist.append({'key':key,'count':onekey})

    allkey=len(keylist)
    keyresult="%.2f%%" % (keycuount/allkey*100)

    return {'keycount':keyresult,'keyresult':resultlist}







if __name__ == '__main__':
    newurl='https://sh.58.com/zufang/37755547866787x.shtml'
    response = requests.get(url=newurl, timeout=30, verify=False)
    keylist=['靠近.*?地铁','步行','协议','博彩','亚洲图片','乱伦','真人娱乐','彩票','购彩','中介']
    print(classify(keylist,response))

