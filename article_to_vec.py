import sqlalchemy
from ta_model import CATEGORIES, Article, traverse
import math
import pickle
import sys
import numpy as np


if __name__ == "__main__":
    print("Article to vec calculating")

    engine = sqlalchemy.create_engine(sys.argv[1])
    session = sqlalchemy.orm.sessionmaker(bind=engine)()

    f = open("word_list.obj", "rb")
    word_list = pickle.load(f)
    f.close()
    WORD_SET = {}
    for i, w in enumerate(word_list):
        WORD_SET[w] = i

    count = session.query(Article).count()
    art_mat = np.zeros((count, len(word_list)))
    cat_mat = np.zeros((count, 1))
    id_mat = np.zeros((count, 1))
    print(count)

    mat_idx = 0
    for article in traverse(session, Article):
        id_mat[mat_idx] = article.id
        cat_mat[mat_idx] = CATEGORIES.index(article.category)

        seg_list = pickle.loads(article.content_cut)
        for seg in seg_list:
            if seg not in WORD_SET:
                continue
            art_mat[mat_idx][WORD_SET[seg]] = 1

        mat_idx += 1
        if mat_idx % 1000 == 0:
            print(mat_idx)

    f = open("article_mat.obj", "wb")
    pickle.dump((art_mat, cat_mat, id_mat), f)
    f.close()
