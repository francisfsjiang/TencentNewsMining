import sys
import sqlalchemy

import sqlalchemy.orm
import jieba
import re

from ta_model import Article, Counter

WORD_DICT = {}

STOP_WRODS = set()


def add_one(obj, name):
    if getattr(obj, name):
        setattr(obj, name,
                getattr(obj, name) + 1
                )
    else:
        setattr(obj, name, 1)


def seg_filter(word):
    seg = word.strip()
    if seg in STOP_WRODS:
        return False

    if len(list(filter(lambda x: (ord(x) > 57 or ord(x) < 48) and x != ".", seg))) == 0:
        return False

    return True

if __name__ == "__main__":

    f = open("stopwords.txt", "r", encoding="utf-8")
    for l in f.readlines():
        STOP_WRODS.add(
            l.strip()
        )
    f.close()
    STOP_WRODS.add(" ")

    engine = sqlalchemy.create_engine(sys.argv[1])
    session = sqlalchemy.orm.sessionmaker(bind=engine)()
    res = session.query(sqlalchemy.func.max(Article.id).label("max_id")).one_or_none()
    max_id = res.max_id
    print("Max id: %d" % max_id)
    sum = 0
    id = 0
    for id in range(1, max_id+1):
        print(id)
        article = session.query(Article).filter(Article.id == id).one_or_none()
        if not article:
            continue
        seg_list = jieba.cut_for_search(article.content)

        words_in_article = set()

        for seg in seg_list:
            if len(seg) > 20:
                continue
            seg = seg.lower()
            if not seg_filter(seg):
                continue
            if seg not in WORD_DICT:
                counter = Counter(
                    word=seg,
                    word_num_total=0,
                    doc_num_total=0,
                )
                WORD_DICT[seg] = counter
            else:
                counter = WORD_DICT[seg]

            add_one(counter, "word_num_%s" % article.category)
            counter.word_num_total += 1

            words_in_article.add(seg)

        for word in words_in_article:
            counter = WORD_DICT[word]
            add_one(counter, "doc_num_%s" % article.category)
            counter.doc_num_total += 1

        if id % 1000 == 0:
            print("ID: %d" % id)

    print("Word num: %d" % len(WORD_DICT))

    for counter in WORD_DICT.values():
        if counter.word_num_total < 100 or len(counter.word) <= 1:
            continue
        session.add(counter)
        session.commit()

