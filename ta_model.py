import sys

from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer, String, Date
from sqlalchemy.dialects.mysql import LONGTEXT
from sqlalchemy import create_engine

Base = declarative_base()


CATEGORIES = [
    "news",
    "army",
    "gnews",
    "sports",
    "ent",
    "finance",
    "tech",
    "games",
    "auto",
    "edu",
    "house"
]


class Article(Base):
     __tablename__ = "articles"
     id             = Column(Integer, primary_key=True, nullable=False,
                             unique=True, autoincrement=True)
     uid            = Column(String(30), unique=True, nullable=False)
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

     category       = Column(String(30), primary_key=True)
     date           = Column(Date)
     page           = Column(Integer)
     num            = Column(Integer)


class Counter(Base):
    __tablename__ = "counter"

    id              = Column(Integer, primary_key=True, nullable=False,
                             unique=True, autoincrement=True)
    word            = Column(String(20), nullable=False, unique=True)

    doc_num_news    = Column(Integer, nullable=False, default=0)
    doc_num_army    = Column(Integer, nullable=False, default=0)
    doc_num_gnews   = Column(Integer, nullable=False, default=0)
    doc_num_sports  = Column(Integer, nullable=False, default=0)
    doc_num_ent     = Column(Integer, nullable=False, default=0)
    doc_num_finance = Column(Integer, nullable=False, default=0)
    doc_num_tech    = Column(Integer, nullable=False, default=0)
    doc_num_games   = Column(Integer, nullable=False, default=0)
    doc_num_auto    = Column(Integer, nullable=False, default=0)
    doc_num_edu     = Column(Integer, nullable=False, default=0)
    doc_num_house   = Column(Integer, nullable=False, default=0)
    doc_num_total   = Column(Integer, nullable=False, default=0)

    word_num_news   = Column(Integer, nullable=False, default=0)
    word_num_army   = Column(Integer, nullable=False, default=0)
    word_num_gnews  = Column(Integer, nullable=False, default=0)
    word_num_sports = Column(Integer, nullable=False, default=0)
    word_num_ent    = Column(Integer, nullable=False, default=0)
    word_num_finance= Column(Integer, nullable=False, default=0)
    word_num_tech   = Column(Integer, nullable=False, default=0)
    word_num_games  = Column(Integer, nullable=False, default=0)
    word_num_auto   = Column(Integer, nullable=False, default=0)
    word_num_edu    = Column(Integer, nullable=False, default=0)
    word_num_house  = Column(Integer, nullable=False, default=0)
    word_num_total  = Column(Integer, nullable=False, default=0)


if __name__ == "__main__":
     engine = create_engine(sys.argv[1])

     Base.metadata.create_all(engine)