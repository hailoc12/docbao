from elasticsearch_dsl import *
from elasticsearch_dsl.connections import connections
from datetime import datetime
from lib.data import *

class Elastic_Article(Document):
	topic = Text()
	href = Text()
	publish_date = Date()
	newspaper = Text()
	created_date = Date()
	language = Text()

	class Index:
		name="docbao"
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
	
	def save(self, **kwargs):
		return super(Elastic_Article, self).save(**kwargs)

	def get_topic(self):
		return self.topic

class ElasticSearch_Client:
# This class handle converting normal Article to ElasticSearch Article
	def __init__(self):
		# Create connection to Elasticsearch
		connections.create_connection(hosts=['localhost'], timeout=20)
		# Check if index articles existed
		index = Index("docbao")
		if not index.exists():
			Elastic_Article.init() # create new index

	def put_article(self, article):
		# put article to Elasticsearch
		elastic_article = Elastic_Article()
		elastic_article.from_article(article) # convert article to elastic_article
		elastic_article.save()
		
