import sqlalchemy
import sqlalchemy.orm
import sqlalchemy.exc
import datetime

from model import Article, Record

LOG = None


class DBManager(object):

    def __init__(self, db_path, log):
        global LOG
        self.engine = sqlalchemy.create_engine(db_path, pool_recycle=200)
        self.session = sqlalchemy.orm.sessionmaker(bind=self.engine)()
        LOG = log

    def get_record(self, category):
        try:
            query = self.session.query(Record).filter(Record.category == category)
            if query.count() > 0:
                record = query[0]
            else:
                record = Record(
                    category=category,
                    date=datetime.datetime(year=2016, month=11, day=20),
                    page=1,
                    num=0
                )
                self.session.add(record)
                self.session.commit()
            return record
        except Exception as e:
            LOG.error("Check order failed. %s" % e)
            self.session.rollback()
        return 0, 0

    def update_record(self, record):
        while 1:
            try:
                self.session.add(record)
                self.session.commit()
                return record
                break

            except sqlalchemy.exc.OperationalError as e:
                LOG.error("Insert record failed operational error. Reason: %s. Record: %s" % (e, record_dict))
                self.session.rollback()
            except Exception as e:
                LOG.error("Insert record failed. Reason: %s. Record: %s" % (e, record_dict))
                self.session.rollback()
                break

    def insert_article(self, article_dict):
        while 1:
            try:
                article_obj = Article(
                    **article_dict
                )
                self.session.add(article_obj)
                self.session.commit()
                break

            except sqlalchemy.exc.IntegrityError as e:
                self.session.rollback()
                break
            except sqlalchemy.exc.OperationalError as e:
                LOG.error("Insert article failed operational error. Reason: %s. Record: %s" % (e, article_dict))
                self.session.rollback()
            except Exception as e:
                LOG.error("Insert article failed. Reason: %s. Artcile: %s" % (e, article_dict))
                self.session.rollback()
                break

