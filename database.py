# -*- coding: utf-8 -*-

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base

db_path = "mysql+mysqldb://root:root@dbhost/app_ncdh?charset=utf8"
engine = create_engine(db_path)
 
DB_Session = sessionmaker(bind=engine)

Base = declarative_base()

def init_db():
    import models
    Base.metadata.create_all(bind=engine)
    