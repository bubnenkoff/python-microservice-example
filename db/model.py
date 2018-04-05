from sqlalchemy.types import (Integer, SmallInteger, Numeric, String, Float, DateTime, Enum, Boolean, UnicodeText, BigInteger)
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship
from dictalchemy import DictableModel

Base = declarative_base(cls=DictableModel)
ListOfTables = Base.metadata.tables.keys() # will use it to to verify list of fields in requests


class Transaction(Base):
    __tablename__ = 'transactions'
    id = Column(Integer, primary_key=True, autoincrement=True)
    opcode = Column(SmallInteger, nullable=False)
    created = Column(String(50), nullable=False) #!
    status = Column(String(50), nullable=False)
    updated = Column(String(50), nullable=False) #!
    status_changes_counter = Column(BigInteger)
    client_id = Column(BigInteger, nullable=False)
    site_id = Column(Integer, nullable=False)
    product_id = Column(Integer, nullable=False)
    instrument_type_id = Column(Integer, nullable=False)
    
    instrument_id = Column(Integer, nullable=True)

    amount = Column(Numeric(15, 2), nullable=False)
    amount_converted = Column(Numeric(15, 2), nullable=True)
    currency_id_converted = Column(None, nullable=True)

    channel_id = Column(None, nullable=False)
    account_id = Column(Integer, nullable=False)
    authcode = Column(String(8), nullable=True)
    remote_id = Column(String(255), nullable=True)
    remote_id_ext = Column(String(255), nullable=True)
    remote_id2 = Column(String(1024), nullable=True)
    remote_id3 = Column(String(1024), nullable=True)
    remote_id4 = Column(String(1024), nullable=True)
    remote_id5 = Column(String(1024), nullable=True)
    product_descr = Column(String(1024), nullable=True)
    # Transaction datetime on the external processing side
    remotely_processed = Column(DateTime)
    site_notified = Column(DateTime)

    is_aft = Column(Boolean, nullable=False, default=False)
    reference_id = Column(None, nullable=True)

    phone = Column(String(16), nullable=True)
    cs0 = Column(String(1024, convert_unicode=True))
    cs1 = Column(String(1024, convert_unicode=True))
    cs2 = Column(String(1024, convert_unicode=True))
    cs3 = Column(String(1024, convert_unicode=True))
    cs4 = Column(String(1024, convert_unicode=True))
    cs5 = Column(String(1024, convert_unicode=True))
    cs6 = Column(String(1024, convert_unicode=True))
    cs7 = Column(String(1024, convert_unicode=True))
    cs8 = Column(String(1024, convert_unicode=True))
    cs9 = Column(String(1024, convert_unicode=True))
    secure_mode = Column(Integer, default=0) # secure_mode = 1 if transactions is 3ds
    hash = Column(String(255), nullable=False)

    order_id = Column(String(255, convert_unicode=True))
    termurl = Column(String(1024), nullable=True)
    md = Column(String(1024), nullable=True)
    terminal_id = Column(None, nullable=True)
    rebill_status = Column('rebill_status', Enum(
        'enabled',
        '',
        'softlock',
        'hardlock',
        'lockuntil',
        name='rebill_status',
    ), nullable=True)
    rebill_from = Column(DateTime, nullable=True)
    rebill_statusreason = Column(String(1024), nullable=True)

    mw_id = Column(String, nullable=True)
    request_id = Column(String(1024), nullable=True, unique=True)
    mw_timestamp_created = Column(DateTime, nullable=False)
    mw_type = Column(String(1024), nullable=True)
    card_type = Column(String(1024), nullable=True)
    pan = Column(String(20), nullable=True)
    mw_merchant_id = Column(Integer, nullable=True)
    mw_node_id = Column(Integer, nullable=True)
    gw_node_id = Column(Integer, nullable=True)
    rrn = Column(String, nullable=True)
    subprovider_id = Column(String, nullable=True)
    contract_id = Column(String, nullable=True)
    contract_token = Column(String, nullable=True)
    ccadress = Column(String(50), nullable=True, unique=True)


    price = relationship('TransactionPrices', uselist=False, backref='transaction') # transaction_prices
    cost = relationship('ClientCosts', uselist=False, backref='transaction') # ClientCosts 


class TransactionPrices(Base):
    __tablename__ = 'transaction_prices'
    id = Column("id", Integer, primary_key=True, autoincrement=True)
    transaction_id = Column(None, ForeignKey("transactions.id"), nullable=False, unique = True)
    mandarin_percentage = Column(Float, nullable=True)
    mandarin_minimum = Column(Float, nullable=True)
    mandarin_maximum = Column(Float, nullable=True)
    mandarin_fix = Column(Float, nullable=True)
    mandarin_total_price = Column(Float, nullable=True)
    counterparty_clientid = Column(Integer, nullable=True)
    counterparty_percentage = Column(Float, nullable=True)
    counterparty_minimum = Column(Float, nullable=True)
    counterparty_maximum = Column(Float, nullable=True)
    counterparty_fix = Column(Float, nullable=True)
    counterparty_total_price = Column(Float, nullable=True)
    status = Column(String(1024), nullable=True) 


class ClientCosts(Base):
    __tablename__ = 'client_costs'
    id = Column("id", Integer, primary_key=True, autoincrement=True)
    transaction_id = Column(None, ForeignKey("transactions.id"), nullable=False, unique = True)
    accountingSystem_clientid = Column(Integer, nullable=True)
    accountingSystem_percentage = Column(Float, nullable=True)
    accountingSystem_minimum = Column(Float, nullable=True)
    accountingSystem_maximum = Column(Float, nullable=True)
    accountingSystem_fix = Column(Float, nullable=True)
    accountingSystem_total_cost = Column(Float, nullable=True)
    paymentSystem_clientid = Column(Integer, nullable=True)
    paymentSystem_percentage = Column(Float, nullable=True)
    paymentSystem_minimum = Column(Float, nullable=True)
    paymentSystem_maximum = Column(Float, nullable=True)
    paymentSystem_fix = Column(Float, nullable=True)
    paymentSystem_total_price = Column(Float, nullable=True)
    status = Column(String(1024), nullable=True)


ListOfTransactionColumns = Transaction.__table__.columns.keys()