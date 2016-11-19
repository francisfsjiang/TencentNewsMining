DROP DATABASE IF EXISTS tencent_articles;
CREATE DATABASE tencent_articles DEFAULT CHARSET utf8;

DROP TABLE IF EXISTS tencent_articles.articles;
CREATE TABLE tencent_articles.articles (
  id           VARCHAR(40) NOT NULL PRIMARY KEY ,
  category     VARCHAR(40),
  sub_category VARCHAR(40),
  date         VARCHAR(40),
  href         VARCHAR(100),
  title        TEXT,
  summary      TEXT,
  content      TEXT
);

DROP TABLE IF EXISTS tencent_articles.record;
CREATE TABLE tencent_articles.record (
  id           VARCHAR(20) NOT NULL PRIMARY KEY ,
  category     VARCHAR(20),
  num          INTEGER
)
