
from kombu import Queue
from kombu import Exchange

enable_utc = True
timezone = 'Asia/Shanghai'
task_default_queue = 'default'
broker_url = 'pyamqp://spsp-server:spsp1505@10.0.6.17'
result_backend = 'redis://10.0.6.17/1'






task_queues = (
    Queue('getdownhtml', exchange=Exchange('getdownhtml', type='direct'), routing_key='getdownhtml'),
    Queue('offline', exchange=Exchange('offline', type='direct'), routing_key='offline'),
    Queue('desilting', exchange=Exchange('desilting', type='direct'), routing_key='desilting'),
    Queue('seconddesilting', exchange=Exchange('seconddesilting', type='direct'), routing_key='seconddesilting'),
    Queue('scrapynormal', exchange=Exchange('scrapynormal', type='direct'), routing_key='scrapynormal'),

)






task_routes = {
    'spider.onlinehtml.getdownhtml': {'queue': 'getdownhtml', 'routing_key': 'getdownhtml',},
    'spider.offlinehtml.offline': {'queue': 'offline', 'routing_key': 'offline', },
    'spider.onlinehtml.desilting': {'queue': 'desilting', 'routing_key': 'desilting', },
    'spider.onlinehtml.seconddesilting': {'queue': 'seconddesilting', 'routing_key': 'seconddesilting', },
    'spider.offlinehtml.scrapynormal': {'queue': 'scrapynormal', 'routing_key': 'scrapynormal', },

}