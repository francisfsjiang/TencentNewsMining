import sys
import sqlalchemy
import sqlalchemy.orm
import re

from model import Article

if __name__ == "__main__":
    engine = sqlalchemy.create_engine(sys.argv[1], pool_recycle=200)
    session = sqlalchemy.orm.sessionmaker(bind=engine)()

    sum = 0
    for article in session.query(Article).all():
        if "return" in article.content and "this" in article.content and "var" in article.content:
            article.content = "".join(filter(lambda x: ord(x) > 127, article.content))
            session.commit()
            sum += 1
            if sum % 1000 == 0:
                print(sum)

    print(sum)
    print("updated")
