
from kombu import Queue
from kombu import Exchange

enable_utc = True
timezone = 'Asia/Shanghai'
task_default_queue = 'default'
broker_url = 'pyamqp://spsp-server:spsp1505@10.0.6.17'
result_backend = 'redis://10.0.6.17/1'






task_queues = (
    Queue('searchshop', exchange=Exchange('searchshop', type='direct'), routing_key='searchshop'),
    Queue('commonlicense', exchange=Exchange('commonlicense', type='direct'), routing_key='commonlicense'),
    Queue('searchtext', exchange=Exchange('searchtext', type='direct'), routing_key='searchtext'),
    Queue('classify', exchange=Exchange('classify', type='direct'), routing_key='classify'),
    Queue('deeplicense', exchange=Exchange('deeplicense', type='direct'), routing_key='deeplicense'),
    Queue('readuploadfile', exchange=Exchange('readuploadfile', type='direct'), routing_key='readuploadfile'),
    Queue('readelejson', exchange=Exchange('readelejson', type='direct'), routing_key='readelejson'),
    Queue('readxingxuanjson', exchange=Exchange('readxingxuanjson', type='direct'), routing_key='readxingxuanjson'),
    Queue('readmeituanjson', exchange=Exchange('readmeituanjson', type='direct'), routing_key='readmeituanjson'),
    Queue('readtmallhtml', exchange=Exchange('readtmallhtml', type='direct'), routing_key='readtmallhtml'),

)






task_routes = {
    'process.searchonhtml.searchshop': {'queue': 'searchshop', 'routing_key': 'searchshop',},
    'process.searchonhtml.commonlicense': {'queue': 'commonlicense', 'routing_key': 'commonlicense', },
    'process.searchonhtml.searchtext': {'queue': 'searchtext', 'routing_key': 'searchtext', },
    'process.searchonhtml.classify': {'queue': 'classify', 'routing_key': 'classify', },
    'process.searchonhtml.deeplicense': {'queue': 'deeplicense', 'routing_key': 'deeplicense', },
    'process.dealwithupload.readuploadfile': {'queue': 'readuploadfile', 'routing_key': 'readuploadfile', },
    'process.dealfile.readelejson': {'queue': 'readelejson', 'routing_key': 'readelejson', },
    'process.dealfile.readxingxuanjson': {'queue': 'readxingxuanjson', 'routing_key': 'readxingxuanjson', },
    'process.dealfile.readmeituanjson': {'queue': 'readmeituanjson', 'routing_key': 'readmeituanjson', },
    'process.dealfile.readtmallhtml': {'queue': 'readtmallhtml', 'routing_key': 'readtmallhtml', },

}