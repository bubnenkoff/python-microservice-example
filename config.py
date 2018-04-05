import os
import sys
import configparser
import logging

config = {}
log = logging.getLogger()

# seting ENV exemple:  export config=/home/bubnenkov/code/microservices/tr_extractor/config.ini
def get_config(): 
    global config
    if not "config" in os.environ:
    	log.critical("ENV do not have key 'config={config path}' that should include path to config!")
    	sys.exit()

    config_file = os.path.join(os.environ['config'])
    config_parser = configparser.RawConfigParser()
    config_parser.read(config_file)
     
    config['dbname'] = config_parser.get('db', 'dbname')
    config['host'] = config_parser.get('db', 'host')
    config['port'] = config_parser.get('db', 'port')
    config['login'] = config_parser.get('db', 'login')
    config['pass'] = config_parser.get('db', 'pass')

    config['logstashhost'] = config_parser.get('logstash', 'host')
    config['logstashport'] = config_parser.get('logstash', 'port')    

    return config
