from sqlalchemy import create_engine, Column, Integer, String
from sqlalchemy.ext.declarative import declarative_base

engine = create_engine('postgres://root:postgres@localhost/postgres', echo=True)

Base = declarative_base()


class Message(Base):
    __tablename__ = 'message'
    id = Column(Integer, primary_key=True)
    text = Column(String)

