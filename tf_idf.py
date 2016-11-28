import sqlalchemy
from ta_model import CATEGORIES, Article, Counter
import math
import pickle
import sys


if __name__ == "__main__":
    print("TF-IDF calculating")

    engine = sqlalchemy.create_engine(sys.argv[1])
    session = sqlalchemy.orm.sessionmaker(bind=engine)()

    count = session.query(Counter).count()
    max_id = session.query(sqlalchemy.func.max(Counter.id).label("max_id")).one_or_none().max_id
    min_id = session.query(sqlalchemy.func.min(Counter.id).label("min_id")).one_or_none().min_id
    print(count, " ", min_id, " ", max_id)

    tf = {}
    idf = {}
    total_tf = [0] * len(CATEGORIES)
    total_doc_num = 0

    for counter in session.query(Counter).all():

        tf[counter.word] = []
        for idx, cat in enumerate(CATEGORIES):
            tf[counter.word].append(getattr(counter, "word_num_%s" % cat))
            total_tf[idx] += getattr(counter, "word_num_%s" % cat)

        # idf[counter.word] = []
        # for cat in CATEGORIES:
            # idf[counter.word].append(math.log(getattr(counter, "doc_num_%s" % cat) + 1 / counter.doc_num_total))
        idf[counter.word] = counter.doc_num_total
        total_doc_num += counter.doc_num_total

    #calc tf

    for key, value in tf.items():
        for idx, _ in enumerate(value):
            tf[key][idx] = tf[key][idx] / total_tf[idx]

    #calc idf

    for key, value in tf.items():
        idf[key] = math.log(idf[key] / total_doc_num)

    tf_idf_map = []
    for id, cat in enumerate(CATEGORIES):
        tf_idf_map.append({})

    for key in tf:
        for idx in range(len(CATEGORIES)):
            tf_idf_map[idx][key] = tf[key][idx] * idf[key]

    WORD_SET = set()

    for idx in range(len(CATEGORIES)):
        l = list(tf_idf_map[idx].items())
        l.sort(key=lambda x: x[1], reverse=True)
        WORD_SET |= set(list(map(lambda x: x[0], l[:900])))
        # WORD_SET |= set(list(map(lambda x: x[0], l)))

    word_list = list(WORD_SET)
    word_list.sort()
    print(len(word_list))

    f = open("word_list.obj", "wb")
    pickle.dump(word_list, f)
    f.close()
