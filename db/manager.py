import logging
import sqlalchemy
from sqlalchemy import orm
from sqlalchemy.orm import sessionmaker, relationship
from sqlalchemy.dialects import postgresql
from db.model import Base, ListOfTables, ListOfTransactionColumns
from sqlalchemy import create_engine
from sqlalchemy.exc import SQLAlchemyError
from config import *
import os
import sys
sys.path.append("..")
from config import *

log = logging.getLogger()

def setup_connection():
	
	config = get_config()
	# engine = create_engine('postgresql://postgres@localhost:5432/gateway0205', echo=False) # for localhost without pass
	conn_string = 'postgresql://' + config['login'] + ':' + config['pass'] + '@' + config['host'] + ':' + config['port'] + '/' + config['dbname']
	engine = create_engine(conn_string, echo=False)
	Session = sessionmaker(bind=engine)
	sess = Session()
	try:
		Base.metadata.create_all(engine)
	except SQLAlchemyError as e:
		log.critical('\nCould not initialize DB: {0}'.format(e))
	return sess

session = setup_connection()