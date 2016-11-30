import sqlalchemy
from ta_model import Article, traverse
import math
import h5py
import pickle
import sys
import numpy as np

CATEGORIES = [
    "news",
    "army",
    "gnews",
    "sports",
    "ent",
    "tech",
    "games",
    "auto",
    "edu",
    "house"
]

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
        if article.category not in CATEGORIES:
            continue
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

    file = h5py.File('article_mat.h5', 'w')
    file.create_dataset('art_mat', data=art_mat)
    file.create_dataset('cat_mat', data=cat_mat)
    file.create_dataset('id_mat', data=id_mat)
    file.close()
