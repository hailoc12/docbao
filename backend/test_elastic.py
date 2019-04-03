from lib.data import *
from lib.elasticsearch_data import *
import random
from datetime import datetime
import json

es = ElasticSearch_Client()
id = random.randint(0, 10000)
article = Article(article_id=id, topic="test2", newspaper="Bao Lao Dong", href="http://hailoc.com", date=datetime.now(), language="vietnamese")
print(json.dumps(article.get_date().strftime("%Y-%m-%dT%H:%M:%S")))
print(json.dumps(article.get_creation_date().strftime("%Y-%m-%dT%H:%M:%S")))
es.put_article(article)


