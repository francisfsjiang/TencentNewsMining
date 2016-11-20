import requests
import random
import datetime
import json
import bs4
import re
import logging
import sys
import os
import multiprocessing

from db_manager import DBManagerMysql

TIME_FORMAT = "%Y-%m-%d"
ID_EXTRACTOR = re.compile(r"http://[\w]*.qq.com/a/([\d]*)/([\d]*).htm")

CATEGORY_INFO = [
    ("news", "news", ["newsgn", "newssh"], "http://roll.%(category)s.qq.com/interface/roll.php?0.%(rand_num)d&cata=%(sub_cats)s&site=%(category)s&date=%(date)s&page=%(page_num)d&mode=2&of=json"),
    ("army", "news", ["milite"], "http://roll.%(category)s.qq.com/interface/roll.php?0.%(rand_num)d&cata=%(sub_cats)s&site=%(category)s&date=%(date)s&page=%(page_num)d&mode=2&of=json"),
    ("gnews", "news", ["newsgj"], "http://roll.%(category)s.qq.com/interface/roll.php?0.%(rand_num)d&cata=%(sub_cats)s&site=%(category)s&date=%(date)s&page=%(page_num)d&mode=2&of=json"),
    ("sports", "sports", [], "http://roll.%(category)s.qq.com/interface/roll.php?0.%(rand_num)d&cata=%(sub_cats)s&site=%(category)s&date=%(date)s&page=%(page_num)d&mode=2&of=json"),
    ("ent", "ent", [], "http://roll.%(category)s.qq.com/interface/roll.php?0.%(rand_num)d&cata=%(sub_cats)s&site=%(category)s&date=%(date)s&page=%(page_num)d&mode=2&of=json"),
    ("finance", "finance", [], "http://roll.%(category)s.qq.com/interface/roll.php?0.%(rand_num)d&cata=%(sub_cats)s&site=%(category)s&date=%(date)s&page=%(page_num)d&mode=2&of=json"),
    ("tech", "tech", [], "http://roll.%(category)s.qq.com/interface/roll.php?0.%(rand_num)d&cata=%(sub_cats)s&site=%(category)s&date=%(date)s&page=%(page_num)d&mode=2&of=json"),
    ("games", "games", [], "http://roll.%(category)s.qq.com/interface/roll.php?0.%(rand_num)d&cata=%(sub_cats)s&site=%(category)s&date=%(date)s&page=%(page_num)d&mode=2&of=json"),
    ("auto", "auto", [], "http://roll.%(category)s.qq.com/interface/roll.php?0.%(rand_num)d&cata=%(sub_cats)s&site=%(category)s&date=%(date)s&page=%(page_num)d&mode=2&of=json"),
    ("edu", "edu", [], "http://roll.%(category)s.qq.com/interface/roll.php?0.%(rand_num)d&cata=%(sub_cats)s&site=%(category)s&date=%(date)s&page=%(page_num)d&mode=2&of=json"),
    ("house", "house", [], "http://roll.%(category)s.qq.com/interface/roll.php?0.%(rand_num)d&cata=%(sub_cats)s&site=%(category)s&date=%(date)s&page=%(page_num)d&mode=2&of=json"),
]


def get_article_content(url):
    try:
        r = requests.get(url)
        soup = bs4.BeautifulSoup(r.text, "html5lib")
        art_div = soup.find("div", id="Cnt-Main-Article-QQ")
        source_span = soup.find(attrs={"bosszone": "jgname"})
        content = "".join(art_div.stripped_strings)
        source = "".join(source_span.stripped_strings)

        return content, source

    except Exception as e:
        return None, None


def get_page(cat_info, session, date, page_num, db_manager):
    rand_num = random.randrange(0, 10 ** 16 - 1)
    u = cat_info["url_template"] % {
        "category": cat_info["root_cat"],
        "rand_num": rand_num,
        "sub_cats": cat_info["sub_cats"],
        "date": date,
        "page_num": page_num
    }
    try:
        r = session.get(u)

        j = json.loads(r.text)
        if j["response"]["code"] != '0':
            return 0, 0
        soup = bs4.BeautifulSoup(j["data"]["article_info"], "html5lib")

        page_count = j["data"]["count"]

        article_num = 0

        for c in soup.find(name="body").children:

            article = {}
            try:
                article["category"] = cat_info["name"]
                article["sub_category"] = c.find("span", "t-tit").string.strip("[]")
                article["date"] = str(c.find("span", "t-time").string)
                article["title"] = str(c.find("a", ).string)
                article["href"] = c.find("a", )["href"]
                article["summary"] = list(c.find("dd", ).stripped_strings)[0]
                article["id"] = cat_info["name"] + "-" + "-".join(ID_EXTRACTOR.match(article["href"]).groups())
                article["content"], article["source"] = get_article_content(article["href"])
                if article["content"]:
                    # articles.append(article)
                    db_manager.insert_article(article)
                    article_num += 1

            except Exception as e:
                if article:
                    print("Failed in handling reason:%s, html:%s" % (e, article))
                else:
                    print("Failed in handling reason:%s" % (e,))
        # LOG.info("Get %d articles in page %d, on %s" % (article_num, page_num, date))
        return page_count, article_num

    except Exception as e:
        print("Failed in gat:%s date:%s page:%d, reason:%s" % (cat_info["name"], date, page_num, e))
        return 0, 0


def worker(cat_index):
    # global LOG
    cat_info = {
        "name": CATEGORY_INFO[cat_index][0],
        "root_cat": CATEGORY_INFO[cat_index][1],
        "sub_cats": ",".join(CATEGORY_INFO[cat_index][2]),
        "url_template": CATEGORY_INFO[cat_index][3],
    }

    # LOG = logging.getLogger(cat_info["name"])
    # LOG.setLevel(logging.DEBUG)
    # 
    # file_handler = logging.FileHandler(filename=os.path.join(sys.argv[2], cat_info["name"] + ".log"), encoding="utf-8")
    # file_handler.setLevel(logging.DEBUG)
    # formatter = logging.Formatter('%(asctime)s - %(processName)-7s - %(levelname)s - %(message)s')
    # file_handler.setFormatter(formatter)
    # LOG.addHandler(file_handler)
    # 
    # stream_handler = logging.StreamHandler(sys.stderr)
    # stream_handler.setLevel(logging.ERROR)
    # stream_handler.setFormatter(formatter)
    # LOG.addHandler(stream_handler)
    # 
    # LOG.info(cat_info["name"])
    # LOG.info(cat_info)

    db_manager = DBManagerMysql(sys.argv[1])

    session = requests.session()
    session.headers.update({
        "User-agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10.12; rv:49.0) Gecko/20100101 Firefox/49.0",
        "Referer": "http://roll.%s.qq.com/index.htm" % cat_info["root_cat"]
    })

    day = datetime.datetime(year=2016, month=11, day=19)

    cat_info["num"] = 0

    while cat_info["num"] < 30000:
        # LOG.info(day.strftime(TIME_FORMAT))

        record_id = cat_info["name"] + "-" + day.strftime(TIME_FORMAT)

        # skip this day
        try:
            result, query_num = db_manager.has_order(record_id)
            if result > 0:
                # LOG.info("Skip day %s" % day.strftime(TIME_FORMAT))
                day -= datetime.timedelta(days=1)
                cat_info["num"] += query_num
                continue
            article_num = 0

            page_count, tmp_article_num = get_page(
                cat_info,
                session,
                day.strftime(TIME_FORMAT),
                1,
                db_manager
            )
            article_num += tmp_article_num

            for i in range(page_count - 1):
                _, tmp_article_num = get_page(
                    cat_info,
                    session,
                    day.strftime(TIME_FORMAT),
                    2 + i,
                    db_manager
                )
                article_num += tmp_article_num

            new_record = {
                "id": record_id,
                "category": cat_info["name"],
                "num": article_num,
            }
            db_manager.insert_record(new_record)

            cat_info["num"] += article_num

            # LOG.info("Get %d articles on %s, total %d" % (article_num, day.strftime(TIME_FORMAT), cat_info["num"]))
        except Exception as e:
            print("Failed in gat:%s date:%s,reason: %s" % (cat_info["name"], day.strftime(TIME_FORMAT), e))

        day -= datetime.timedelta(days=1)


if __name__ == "__main__":

    processes = []

    # idx = 7
    # threads.append(
    #     threading.Thread(
    #         target=worker,
    #         args=(idx,),
    #         name=CATEGORY_INFO[idx][0]
    #     )
    # )

    for idx in range(len(CATEGORY_INFO)):
        processes.append(
            multiprocessing.Process(
                target=worker,
                args=(idx, ),
                name=CATEGORY_INFO[idx][0]
            )
        )

    for p in processes:
        p.start()

    for p in processes:
        p.join()
