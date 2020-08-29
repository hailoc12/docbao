import copy
from datetime import datetime
from elasticsearch_dsl import *
from elasticsearch_dsl.connections import connections
import os

HOST = os.environ['DOCBAO_ELASTICSEARCH_HOST']

class Content(InnerDoc):
    type = Text()
    content = Text()
    link = Text()

class Image(InnerDoc):
    small = Text()
    large = Text()

class Elastic_Article(Document):
    article_id = Text()
    topic = Text()
    href = Text()
    publish_date = Date()
    newspaper = Text()
    created_date = Date()
    language = Text()
    sapo = Text()
    content = Nested(Content)
    feature_image = Text()
    avatar = Text()
    tags = Text()

    class Index:
        name="newspaper_news"
        settings = {
			"number_of_shards": 1,
        }

    def from_article(self, article):
        self.topic = article.get_topic()
        self.href = article.get_href()
        self.newspaper = article.get_newspaper()
        self.publish_date = article.get_date()
        self.created_date = article.get_creation_date()
        self.language = article.get_language()
        self.sapo = article.get_sapo()
        # use deepcopy to prevent changing article object to Elasticsearch object
        self.content = copy.deepcopy(article.get_content())
        self.feature_image = copy.deepcopy(article.get_feature_image())
        self.avatar = article.get_avatar()
        self.tags = article.get_tags()
        self.article_id = article.get_id()

    def save(self, **kwargs):
        return super(Elastic_Article, self).save(**kwargs)
    
    def get_topic(self):
        return self.topic

class ElasticSearch_Client:
# This class handle converting normal Article to ElasticSearch Article
	def __init__(self):
		# Create connection to Elasticsearch
		connections.create_connection(hosts=[HOST], timeout=20)
		# Check if index articles existed
		index = Index("newspaper_news")
		if not index.exists():
			Elastic_Article.init() # create new index

	def push_article(self, article):
		# push article to Elasticsearch
		elastic_article = Elastic_Article()
		elastic_article.from_article(article) # convert article to elastic_article
		elastic_article.save()
		
