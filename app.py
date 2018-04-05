# -*- coding: utf-8 -*-
import json
import falcon
import logging
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.dialects import postgresql
from dictalchemy.utils import make_class_dictable, asdict
from db.manager import session
from db.model import *

log = logging.getLogger()

class MyAPI():
	def on_post(self, req, resp):
		request_json = None
		ready_query = None
		error_msg = dict()
		try:
			request_json = json.loads(req.stream.read().decode('utf-8')) # do not needed in Python >=3.6
			# оригинальный request_json нам так же потребуется т.к. в нем содержится информация о том какие таблицы
			# нам необходимо сджойнить, а так же прочие параметры, которые мы можем задать (увы) только на этапе формирования словаря
			if do_simple_validation(request_json): # Now True or False only
				ready_query = make_query(request_json)
				resp.body = get_list_of_transactions_from_db(ready_query, request_json)
			else:
				error_msg['error'] = 'Valiadation Error! <filters> is missing?'
				print('Valiadation Error! "filters" is missing?')
				resp.body = json.dumps(error_msg)
		except ValueError as e:
			log.critical("Input JSONDecodeError: {0} Exception: {1}".format(req.stream.read().decode('utf-8'), e))
			error_msg['error'] = 'JSONDecodeError'
			resp.body = json.dumps(error_msg)

	def on_get(self, req, resp):
		resp.body = "Please send POST requests!"

def create_app():
	app = falcon.API()
	api = MyAPI()
	app.add_route('/', api)
	return app

def do_simple_validation(request_json):
	if 'filters' not in request_json:
		return False
	else:
		return True

def make_query(request_json): # тут мы формируем только базовый запрос, некоторые вещи делаем еще в get_list_of_transactions_from_db
	query = session.query(Transaction)
	incl = request_json['filters'][0]

	for k, v in incl.items():
		if k not in ['start_date', 'end_date', 'limit', 'offset']: # у нас нет атрибутов 'start_date', 'end_date'. Пропускаем и обрабатываем их дальше
			column = getattr(Transaction, k)
			if isinstance(v, list):
				query = query.filter(column.in_(v))
			if isinstance(v, str):
				query = query.filter(column == v)
			if isinstance(v, int):
				query = query.filter(column == v)
		else:
			# не пытаться использовать between в SQL тк мы тут в цикле все обрабатываем
			if 'start_date' in k:
				query = query.filter(Transaction.created >= v)
			if 'end_date' in k:	
				query = query.filter(Transaction.created <= v)
	# Идея перебирать некоторые вещи в цикле была не очень полезна. 
	# Некоторые вещи типа лимитов **надежнее/удобнее** без всяких циклов
	# print(incl['limit']) --> 100
	my_limit = incl['limit']
	my_offset = incl['offset']
	query = query.order_by(Transaction.id)
	query = query.limit(my_limit)
	query = query.offset(my_limit * my_offset)

	# print(str(query.statement.compile(compile_kwargs={"literal_binds": True})))
	return query

def get_list_of_transactions_from_db(ready_query, request_json): # example: 6225064,6225148
	tr_list = []
	follow_list = request_json['join'] # из прилетевшего json нам надо извлечь столбцы которые нужно приджойнить
	exclude_columns = request_json['exclude_columns'] # столбцы которые исключаем (опять же на момент формирования словаря только можем)
	answer = None
	count = 0
	tr_count_dict = dict() # только для подсчета транзакций
	another_answer = dict() # если нужно вернуть произвольный ответ.
	try:
		if 'count' in request_json and request_json['count']: # если поле есть и оно True
			count = ready_query.count()	
			tr_count_dict['count'] = count
		else:
			for tr in ready_query.all():
				# print(tr.asdict(follow=['price'], exclude=['created']))
				tr_list.append(tr.asdict(follow=follow_list, exclude=exclude_columns))
	except SQLAlchemyError as e:
		log.critical("Can't extract list of transactions from DB. Exception: {0}".format(e))
	try:
		if 'count' in request_json and request_json['count']: # если поле есть и оно True
			answer = json.dumps(tr_count_dict)
		else: # а вот тут уже список
			answer = json.dumps(tr_list, default=str)
			answer = answer[1:-1] # Потому что default=str добавляет нам обертку вида: [{}] а надо просто {}
			# print(repr(answer))
			if not answer or answer == '[]': # если по запросу ничего нет. Почему-то dumps тут возвращает []
				another_answer['error'] = "No data for specified request"
				answer = json.dumps(another_answer)
	except TypeError as e:
		log.critical("Can't decode DB answer to JSON. Exception: {0}".format(e))

	return answer
	

# print(get_list_of_transactions_from_db([6225064,6225148]))




