
from kombu import Queue
from kombu import Exchange

enable_utc = True
timezone = 'Asia/Shanghai'
task_default_queue = 'default'
broker_url = 'pyamqp://spsp-server:spsp1505@10.0.6.17'
result_backend = 'redis://10.0.6.17/1'