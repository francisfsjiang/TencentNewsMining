DROP DATABASE IF EXISTS tencent_articles;
CREATE DATABASE tencent_articles DEFAULT CHARSET utf8;

DROP TABLE IF EXISTS tencent_articles.articles;
CREATE TABLE tencent_articles.articles (
  id           VARCHAR(20) NOT NULL PRIMARY KEY ,
  category     VARCHAR(20),
  sub_category VARCHAR(20),
  date         VARCHAR(20),
  href         VARCHAR(40),
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