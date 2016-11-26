import sys
import sqlalchemy

import sqlalchemy.orm
import re

from model import Article

if __name__ == "__main__":
    engine = sqlalchemy.create_engine(sys.argv[1])
    session = sqlalchemy.orm.sessionmaker(bind=engine)()
    count = session.query(Article).count()
    print("Count: %d" % count)
    sum = 0
    id = 0
    for id in range(1, count+1):
        article = session.query(Article).filter(Article.id == id).one_or_none()
        if "return" in article.content and "this" in article.content and "var" in article.content:
            article.content = "".join(filter(lambda x: ord(x) > 127, article.content))
            session.commit()
            sum += 1
            if sum % 1000 == 0:
                print(sum)

        if id % 1000 == 0:
            print("ID: %d" % id)
    print("ID : %d" % id)
    print(sum)
    print("updated")
