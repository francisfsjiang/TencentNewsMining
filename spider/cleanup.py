import sys
import sqlalchemy

import sqlalchemy.orm
import re

from ta_model import Article


Key = [ "return", "this", "var", "undefined", "list", "display","padding","margin", ]


if __name__ == "__main__":
    engine = sqlalchemy.create_engine(sys.argv[1])
    session = sqlalchemy.orm.sessionmaker(bind=engine)()
    res = session.query(sqlalchemy.func.max(Article.id).label("max_id")).one_or_none()
    print("Max id: %d" %res.max_id)
    sum = 0
    id = 0
    for id in range(1, res.max_id+1):
        print(id)
        article = session.query(Article).filter(Article.id == id).one_or_none()
        if not article:
            continue
        for w in Key:
            if w in article.content:
                article.content = "".join(filter(lambda x: ord(x) > 127, article.content))
                session.commit()
                sum += 1
                if sum % 1000 == 0:
                    print(sum)
                break

        if id % 1000 == 0:
            print("ID: %d" % id)
    print("ID : %d" % id)
    print(sum)
    print("updated")
