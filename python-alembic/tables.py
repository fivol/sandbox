# coding: utf-8
from sqlalchemy import Column, Float, Integer, String, text
from sqlalchemy.ext.declarative import declarative_base


Base = declarative_base()
metadata = Base.metadata


class User(Base):
    __tablename__ = 'user'

    id = Column(Integer, primary_key=True, server_default=text("nextval('user_id_seq'::regclass)"))
    name = Column(String(50), nullable=False)
    age = Column(Float(53))
