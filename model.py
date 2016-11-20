import sys

from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer, String
from sqlalchemy.dialects.mysql import LONGTEXT
from sqlalchemy import create_engine

Base = declarative_base()


class Article(Base):
     __tablename__ = "articles"

     id             = Column(String(30), primary_key=True)
     category       = Column(String(30))
     sub_category   = Column(String(30))
     date           = Column(String(30))
     href           = Column(String(200))
     title          = Column(LONGTEXT)
     summary        = Column(LONGTEXT)
     content        = Column(LONGTEXT)
     source         = Column(String(30))


class Record(Base):
     __tablename__ = "records"

     id             = Column(String(30), primary_key=True)
     category       = Column(String(30))
     num            = Column(Integer)

if __name__ == "__main__":
     engine = create_engine(sys.argv[1])

     Base.metadata.create_all(engine)
