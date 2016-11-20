import sqlalchemy
import sqlalchemy.orm
import sqlalchemy.exc

from model import Article, Record

LOG = None


class DBManager(object):

    def __init__(self, db_path, log):
        global LOG
        self.engine = sqlalchemy.create_engine(db_path, pool_recycle=200)
        self.session = sqlalchemy.orm.sessionmaker(bind=self.engine)()
        LOG = log

    def has_order(self, record_id):
        try:
            query = self.session.query(Record).filter(Record.id == record_id)
            if query.count() > 0:
                return query.count(), int(query[0].num)
        except Exception as e:
            LOG.error("Check order failed. %s" % e)
        return 0, 0

    def insert_article(self, article_dict):
        try:
            article_obj = Article(
                **article_dict
            )
            self.session.add(article_obj)
            self.session.commit()

        except sqlalchemy.exc.IntegrityError as e:
            self.session.rollback()
        except Exception as e:
            LOG.error("Insert article failed. Reason: %s. Artcile: %s" % (e, article_dict))
            self.session.rollback()

    def insert_record(self, record_dict):
        try:
            article_obj = Record(
                **record_dict
            )
            self.session.add(article_obj)
            self.session.commit()

        except sqlalchemy.exc.IntegrityError as e:
            self.session.rollback()
        except Exception as e:
            LOG.error("Insert record failed. Reason: %s. Record: %s" % (e, record_dict))
            self.session.rollback()
