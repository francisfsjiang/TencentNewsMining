import sqlalchemy
import sys
import jieba
import pickle

from ta_model import Article, traverse

if __name__ == "__main__":

    engine = sqlalchemy.create_engine(sys.argv[1])
    session = sqlalchemy.orm.sessionmaker(bind=engine)()

    for article in traverse(session, Article):
        print(article.id)
        seg_list = jieba.cut(article.content, cut_all=False)
        s = pickle.dumps(list(seg_list))
        article.content_cut = s
        session.add(article)
        session.commit()
