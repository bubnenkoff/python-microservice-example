# -*- coding: utf-8 -*-
# так как мы логируем все в json, то тюнингуем штатный модуль, так чтобы он отдавал нам json с нужными полями

# @timestamp - текущее время в UTC в ISO-формате (например 2017-12-20T17:05:35.311Z)
# serviceType - тип сервиса (источник) - secure, gw, etc
# level - уровень сообщения (FATAL, ERROR, WARN, INFO, DEBUG, TRACE)
# message - сообщение

# необязательные:
# serviceInstanceId - id инстанса сервиса
# subsystem - подсистема внутри сервиса (web и service в случае секура)
# category - категория (источник) внутри сервиса (обычно используют имя класса)

import logging
import json
from datetime import datetime

class JsonFormatter(logging.Formatter):
   def format(self, record):
       record.message = record.getMessage()
       # record.asctime = self.formatTime(record, self.datefmt) # аналог этого поля у нас уже есть
       if record.exc_info:
           if not record.exc_text:
               record.exc_text = self.formatException(record.exc_info)
       return json.dumps({k: v for k, v in vars(record).items() if k not in ('msg', 'args', 'exc_info', 'threadName', 'MainThread', 'thread', 'relativeCreated', 'exc_text', 'msecs', 'process', 'processName', 'funcName', 'levelno')})

class LogstashFilter(logging.Filter):
   def filter(self, record): # полное описание https://gitlab.sudo.su/xmp/wiki/wikis/JSON-Log-Format
       setattr(record, '@timestamp', datetime.fromtimestamp(record.created).isoformat()) # @timestamp - текущее время в UTC в ISO-формате (например 2017-12-20T17:05:35.311Z)
       record.serviceType = 'tr_extractor' # serviceType - тип сервиса (источник) - secure, gw, etc
       record.level = record.levelname # level - уровень сообщения (FATAL, ERROR, WARN, INFO, DEBUG, TRACE)
       return True