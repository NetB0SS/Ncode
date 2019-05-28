from __future__ import absolute_import, unicode_literals
from celery import Celery,Task
import time,json,requests,os
requests.packages.urllib3.disable_warnings()


app=Celery('spider')
app.config_from_object('celeryconfig')

class DebugTask(Task):

    def __call__(self, *args, **kwargs):
        # print('TASK STARTING: {0.name}[{0.request.id}]'.format(self))
        return super(DebugTask, self).__call__(*args, **kwargs)


app.Task = DebugTask




#这是个遍历本地文件夹找留证目录的方法
@app.task(name='spider.offlinehtml.offlinehtml',queue='offlinehtml')
def offline(osPath):
    '''
    这是个遍历本地文件夹，找到source.html的上一层目录，但是还是要判断一下，要不有可能会有失败的留证捣乱
    :param osPath:
    :return date:
    '''
    date=[]

    for root, dirs, files in os.walk(osPath):
        for dirr in dirs:
            dirname = os.path.join(root, dirr)
            date.append(dirname)
    return date


@app.task(name='spider.offlinehtml.scrapynormal',queue='scrapynormal')
def scrapynormal(htmlpath):
    '''
    制定html页面解析返回responsetext
    :param htmlpath:
    :return:
    '''
    htmlfile=open(htmlpath,'r',encoding='utf-8')
    readhtml=htmlfile.read()
    # print (type(readhtml))

    return readhtml




if __name__ == '__main__':
    print (scrapynormal('/Users/netboss/program/Ncode/text/024text/html/tmalllist/美白1.html'))