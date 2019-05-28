from __future__ import absolute_import, unicode_literals
from celery import Celery,Task
import csv



app=Celery('process')
app.config_from_object('celeryconfig')

class DebugTask(Task):

    def __call__(self, *args, **kwargs):
        # print('TASK STARTING: {0.name}[{0.request.id}]'.format(self))
        return super(DebugTask, self).__call__(*args, **kwargs)


app.Task = DebugTask

#这个对应flask的接口来处理用户上传上来的文件
@app.task(name='process.dealwithupload.readuploadfile',queue='readuploadfile')
def readuploadfile(filepath):
    fileopen=open(filepath,'r',encoding='utf-8')

    pass