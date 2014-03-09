#-*- coding: utf-8 -*-

from sqlalchemy import Column, Integer, String, BIGINT, DATETIME, DATE
from database import Base


class Photo(Base): 
    __tablename__ = "photo"

    id = Column(Integer, primary_key=True)
    baidu_id = Column(BIGINT, unique=True)
    photo_id = Column(BIGINT)
    image_url = Column(String(255))
    image_width = Column(Integer)
    image_height = Column(Integer)
    thumbnail_url = Column(String(255))
    thumbnail_width = Column(Integer)
    thumbnail_height = Column(Integer)
    thumb_large_url = Column(String(255))
    thumb_large_width = Column(Integer)
    thumb_large_height = Column(Integer)
    from_url = Column(String(255))
    obj_url = Column(String(255))
    desc = Column(String(255))
    image_date = Column(DATE)
    insert_date = Column(DATETIME)

    