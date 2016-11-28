import sqlalchemy
from ta_model import CATEGORIES, Article, Counter
import math
import pickle
import sys
import jieba
import numpy as np


if __name__ == "__main__":
    print("Article to vec calculating")

    engine = sqlalchemy.create_engine("mysql+mysqlconnector://root:root@127.0.0.1:3306/tencent_articles?charset=utf8")
    session = sqlalchemy.orm.sessionmaker(bind=engine)()

    count = session.query(Article).count()
    max_id = session.query(sqlalchemy.func.max(Article.id).label("max_id")).one_or_none().max_id
    min_id = session.query(sqlalchemy.func.min(Article.id).label("min_id")).one_or_none().min_id
    print(count, " ", min_id, " ", max_id)

    f = open("word_list.obj", "rb")
    word_list = pickle.load(f)
    f.close()
    WORD_SET = {}
    for i, w in enumerate(word_list):
        WORD_SET[w] = i

    art_mat = np.zeros((count, len(word_list)))
    cat_mat = np.zeros((count, 1))
    id_mat = np.zeros((count, 1))

    mat_idx = 0
    for id in range(1, max_id + 1):

        article = session.query(Article).filter(Article.id == id).one_or_none()
        if not article:
            continue

        id_mat[mat_idx] = id
        cat_mat[mat_idx] = CATEGORIES.index(article.category)

        seg_list = jieba.cut_for_search(article.content)
        for seg in seg_list:
            if seg not in WORD_SET:
                continue
            art_mat[mat_idx][WORD_SET[seg]] = 1

        mat_idx += 1

    f = open("article_mat.obj", "wb")
    pickle.dump((art_mat, cat_mat, id_mat), f)
    f.close()
