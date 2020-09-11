################################################################################
#Library: Bangtin RabbitMQ client
#Function: Push crawled news to RabbitMQ queues
#Created date: 2019-07-10                                                      #
#################################################################################

import jsonpickle
import os
import pika
import pytz
from random import randint
from src.backend.lib.utils import get_independent_os_path, open_utf8_file_to_read, try_download

# Rabbit MQ Username
HOST = os.environ['DOCBAO_RABBITMQ_HOST']
USERNAME = os.environ['DOCBAO_RABBITMQ_USERNAME']
PASSWORD = os.environ['DOCBAO_RABBITMQ_PASSWORD']
EXCHANGE = os.environ['DOCBAO_RABBITMQ_EXCHANGE']
DEFAULT_QUEUE = os.environ['DOCBAO_RABBITMQ_DEFAULT_QUEUE']

# Represent a post
class Post():

    def __init__(self, article):
    # Function
    # --------
    # Turn article to post format
        self._data = {}
        if article.get_author_id() is None:
            self._data['authorId'] = article.get_newspaper()
        else:
            self._data['authorId'] = article.get_author_id()
        self._data['id'] = article.get_id()
        post_type = article.get_post_type()
        if post_type == 0: # newspaper
            self._data['title'] = article.get_topic()
            self._data['displayType'] = 0
            self._data['url'] = article.get_href()
            if len(article.get_feature_image()) > 0:
                # feature_image = article.get_feature_image()
                feature_image = article.get_all_image()
                if feature_image:
                    for image in feature_image:
                        if image.strip() != '':
                            if try_download(image): # make sure that this image link can be downloaded
                                self._data['featureImages'] = [image]
                                break
                else:
                    pass # no featureImages field

            self._data['content'] = [{'type':'text', 'content': article.get_sapo()}]

            for item in article.get_content():
                self._data['content'].append(item)
        else: # mxh
            self._data['displayType'] = 1
            if len(article.get_feature_image()) == 0:
                pass # no featureImages
            else:
                self._data['featureImages'] = article.get_feature_image()
            self._data['content'] = article.get_content()[0]['content']

        self._data['categories'] = ['kinhte', 'thoisu', 'vanhoa', 'xahoi', 'khcn', 'taichinh', 'phapluat']

        tags = []
        for tag in article.get_keywords():
            tags.append({'tag':tag, 'point': randint(1,  10)})
        self._data['tag'] = tags
        self._data['createdAt'] = article.get_creation_date_string(pytz.timezone("UTC"), "%Y-%m-%dT%H:%M:%S.%fZ")
        self._data['publish_date'] = article.get_date_string(pytz.timezone("UTC"), "%Y-%m-%dT%H:%M:%S.%fZ")

        # NOTE: below fields are used only for middleware processing and will be ignore when pushing to frontend
        self._data['avatar'] = article.get_avatar()
        self._data['author_fullname'] = article.get_author_fullname()

    def get_body(self):
        # function
        # --------
        # get post data in json format (byte string)
        return jsonpickle.dumps(self._data)

    def get_post_id(self):
        return self._data['id']

    def get_author_id(self):
        return self._data['authorId']

    def get_title(self):
        if 'title' not in self._data:
            return None
        else:
            return self._data['title']

    def get_displayType(self):
        return self._data['displayType']

    def get_tags(self):
        return self._data['tag']

    def get_first_image(self):
        for item in self.get_content():
            if item['type'] == 'image':
                return item['link']
        return None

    def get_featureImages(self):
        return self._data['featureImages']

    def get_create_date(self):
        return self._data['createdAt']

    def get_categories(self):
        return self._data['categories']

    def get_content(self):
        return self._data['content']

    def reformat_content(self):
        content = self.get_content()
        self._data['content'] = {'type':'text', 'content': content}

class RabbitMQ_Client():
    def push_to_queue(self, articles):
        # Push post to newspaper, kols, analysis queue
        # Input
        # -------
        # articles: list of article object

        connection = self._connection

        # get queues
        newspaper_queue = DEFAULT_QUEUE
        exchange = EXCHANGE
        kol_queue = 'kol_news'

        channel = connection.channel()
        channel.exchange_declare(exchange=EXCHANGE, exchange_type='fanout') 
        channel.queue_declare(newspaper_queue, durable=True)
        channel.queue_bind(exchange=EXCHANGE, queue=newspaper_queue)

        # channel.queue_declare(kol_queue, durable=True)

        # push post
        for article in articles:
            post = Post(article)
            post_body = post.get_body()
            if article.get_post_type() == 0:
                #newspaper

                # push post to exchange and save in default_queue
                channel.basic_publish(exchange=EXCHANGE,
                                  routing_key='',
                                  body=post_body)
            else:
                channel.basic_publish(exchange='',
                                  routing_key=kol_queue,
                                  body=post_body)

    def create_queue(self, queue_name):
        channel = self._connection.channel()
        channel.queue_declare(queue_name, durable=True)

    def delete_queue(self, queue_name):
        channel = self._connection.channel()
        channel.queue_delete(queue_name)

    def connect(self, host='', username='', password='', port=''):
        # connect to RabbitMQ
        host = HOST
        username = USERNAME
        password = PASSWORD

        # login
        credentials = pika.PlainCredentials(username, password)
        parameters = pika.ConnectionParameters(host, 5672,'/', credentials)
        connection = pika.BlockingConnection(parameters)

        self._connection = connection

    def push_baonoi_task_to_queue(self, task_body, task_queue):
        channel = self._connection.channel()
        queue_name = task_queue
        queue_state = channel.queue_declare(queue_name, durable=True)
        data = task_body
        body = jsonpickle.dumps(data)
        channel.basic_publish(exchange='',
                              routing_key=queue_name,
                              body=body)

    def push_random_kols_to_queue(self, base_path = '..', number = 300):
        print("Push %s random kols id to smcc service to get their post in the next crawl" % str(number))
        channel = self._connection.channel()
        queue_name = 'facebook_scanning'
        queue_state = channel.queue_declare(queue_name, durable=True)

        with open_utf8_file_to_read(get_independent_os_path([base_path, 'backend', 'input', 'kols_list.txt'])) as stream:
            kols_list = [x.strip() for x in stream.read().split('\n') if x.strip() != '']
        choosen = set()
        count = 0
        number_of_kols = len(kols_list)
        while count < number:
            index = randint(0, number_of_kols-1)
            kol_id = kols_list[index]
            if kol_id not in choosen:
                choosen.add(kol_id)
                count+=1

        for kol_id in choosen:
            body = kol_id
            print(kol_id)
            channel.basic_publish(exchange='',
                                  routing_key=queue_name,
                                  body=body)

    def get_baonoi_notification_from_queue(self, queue_name):
        # get queue
        channel = self._connection.channel()
        queue_state = channel.queue_declare(queue_name, durable=True)
        queue_length = queue_state.method.message_count

        messages = []
        while (queue_length > 0):
            method, properties, body = channel.basic_get(queue_name, auto_ack=True)
            queue_length -= 1
            if body is not None:
                #print(body)
                messages.append(jsonpickle.decode(str(body, encoding='utf-8')))
        return messages


    def get_kols_post_from_queue(self):
        # get queue
        queue_name = 'facebook_result'
        channel = self._connection.channel()
        queue_state = channel.queue_declare(queue_name, durable=True)
        queue_length = queue_state.method.message_count

        kol_posts = []
        while (queue_length > 0):
            method, properties, body = channel.basic_get(queue_name, auto_ack=True)
            queue_length -= 1
            if body is not None:
                #print(body)
                kol_posts.append(jsonpickle.decode(str(body, encoding='utf-8')))
        return kol_posts


    def push_baonoi_restart_signal_to_queue(self, queue_name):
        # Input
        # -------
        # trends: an array of dict
        #   ['topic': topic_i, 'posts': [post1, post2, post..n]  (1<=i<=6; 1<=n<=6)

        # prepare data
        connection = self._connection
        body = jsonpickle.dumps({"signal": "restart"})

        # get queues
        channel = connection.channel()
        queue_state = channel.queue_declare(queue_name, durable=True)

        # push trends
        channel.basic_publish(exchange='',
                              routing_key=queue_name,
                              body=body)


    def push_trends_to_queue(self, trends, queue_name='newspaper_trends'):
        # Input
        # -------
        # trends: an array of dict
        #   ['topic': topic_i, 'posts': [post1, post2, post..n]  (1<=i<=6; 1<=n<=6)

        # prepare data
        connection = self._connection
        trends_body = jsonpickle.dumps(trends)
        print("Trends body: ")
        print(trends_body)

        # get queues
        channel = connection.channel()
        queue_state = channel.queue_declare(queue_name, durable=True)

        # push trends
        channel.basic_publish(exchange='',
                              routing_key=queue_name,
                              body=trends_body)

    def disconnect(self):
        # close
        self._connection.close()

