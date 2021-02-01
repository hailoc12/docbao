###################################################################
# File: postgresql_client.py
# Function: Save crawled article in PosgreSQL database
# Created: 30/01/2021
# Author: hailoc12
###################################################################

import datetime
import random
import os
from sqlalchemy import create_engine
from sqlalchemy import Column, String, Date
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import composite, sessionmaker
from src.backend.lib.data import Article

POSTGRES_USERNAME = os.environ['DOCBAO_POSTGRES_USERNAME']
POSTGRES_PASSWORD = os.environ['DOCBAO_POSTGRES_PASSWORD']
POSTGRES_DB       = os.environ['DOCBAO_POSTGRES_DATABASE']
POSTGRES_HOST     = os.environ['DOCBAO_POSTGRES_HOST']
POSTGRES_PORT     = os.environ['DOCBAO_POSTGRES_PORT']

sqlalchemy_base = declarative_base()

class Postgres_Article(sqlalchemy_base):
    __tablename__ = POSTGRES_DB
    article_id = Column(String, primary_key=True)
    topic = Column(String)
    href = Column(String)
    publish_date = Column(Date)
    newspaper = Column(String)
    created_date = Column(Date)
    language = Column(String)
    sapo = Column(String)
    content = Column(String) # full content
    feature_image = Column(String)

class PostgresClient():
    def __init__(self):
        db_string = f"postgres://{POSTGRES_USERNAME}:{POSTGRES_PASSWORD}@{POSTGRES_HOST}:{POSTGRES_PORT}/{POSTGRES_DB}"
        db = create_engine(db_string)
        Session = sessionmaker(db)
        self._session = Session()
        sqlalchemy_base.metadata.create_all(db)

    def push_article(self, article):
        new_article = Postgres_Article(
            article_id = article.get_id(),
            topic = article.get_topic(),
            href  = article.get_href(),
            publish_date = article.get_date(),
            newspaper = article.get_newspaper(),
            created_date = article.get_creation_date(),
            language = article.get_language(),
            sapo = article.get_sapo(),
            content = article.get_full_content(),
            feature_image = article.get_feature_image(),
        )

        self._session.add(new_article)
        self._session.commit()

    def get_sample_articles(self):
        for article in self._session.query(Postgres_Article):
            print(f"Title: {article.topic}")
            print(f"Newpspaper: {article.newspaper}")
            print(f"Link: {article.href}")
            print(f"Publish date: {article.publish_date}")
            print(f"Crawled date: {article.created_date}")
            print(f"Sapo: {article.sapo}")
            print(f"Feature_image: {article.feature_image}")
            print(f"Content: {article.content}")
            print()

            input("Press Enter to print next article !")
            print()


# UNIT TEST
if __name__ == '__main__':
    print("Testing Postgres_client module")
    sample_article = Article(
        article_id = random.randint(0, 1000000),
        href = 'https://test.com',
        topic = 'day la bai test',
        date = None,
        newspaper = 'bao dantri',
        language = 'vietnamese',
        sapo = 'day la gioi thieu',
        content = [{
            'type': "text",
            "content": "noi dung test"
        }],
        feature_image = 'https://test.com',
        avatar = '',
        post_type=0,
    )
    print("Test push a sample article")
    db = PostgresClient()
    db.push_article(sample_article)
    print("OK")

    print("Test list articles in database")
    db.get_sample_articles()
    print("OK")

