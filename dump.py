import sys
import sqlalchemy
import pickle

import sqlalchemy.orm
import re
import os

from ta_model import Article, Counter, traverse


if __name__ == "__main__":

    engine = sqlalchemy.create_engine(sys.argv[1])
    session = sqlalchemy.orm.sessionmaker(bind=engine)()

    for article in traverse(session, Article):
        f = open(
            "dump/%s/%s.txt" % (article.category, article.uid),
            "w",
            encoding="utf-8"
        )
        f.write(article.content)
        f.close()



