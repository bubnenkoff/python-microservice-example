import logging 
import logstash
import logstashformatter
from config import *

from app import create_app

log = logging.getLogger()
log.setLevel(logging.WARNING)
#handler = logging.StreamHandler() # standard handler
logstash_handler = logstash.LogstashHandler(config['logstashhost'], config['logstashport'], version=1)
logstash_handler.setFormatter(logstashformatter.JsonFormatter())
log.addHandler(logstash_handler)
# log.addHandler(logstash.LogstashHandler(host, 5959, version=1))
log.addFilter(logstashformatter.LogstashFilter())

app = create_app() # 
