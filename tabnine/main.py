from sqlalchemy import Column, Integer
from sqlalchemy.ext.declarative import declarative_base


Base = declarative_base()


class User(Base):
    username = Column(Integer, primary_key=True)
    first_name = Column(Integer, nullable=False)
    second_name = Col
