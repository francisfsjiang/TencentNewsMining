import requests
import random
import datetime
import json
import bs4
import re
import pymongo
import pymongo.errors
import logging
import threading

TIME_FORMAT = "%Y-%m-%d"
ID_EXTRACTOR = re.compile(r"http://[\w]*.qq.com/a/([\d]*)/([\d]*).htm")
MONGODB_HOST = "localhost"
MONGODB_PORT = 27017

LOG = None

CATEGORY_INFO = [
    ("news",    "news",    ["newsgn", "newssh"], "http://roll.%(category)s.qq.com/interface/roll.php?0.%(rand_num)d&cata=%(sub_cats)s&site=%(category)s&date=%(date)s&page=%(page_num)d&mode=2&of=json"),
    ("army",    "news",    ["milite"],           "http://roll.%(category)s.qq.com/interface/roll.php?0.%(rand_num)d&cata=%(sub_cats)s&site=%(category)s&date=%(date)s&page=%(page_num)d&mode=2&of=json"),
    ("gnews",   "news",    ["newsgj"],           "http://roll.%(category)s.qq.com/interface/roll.php?0.%(rand_num)d&cata=%(sub_cats)s&site=%(category)s&date=%(date)s&page=%(page_num)d&mode=2&of=json"),
    ("sports",  "sports",  [],                   "http://roll.%(category)s.qq.com/interface/roll.php?0.%(rand_num)d&cata=%(sub_cats)s&site=%(category)s&date=%(date)s&page=%(page_num)d&mode=2&of=json"),
    ("ent",     "ent",     [],                   "http://roll.%(category)s.qq.com/interface/roll.php?0.%(rand_num)d&cata=%(sub_cats)s&site=%(category)s&date=%(date)s&page=%(page_num)d&mode=2&of=json"),
    ("finance", "finance", [],                   "http://roll.%(category)s.qq.com/interface/roll.php?0.%(rand_num)d&cata=%(sub_cats)s&site=%(category)s&date=%(date)s&page=%(page_num)d&mode=2&of=json"),
    ("tech",    "tech",    [],                   "http://roll.%(category)s.qq.com/interface/roll.php?0.%(rand_num)d&cata=%(sub_cats)s&site=%(category)s&date=%(date)s&page=%(page_num)d&mode=2&of=json"),
    ("games",   "games",   [],                   "http://roll.%(category)s.qq.com/interface/roll.php?0.%(rand_num)d&cata=%(sub_cats)s&site=%(category)s&date=%(date)s&page=%(page_num)d&mode=2&of=json"),
    ("auto",    "auto",    [],                   "http://roll.%(category)s.qq.com/interface/roll.php?0.%(rand_num)d&cata=%(sub_cats)s&site=%(category)s&date=%(date)s&page=%(page_num)d&mode=2&of=json"),
    ("edu",     "edu",     [],                   "http://roll.%(category)s.qq.com/interface/roll.php?0.%(rand_num)d&cata=%(sub_cats)s&site=%(category)s&date=%(date)s&page=%(page_num)d&mode=2&of=json"),
    ("house",   "house",   [],                   "http://roll.%(category)s.qq.com/interface/roll.php?0.%(rand_num)d&cata=%(sub_cats)s&site=%(category)s&date=%(date)s&page=%(page_num)d&mode=2&of=json"),
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

    except:
        return None, None


def get_page(cat_info, session, date, page_num, articles_col):

    rand_num = random.randrange(0, 10**16 - 1)
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
            return [], 0
        soup = bs4.BeautifulSoup(j["data"]["article_info"], "html5lib")

        page_count = j["data"]["count"]

        article_num = 0

        for c in soup.find(name="body").children:

            article = {
                "category": cat_info["name"],
                "sub_category": c.find("span", "t-tit").string.strip("[]"),
                "date": c.find("span", "t-time").string,
                "title": c.find("a", ).string,
                "href": c.find("a", )["href"],
                "summary": list(c.find("dd", ).stripped_strings)[0],
            }

            article["id"] = cat_info["name"] + "-" + "-".join(ID_EXTRACTOR.match(article["href"]).groups())
            article["content"], article["source"] = get_article_content(article["href"])
            if article["content"]:
                # articles.append(article)
                article_num += 1
                try:
                    articles_col.insert(article)
                except pymongo.errors.DuplicateKeyError:
                    continue
        LOG.info("Get %d articles in page %d, on %s" % (article_num, page_num, date))
        return page_count, article_num

    except Exception as e:
        LOG.error("Failed in cat:%s date:%s page:%d, reason:%s" % (cat_info["name"], date, page_num, e))
        return [], 0


def worker(cat_index):

    db = pymongo.MongoClient(MONGODB_HOST, MONGODB_PORT).tencent_articles
    articles_col = db.articles
    record_col = db.record

    cat_info = {
        "name": CATEGORY_INFO[cat_index][0],
        "root_cat": CATEGORY_INFO[cat_index][1],
        "sub_cats": ",".join(CATEGORY_INFO[cat_index][2]),
        "url_template": CATEGORY_INFO[cat_index][3],
    }
    LOG.info(cat_info["name"])
    LOG.info(cat_info)

    session = requests.session()
    session.headers.update({
        "User-agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10.12; rv:49.0) Gecko/20100101 Firefox/49.0",
        "Referer": "http://roll.%s.qq.com/index.htm" % cat_info["root_cat"]
    })

    day = datetime.datetime(year=2016, month=11, day=18)
    record_col.find({"category": cat_info["name"]})

    cat_info["num"] = 0

    while cat_info["num"] < 30000:
        logging.info(day.strftime(TIME_FORMAT))

        record_id = cat_info["name"] + "-" + day.strftime(TIME_FORMAT)

        # skip this day
        try:
            doc = record_col.find_one({"id": record_id})
            if doc:
                LOG.info("Skip day %s" % day.strftime(TIME_FORMAT))
                day -= datetime.timedelta(days=1)
                cat_info["num"] += int(doc["num"])
                continue

            article_num = 0

            page_count, tmp_article_num = get_page(
                cat_info,
                session,
                day.strftime(TIME_FORMAT),
                1,
                articles_col
            )
            article_num += tmp_article_num

            for i in range(page_count - 1):
                _, tmp_article_num = get_page(
                    cat_info,
                    session,
                    day.strftime(TIME_FORMAT),
                    2 + i,
                    articles_col
                )
                article_num += tmp_article_num

            record_col.insert({
                "id": record_id,
                "category": cat_info["name"],
                "num": article_num
            })
            cat_info["num"] += article_num

            LOG.info("Get %d articles on %s, total %d" % (article_num, day.strftime(TIME_FORMAT), cat_info["num"]))
        except Exception as e:
            LOG.error("Failed in cat:%s date:%s,reason: %s" % (cat_info["name"], day.strftime(TIME_FORMAT), e))

        day -= datetime.timedelta(days=1)


if __name__ == "__main__":

    LOG = logging.getLogger('ta')
    LOG.setLevel(logging.DEBUG)

    ch = logging.FileHandler(filename="log.log")
    ch.setLevel(logging.DEBUG)
    formatter = logging.Formatter('%(asctime)s - %(threadName)-7s - %(levelname)s - %(message)s')
    ch.setFormatter(formatter)
    LOG.addHandler(ch)

    process = []
    for idx in range(len(CATEGORY_INFO)):
        process.append(
            threading.Thread(
                target=worker,
                args=(idx, ),
                name=CATEGORY_INFO[idx][0]
            )
        )

    for p in process:
        p.start()

    for p in process:
        p.join()

