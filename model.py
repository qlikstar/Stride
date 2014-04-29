from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer, Numeric, String, Date, Boolean, Index, event, DDL, func
import psycopg2
from sqlalchemy import create_engine
from sqlalchemy import text
from sqlalchemy import Sequence
from sqlalchemy import ForeignKey
from sqlalchemy.orm import sessionmaker
from sqlalchemy.orm import relationship, backref
from sqlalchemy import UniqueConstraint
from sqlalchemy.types import UserDefinedType
from sqlalchemy.sql import label
from sqlalchemy import func
import decimal

from sqlalchemy.dialects.postgresql import ARRAY, BIGINT, BIT, \
    BOOLEAN, BYTEA, CHAR, CIDR, DATE, \
    DOUBLE_PRECISION, ENUM, FLOAT, INET, INTEGER, \
    INTERVAL, MACADDR, NUMERIC, REAL, SMALLINT, TEXT, TIME, \
    TIMESTAMP, UUID, VARCHAR

import string
import ConfigParser

# load the app configuration file
config_file = 'app_config.ini'
config = ConfigParser.ConfigParser()
config.read(config_file)

# set the database configuration parameters
db_port = config.get('DEFAULT', 'port');
db_host =  config.get('DEFAULT','host')
db_pass = config.get('DEFAULT','passwd')
db_database = config.get('DEFAULT','database')
db_user = config.get('DEFAULT','user')
connect_str = 'postgresql+psycopg2://' + db_user + ':' + db_pass + '@' +\
    db_host + ':' + db_port + '/' + db_database

# can also call sessionmaker w/ out engine, and then use configure
engine = create_engine(connect_str, echo=False)
engine.dialect._to_decimal = float
Session = sessionmaker(bind=engine)
Base = declarative_base()

class Provider(Base):

    __tablename__ = 'provider'

    id = Column(Integer, primary_key=True)
    lastname = Column(TEXT)
    firstname = Column(TEXT)
    credentials = Column(TEXT)
    addr1 = Column(TEXT)
    addr2 = Column(TEXT)
    city = Column(TEXT, index=True)
    zipcode = Column(TEXT, index=True)
    state = Column(TEXT, index=True)
    latitude = Column(TEXT)
    longitude = Column(TEXT)
    
    def __init__(self, lastname, firstname, credentials,
                 addr1, addr2, city, zipcode, state, latitude, longitude):

        self.lastname = lastname
        self.firstname = firstname
        self.credentials = credentials
        self.addr1 = addr1
        self.addr2 = addr2
        self.city = city
        self.zipcode = zipcode
        self.state = state
        self.latitude = latitude
        self.longitude = longitude

    def __repr__(self):
        return "Provider<("+\
            "'%s', '%s', '%s', '%s', '%s', '%s', '%s')>" %\
            (self.firstname, self.lastname, self.credentials, self.addr1,
             self.city, self.zipcode, self.state,self.latitude, self.longitude)




class Zip_geo(Base):

    __tablename__ = 'zip_geo'

    id = Column(Integer, primary_key=True)
    zipcode   = Column(TEXT, index=True)
    latitude  = Column(TEXT)
    longitude = Column(TEXT)

    def __init__(self, zipcode, latitude, longitude):

        self.zipcode   = zipcode
        self.latitude  = latitude
        self.longitude = longitude

    def __repr__(self):
        return "Zip_geo<("+\
            "'%s', '%s', '%s')>" %\
            (self.zipcode, self.latitude, self.longitude)
