from sqlalchemy import *
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

engine = create_engine("sqlite:///quotes_sqlite.db", echo=True)

Base = declarative_base()


class Quote(Base):
    __tablename__ = 'quote'
    id = Column(Integer, primary_key=True)
    quote = Column(String)
    author_id = Column(ForeignKey('author.id'))


class Author(Base):
    __tablename__ = 'author'
    id = Column(Integer, primary_key=True)
    name = Column(String)
    born_date = Column(String)
    born_location = Column(String)
    description = Column(Text)


# Base.metadata.create_all(engine)

Session = sessionmaker(bind=engine)
