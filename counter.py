import sys
import sqlalchemy

import sqlalchemy.orm
import jieba
import re

from ta_model import Article, Counter

WORD_DICT = {}

STOP_WRODS = set()


def add_one(obj, name):
    setattr(obj, name,
            getattr(obj, name) + 1
            )

def seg_filter(seg):
    if seg in STOP_WRODS:
        return False



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
    count = session.query(Article).count()
    print("Count: %d" % count)
    sum = 0
    id = 0
    for id in range(1, count+1):
        print(id)
        article = session.query(Article).filter(Article.id == id).one_or_none()
        if not article:
            continue
        seg_list = jieba.cut_for_search(article.content)

        words_in_article = set()

        for seg in seg_list:
            if seg == "innerHTML":
                exit(-1)
            else:
                continue
            if seg_filter(seg):
                continue
            if seg not in WORD_DICT:
                counter = session.query(Counter).filter(Counter.word == seg).one_or_none()
                if not counter:
                    counter = Counter(
                        word=seg
                    )
                    session.add(counter)
                    session.commit()

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

    for counter in WORD_DICT.values():
        session.add(counter)
        session.commit()

    print("ID : %d" % id)
    print(sum)
    print("updated")
