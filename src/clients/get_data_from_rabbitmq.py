##################################################################################################
#Program: Docbao Rabbitmq Client                                                                 #
#Function: Get crawled posts through RabbitMQ                                                    #
##################################################################################################

"""HOW TO USE
This program will check repeatedly if there are new post in RabbitMQ queue. If there are new posts,
it will parse binary message into Post() object, and for each Post instance, call Post.push_to_database()
to save it in database.

Some task must be done to make this works:
1. Provide host, username, password, exchange and queue name for RabbitMQ connection
2. Rewrite Post.push_to_database() function to save post in your favourite database
3. Run this file with Python
"""

from datetime import datetime, timedelta
import jsonpickle
import pika
import jsonpickle
from random import randint
import sys
import time
from time import sleep
import traceback

# RabbitMQ host
HOST = ''
PORT = ''
USERNAME = ''
PASSWORD = ''
EXCHANGE = ''
POST_QUEUE = '' # queue to bind to get posts
MAX_POST = 5 # number of post to push each queue
WAIT_BETWEEN_POST = 0.5

class Post():
    """Represent a crawled article"""
    """
        @Post main function:
            - get_title():
            - get_url():
            - get_author_fullname(): get source of this post
            - get_pushlish_date():
            - get_create_date(): get crawled date
            - get_content(): return a list of image/text paragraphs. First paragraph is post description
                Text paragraph: {'type': 'text', 'content': text}
                Image paragraph: {'type': 'image', 'link': link, 'content': image title}
        """

    def push_to_database(self):
        """Push Post instance to database"""

        # TODO: write code to push Post to your favorite database here
        print(f'Pushing {self.get_title()} to database')

        # print("Post source: %s" % self.get_author_fullname())
        # print("Post url: %s" % self.get_url())
        # print("Post publish_date: %s" % self.get_publish_date())
        # print("Post crawl date: %s" % self.get_create_date())

        # print("Post content")
        # for paragraph in self.get_content():
        #     if paragraph['type'] == 'text':
        #         print(paragraph['content'])
        #     elif paragraph['type'] == 'image':
        #         print(f"[{paragraph['content']}]({paragraph['link']})")
        #     else:
        #         pass

        pass

    has_error = False
    def __init__(self, body):
        """Parsing binary data to make Post instance"""
        try:
            self._body = body # byte data
            unicode_body = str(body, encoding="utf-8")
            self._data = jsonpickle.decode(unicode_body)
            if 'tag' in self._data:
                del self._data['tag']

        except:
            print_exception()
            has_error = True

    def get_post_id(self):
        if 'id' in self._data:
            return self._data['id']
        else:
            return None

    def get_author_id(self):
        if 'authorId' in self._data:
            try:
                # fix bytestring converted to str bug in authorId
                self._data['authorId'] = eval(self._data['authorId']).decode('utf-8')
            except:
                pass
            return self._data['authorId']
        else:
            return None

    def get_author_fullname(self):
        if 'author_fullname' in self._data:
            return self._data['author_fullname']
        else:
            return None

    def get_title(self):
        if 'title' not in self._data:
            return None
        else:
            return self._data['title']

    def get_displayType(self):
        return self._data['displayType']

    def get_tags(self):
        return self._data['tag']

    def set_featureImages(self, featureImages):
        self._data['featureImages'] = featureImages

    def get_featureImages(self):
        if 'featureImages' not in self._data:
            return None
        else:
            return self._data['featureImages']

    def set_dummy_image(self):
        self._data['featureImages'] = [{'small':DUMMY_IMAGE, 'large': DUMMY_IMAGE}]

    def get_publish_date(self):
        return self._data['publish_date']

    def get_create_date(self):
        return self._data['createdAt']

    def set_create_date(self, value):
        self._data['createdAt'] = value


    def get_categories(self):
        return self._data['categories']

    def get_content(self):
        return self._data['content']

    def set_content(self, content):
        self._data['content'] = content

    def get_avatar(self):
        if 'avatar' in self._data:
            return self._data['avatar']
        else:
            return None

    def validate(self):
        if self.has_error: #parse json unsuccesfully
            return False

        # validate id
        if self.get_post_id() is None:
            print("Wrong id")
            return False
        if not isinstance(self.get_post_id(), str):
            print("Wrong id")
            return False
        elif len(self.get_post_id()) > 100:
            print("Wrong id")
            return False

        # validate authorId
        if self.get_author_id() is None:
            print("Wrong authorid")
            return False

        if not isinstance(self.get_author_id(), str):
            print("Wrong authorid")
            return False

        elif len(self.get_author_id()) > 100:
            print("Wrong authorid")
            return False

        # validate title
        if self.get_displayType() not in [0, 1]:
            return False
        elif self.get_displayType() == 0: # newspaper
            if not isinstance(self.get_title(), str):
                print("Wrong title")
                return False

        """
        # validate tag
        for tag in self.get_tags():
            if 'tag' not in tag or 'point' not in tag:
                print("Wrong tag")
                return False
            if len(tag['tag']) > 600:
                print('tag is too long')
                return False

            if int(tag['point']) < 0 or int(tag['point']) > 1000:
                print("Wrong tag point")
                return False
        """

        # validate createdAt
        if not isinstance(self.get_create_date(), str):
            print("Wrong publish date")
            return False

        # validate categories
        if len(self.get_categories()) == 0:
            print("Wrong category")
            return False
        else:
            for category in self.get_categories():
                if category == '':
                    print("Blank category")
                    return False

        # validate content
        content = self.get_content()
        if content is None or len(content) == 0:
            print("Wrong content")
            return False
        else:
            if self.get_displayType() == 0:
                for item in content:
                    if 'type' not in item:
                        print("Wrong content format")
                        return False
                    else:
                        if item['type'] == 'image' and 'link' not in item:
                            print("Lack image in news format. Use dummy image")
                            item['link'] = DUMMY_IMAGE
                        elif item['type'] == 'text' and 'content' not in item:
                            print("Lack content in news format. Use dummy content")
                            item['content'] = "Dummy content"
            else: # content must be a string
                if not isinstance(content, str):
                    print("Wrong social content format")
                    return False

        # this post is ok
        return True

    def get_byte_data(self):
        return jsonpickle.dumps(self._data)

    def get_url(self):
        return self._data['url']

    def push_to_AINEWS(self):
        API_url2 = API_HOST + "/v2/posts"

        data = self.get_byte_data()
        print("Push post_id: %s to AINEWS app" % self.get_post_id())
        headers = {"Content-type": "application/json", "Authorization": "Bearer FSTujwiNAqrkKWDP1fYOmCGpMuO2TnKl"}
        response = requests.post(API_url2, data=data, headers=headers)
        if response.status_code == 200:
            print("OK")
            return True
        else:
            print("Error. Response code: %s" % str(response.status_code))
            print("Error data below")
            print(data)
            return False


def validate_data(ch, method, properties, body):
    post = Post(body)


def get_data_from_rabbitmq():
    """Start a process that get data from RabbitMQ then push to database"""

    # connect to RabbitMQ
    # login
    credentials = pika.PlainCredentials(USERNAME, PASSWORD)
    parameters = pika.ConnectionParameters(HOST, PORT,'/', credentials)
    connection = pika.BlockingConnection(parameters)

    exchange = EXCHANGE
    queue = POST_QUEUE
    number_of_post = MAX_POST

    # Get  posts from queue

    channel = connection.channel()
    queue_state = channel.queue_declare(queue, durable=True, passive=True)
    channel.queue_bind(exchange=exchange, queue=queue)

    queue_length = queue_state.method.message_count
    print("Number of post in queues: %s" % str(queue_state.method.message_count))

    # get message
    count_post = 0
    posts = []
    while (queue_length >= 1 and count_post<MAX_POST):
        method, properties, body = channel.basic_get(queue, auto_ack=True)

        if body is not None:
            posts.append(body)
        queue_length -=1
        count_post +=1

    # parse message into Post and push to database
    count_post = 0
    for body in posts:
        count_post+=1
        print("Processing post %s: " % str(count_post))
        #continue
        post = Post(body)
        if post.validate():         # post is in right format
            post.push_to_database() # push article to database
            print()

    # Close
    connection.close()


def print_exception():
    # Print error message in try..exception
    exec_info = sys.exc_info()
    traceback.print_exception(*exec_info)

# MAIN PROGRAM HERE
if __name__ == '__main__':
    print("GET CRAWLED DATA FROM RABBITMQ")
    while True:
        try:
            # connection might be corrupted for many reasons
            get_data_from_rabbitmq()
        except:
            print_exception()
            print("Some error has happened. Sleep 30 seconds")
            sleep(30)
        sleep(15)

