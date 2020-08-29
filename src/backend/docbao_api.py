###############################################################################
# Program: Docbao API                                                         #
# Function: Provide API to work with docbao backend from client               #
# Author: hailoc12                                                            #
# Created: 2019-08-15                                                         #
###############################################################################

"""
Important API

/v1/relate: return relate post of a post for a specific user
/v1/recommend: return recommend post for a specific user

Important Function

encode_auth_token(self, user_id): return token for user_id to use in API call
"""

from flask import Flask, request, jsonify, abort
from lib import *
import random
import jwt
import datetime
import uuid
import jsonpickle
from deco import concurrent, synchronized
from pydub import AudioSegment
import os
import io
import random
import base64


SECRET_KEY = "J\x19\xdaS\x88q\xc8\xfe\x97@\xear\xf3]Jn\xa6,\xcc\xba%P\xa5P"
USER_ID = "bangtin_ainews"
API_PORT = 8080
THEODOIBAOCHI_USER_ID = "theodoibaochi"

# Database function
def load_data():
    '''
    load data to use in API
    :output:
        tuple (config_manager, data_manager, keyword_manager)
        else None
    '''
    try:
        config_manager = ConfigManager(get_independent_os_path(['input', 'config.yaml']),
                                       get_independent_os_path(['input', 'kols_list.txt']),
                                       get_independent_os_path(['input', 'fb_list.txt'])) #config object

        data_manager = ArticleManager(config_manager, get_independent_os_path(["data", "article.dat"]),get_independent_os_path(["data","blacklist.dat"]) ) #article database object
        keyword_manager = KeywordManager(data_manager, config_manager, get_independent_os_path(["data", "keyword.dat"]), get_independent_os_path(["input", "collocation.txt"]), get_independent_os_path(["input", "keywords_to_remove.txt"]))    #keyword analyzer object
        config_manager.load_data(crawl_newspaper=False, crawl_kols=False, crawl_kols_by_smcc=False)
        data_manager.load_data()
        keyword_manager.load_data()
        return (config_manager, data_manager, keyword_manager)
    except:
        return None


def get_relate_post(post_id, number_of_post=6, append_trending_post=True):
    """
    return an array of 6 post relating to current post_id
    :input:
        append_trending_post: true/false
            Add trending post to result if relate posts < number_of_post
        
    """
    NUMBER_OF_POST = number_of_post

    result = load_data()
    if result:
        config_manager, data_manager, keyword_manager = result
    else:
        print("Can't load data")
        return None
   
    article = data_manager.get_article(post_id)
    if article:
        relate_posts = []
        for keyword in article.get_keywords():
            keyword_obj = keyword_manager.get_keyword(keyword)
            if keyword_obj:
                relate_posts.extend([relate_id for relate_id in keyword_obj.get_covering_article() if relate_id != post_id])
        count = 0
        random_relates = []
        while count < number_of_post and count < len(relate_posts):
            index = random.randint(0, len(relate_posts) -1)
            random_relates.append(relate_posts.pop(index)) 
            count += 1

        result = random_relates
        print(result)

        if result:
            if append_trending_post:
                if len(result) < NUMBER_OF_POST:
                    latest_posts= [post.get_id() for post in data_manager.get_articles(NUMBER_OF_POST - len(result))]
                    result.extend(latest_posts)
                else:
                    pass
        else:
            if append_trending_post:
                latest_posts= [post.get_id() for post in data_manager.get_articles(NUMBER_OF_POST - len(result))]
                result.extend(latest_posts)
        print(result)

        return result
    else:
        print("Can't find article has id %s" % post_id)
        return None


def get_trend_post(max_post = 100):
    """
    Return latest post relating to trending keywords
    :output:
        list of post_id (n <= max_post)
    """
    result = load_data()
    if result:
        config_manager, data_manager, keyword_manager = result
    else:
        print("Can't load data")
        return None

    result = []

    for count, keyword in enumerate(keyword_manager.get_trending_keywords(), 1):
        if count > max_post:
            break
        else:
            result.extend([post.get_id() for post in data_manager.get_latest_article_contain_keyword(keyword['keyword'], number=max(2, 4//count))])

    if result:
        return result
    else:
        return None


def encode_auth_token(user_id=USER_ID):
    """Generates the Auth Token 
    :return: string 
    """
    try:
        payload = {
                'exp': datetime.datetime.utcnow() + datetime.timedelta(days=1000, seconds=5),
                'iat': datetime.datetime.utcnow(),
                'sub': user_id
                }
        return jwt.encode(
                    payload,
                    SECRET_KEY,
                    algorithm='HS256'
                )
    except Exception as e:
        return e


def decode_auth_token(auth_token):
    """    Decodes the auth token    
    :param auth_token:    
    :return: integer|string    
    """
    try:
        payload = jwt.decode(auth_token, SECRET_KEY)
        return payload['sub']
    except jwt.ExpiredSignatureError:
        return 'Signature expired. Please log in again.'
    except jwt.InvalidTokenError:
        return 'Invalid token. Please log in again.'


# API PART
app = Flask(__name__)


@app.route('/v1/article/similarity')
def get_similarity():
    """
    return similarity between two article
    :input:
        request body: {'article1': id, 'article2': id, full_content:True/False, algorithm: 'cosine'}
    :output:
        normalized_similiarty (0..1)
    """
    #TODO: replace this with query from database
    result = load_data()
    if result:
        config_manager, data_manager, keyword_manager = result
    else:
        print("Can't load data")
        return jsonify("Can't load database")

    body = request.json
    header = request.headers
    auth_token = header['Authorization'].replace('Bearer ', '')

    if decode_auth_token(auth_token) == THEODOIBAOCHI_USER_ID:
        if 'article1' in body and 'article2' in body:
            id1 = body['article1']
            id2 = body['article2']
            full_content = body['full_content']
            algorithm = body['algorithm']
            similarity = data_manager.get_similarity(id1, id2, full_content, algorithm)
            if similarity:
                return jsonify(similarity)
            else:
                return jsonify("Can't find article to compare")
        else:
            return jsonify("Can't find article1 and article2 id in request")
    else:
        print("Can't authorize")
        return jsonify({"error": "Can't authorize"})
 

@app.route('/v1/articles/<number>')
def get_articles(number):
    """
    return list of lastest articles with length=number
    :output:
        - an array of dict with format like in article_data.json
        - else None
    """
    #TODO: replace this with query from database
    result = load_data()
    if result:
        config_manager, data_manager, keyword_manager = result
    else:
        print("Can't load data")
        return None

    body = request.json
    header = request.headers
    auth_token = header['Authorization'].replace('Bearer ', '')

    if decode_auth_token(auth_token) == THEODOIBAOCHI_USER_ID:
        articles = data_manager.get_articles_as_json(int(number))
        if articles:
            return jsonify({'article_list': articles })
        else:
            return jsonify({"error": "Can't get any articles"})
    else:
        print("Can't authorize")
        return jsonify({"error": "Can't authorize"})
 
@app.route('/v1/image/upload', methods=['POST'])
def upload_image():
    """
    upload image and return image url
    :input:
        - {'data': image_byte_stream, 'type': in ['feature_image', 'content_image', 'avatar', 'category']}
    :output:
        - if type in ['feature_image', 'content_image']:
                return {'large': url, 'small': url}
          elif type in ['avatar', 'category']:
              return url
        - else None
    """

    body = request.json
    header = request.headers
    auth_token = header['Authorization'].replace('Bearer ', '')
    print(auth_token)

    if decode_auth_token(auth_token) == THEODOIBAOCHI_USER_ID:
        cdn_manager = CDNManager()
        data = request.files['data']
        image_type = request.form['image_type']
        image_url = cdn_manager.convert_image(data.read(), type=image_type, mode='data')
        if image_url:
            return jsonify(image_url)
        else:
            return jsonify({"error": "Can't convert and uploate image"})
    else:
        print("Can't authorize")
        return jsonify({"error": "Can't authorize"})
 
@app.route('/v1/article/<id>')
def get_article(id):
    """
    return article that have id=id
    :output:
        - body of an article if id exists in database
        - else None
    """
    #TODO: replace this with query from database
    result = load_data()
    if result:
        config_manager, data_manager, keyword_manager = result
    else:
        print("Can't load data")
        return None


    body = request.json
    header = request.headers
    auth_token = header['Authorization'].replace('Bearer ', '')

    if decode_auth_token(auth_token) == THEODOIBAOCHI_USER_ID:
        article = data_manager.get_article(id)
        if article:
            content = [x['content']for x in article.get_content() if x['type']=='text']
            result = {
              'topic':article.get_topic(),
              'href':article.get_href(),
              'newspaper': article.get_newspaper(),
              'publish_time': article.get_date_string(config_manager.get_display_timezone()),
              'sapo': article.get_sapo(),
              'content': content
            }
            return jsonify(result)
        else:
            return jsonify({"error": "Can't get any articles"})
 

@app.route('/v1/search')
def search_articles_API():
    """return articles that satisfy search_string format
    input
        - search: search string
        - full_search: true/false
    output
        - list of dict that contain article information
    """
    #TODO: replace this with query from database
    result = load_data()
    if result:
        config_manager, data_manager, keyword_manager = result
    else:
        print("Can't load data")
        return None


    body = request.json
    header = request.headers
    auth_token = header['Authorization'].replace('Bearer ', '')

    if decode_auth_token(auth_token) == THEODOIBAOCHI_USER_ID:
        search_string = body['search']
        full_search = body['full_search']
        if 'tag_filter' in body:
            tag_filter = body['tag_filter']
        else:
            tag_filter = None

        # TODO: cache request with Redis
        search_result = data_manager.search_in_database(search_string, search_content=full_search, tag_filter=tag_filter)
        max_length = config_manager.get_maximum_topic_display_length()
        article_list = []
        if search_result:
            for article in search_result:
                article_list.append({
                              'id': article.get_id(),
                              'topic':trim_topic(article.get_topic(), max_length),
                              'href':article.get_href(),
                              'newspaper': article.get_newspaper(),
                              'update_time': article.get_creation_date_string(config_manager.get_display_timezone()),
                              'publish_time': article.get_date_string(config_manager.get_display_timezone()),
                              'sapo': article.get_sapo()
                             })

            return jsonify({'posts': article_list})
        else:
            return jsonify({'error': "Can't get any result"})
    else:
        return jsonify({'error': 'Wrong authorization token'})


@app.route('/v1/relate')
def get_relate_post_API():
    """return relate post for a specific user
    input
        - user_id: can be omitted
        - post_id
    output
        - list of post_id that relate to input post_id
    """

    body = request.json
    header = request.headers
    auth_token = header['Authorization'].replace('Bearer ', '')

    if decode_auth_token(auth_token) == USER_ID:
        if 'user_id' in body:
            user_id = body['user_id']
        else:
            user_id = None
        if 'post_id' in body:
            post_id = body['post_id']

            # TODO: cache request with Redis
            result = get_relate_post(post_id)
            if result:
                return jsonify({'posts': result})
            else:
                return jsonify({'error': "Can't find related posts"})
        else:
            return jsonify({'error': "Not post_id in request"})
    else:
        return jsonify({'error': 'Wrong authorization token'})


@app.route('/v1/quality_articles')
def get_quality_articles_API():
    """
    return quality post
    input
        body = ['number_of_articles': number,
                'number_of_relate_articles': number]
    output
        {'posts': [{'post_id': id, 'relate_post':[id1, id2...]}]}
    """
    #TODO: replace this with query from database
    result = load_data()
    if result:
        config_manager, data_manager, keyword_manager = result
    else:
        print("Can't load data")
        return None
 
    body = request.json
    header = request.headers
    auth_token = header['Authorization'].replace('Bearer ', '')
    number_of_articles = int(body['number_of_articles'])
    must_have_images = body['must_have_images']
    number_of_relate_articles = int(body['number_of_relate_articles'])
    min_number_of_images = int(body['min_number_of_images'])
    contain_filter = None if 'contain_filter' not in body else body['contain_filter']

    if decode_auth_token(auth_token) == THEODOIBAOCHI_USER_ID:
        # TODO: cache request with Redis
        result = []
        if contain_filter:
            print(contain_filter)
            trend_posts = data_manager.search_in_database(contain_filter, search_content=False, tag_filter=None, max_number=30)
            trend_posts = [article.get_id() for article in trend_posts]
            print(trend_posts)
        else:
            trend_posts = get_trend_post(max_post=max(50, number_of_articles))
        if trend_posts:
            random.shuffle(trend_posts)
            count = 0
            quality_posts = trend_posts
            for post_id in quality_posts:
                article = data_manager.get_article(post_id)
                if article:
                    # Choose article based on trendy and number of images
                    if len(article.get_all_image()) >= min_number_of_images:
                        relate_posts = []
                        if number_of_relate_articles > 0:
                            relate_posts = get_relate_post(post_id, number_of_relate_articles, False)
                        result.append({'post_id':post_id,
                                        'relate_posts': relate_posts})
                        count += 1
                        if count >= number_of_articles:
                            break

            return jsonify({'posts': result})
        else:
            return jsonify({'error': "Can't find quality posts"})
    else:
        return jsonify({'error': 'Wrong authorization token'})


@app.route('/v1/recommend')
def get_recommended_post_API():
    """return relate post for a specific user
    input
        - user_id: can be omitted
        - type:
            + 0: recommendation
            + 1: top trends
    output
        - list of post_id that relate to input post_id
    """

    body = request.json
    header = request.headers
    auth_token = header['Authorization'].replace('Bearer ', '')

    if decode_auth_token(auth_token) == USER_ID:
        if 'user_id' in body:
            user_id = body['user_id']
        else:
            user_id = None
        type = body['type']

        # TODO: cache request with Redis
        if type == 0:
            result = get_trend_post()

            #for index, post in enumerate(result):
            #    print(post)
            #result = get_recommend_post(user_id)
        else:
            result = get_trend_post()

        if result:
            return jsonify({'posts': result})
        else:
            return jsonify({'error': "Can't find recommended posts"})
    else:
        return jsonify({'error': 'Wrong authorization token'})


@app.route("/v1/baonoi/restart",methods=['POST'])
def send_baonoi_restart_signal():
    '''
    Restart baonoi server to recover from errors
    :input:
        body: {"server": number}
    :output:
        no response
    '''
       
    body = request.json
    header = request.headers
    auth_token = header['Authorization'].replace('Bearer ', '')

    if decode_auth_token(auth_token) == THEODOIBAOCHI_USER_ID:
        server = None if 'server' not in body else body['server']

        if server != None:

            rb = RabbitMQ_Client()
            rb.connect()
            rb.push_baonoi_task_to_queue(body, 'baonoi_restart_' + str(server))
            rb.disconnect()
            
            return jsonify('Success push restart signal to server %s' % str(server))
        else:
            return jsonify({"error": "Bad input"})
            
    else:
        print("Can't authorize")
        return jsonify({"error": "Can't authorize"})


@app.route("/v1/baonoi",methods=['POST'])
def make_baonoi():
    '''
    Create baonoi from article and upload to youtube channel
    :input:
        body: {'id': article_id, 'channel': channel_name_in_config_file, ['voice': url], ['images': [{'large', 'small'}]]}
    :output:
        no response
    '''
    #TODO: replace this with query from database
    result = load_data()
    if result:
        config_manager, data_manager, keyword_manager = result
    else:
        print("Can't load data")
        return None
       
    body = request.json
    header = request.headers
    auth_token = header['Authorization'].replace('Bearer ', '')

    if decode_auth_token(auth_token) == THEODOIBAOCHI_USER_ID:
        text = None if 'text' not in body else body['text']
        article_id = None if 'id' not in body else body['id']

        if text:
            if type(text)==list:
                topic = trim_topic(text[0], 12)
            else:
                topic = trim_topic(text, 12)
        elif article_id:
            article = data_manager.get_article(article_id)
            if not article:
                return jsonify({"errors": "Can't find article %s" % str(article_id)})
            else:
                topic = article.get_topic()
        else:
            return jsonify({"error": "text and id can't be both null"})

        server = body['server']
        rb = RabbitMQ_Client()
        rb.connect()
        rb.push_baonoi_task_to_queue(body, 'baonoi_task_' + str(server))
        rb.disconnect()
        
        return jsonify('Success push "%s" to queue' % topic)
        
    else:
        print("Can't authorize")
        return jsonify({"error": "Can't authorize"})


@app.route("/v1/image",methods=['GET'])
def get_image():
    '''
    Get all image url from an article and relate posts
    :input:
        body: {'id': article_id, 'from_relate_post': boolean, 'relate_post': number, 'precision': 0..1, 'provided_relate_posts': [id]}
        relate_post: number of latest post to check relation with article_id post
        precision: min similarity to be considered related post
    :output:
        {"image": [array of dict {'large': url, 'small': url}]}
    '''
    #TODO: replace this with query from database
    result = load_data()
    if result:
        config_manager, data_manager, keyword_manager = result
    else:
        print("Can't load data")
        return None
       
    body = request.json
    header = request.headers
    auth_token = header['Authorization'].replace('Bearer ', '')

    if decode_auth_token(auth_token) == THEODOIBAOCHI_USER_ID:
        article_id = None if 'id' not in body else body['id']
        from_relate_post = False if 'from_relate_post' not in body else body['from_relate_post']
        relate_post = 100 if 'relate_post' not in body else body['relate_post']
        precision = 0.5 if 'precision' not in body else body['precision']
        full_content = False if 'full_content' not in body else body['full_content']
        provided_relate_posts = None if 'provided_relate_posts' not in body else body['provided_relate_posts']

        article_list = []

        if article_id:
            article = data_manager.get_article(article_id)
            if article:
                article_list.append(article)

        if provided_relate_posts:
            article_list.extend([relate_article for relate_article in map(data_manager.get_article, provided_relate_posts) if relate_article])
        elif from_relate_post:
            relate_post = get_relate_post(article_id, relate_post)
            for post_id in relate_post:
                if data_manager.get_similarity(article_id, post_id, full_content=full_content, algorithm='levenshtein') > precision:
                    print("Found an similar article: %s" % post_id)
                    post = data_manager.get_article(post_id)
                    print("Title: %s" % post.get_topic())
                    print()
                    article_list.append(post)

        images = []
        for article in article_list:
            images.extend(article.get_all_image())
        return jsonify({"images": images})


@app.route("/v1/baonoi/notification",methods=['GET'])
def get_banoi_notification():
    '''
    Get all notification from baonoi server
    
    Input:
    request={
                'server': number // server to get notification
            }
    '''
    body = request.json
    header = request.headers
    auth_token = header['Authorization'].replace('Bearer ', '')

    if decode_auth_token(auth_token) == THEODOIBAOCHI_USER_ID:
        server = body['server']
        rb = RabbitMQ_Client()
        rb.connect()
        messages = rb.get_baonoi_notification_from_queue("baonoi_notification_" + str(server).strip())
        return jsonify(messages)
    else:
        print("Can't authorize")
        return jsonify({"error": "Can't authorize"})


@app.route("/v1/asr",methods=['GET'])
def get_text():
    '''
    Transform speech to text and get text from response
    
    Input:
    request={
            'name'='file', 'filename'=$FILE_PATH
            }
    headers = {
                'token': 'anonymous',
                #'sample_rate': (float) sample rate of file audio if use pcm,
                #'format':(string) format of file audio if use pcm,
                #'num_of_channels':(integer) number channels of file audio if use pcm,
                #'asr_model': 'model code' (default)
                }

    #AUDIO_PATH: PATH TO AUDIO
    files = {'file': open($AUDIO_PATH,'rb')} 

    CERT_PATH: PATH to vtcc.ai certificate

    Output: Text-Subscript of audio
    '''
    body = request.json
    header = request.headers
    auth_token = header['Authorization'].replace('Bearer ', '')

    if decode_auth_token(auth_token) == THEODOIBAOCHI_USER_ID:
        # prepare data to call Viettel STT API
        data = body
        if 'asr_model' not in body:
            data['asr_model'] = 'model code'
        if 'token' not in body:
            data['token']=''
        url = "https://vtcc.ai/voice/api/asr/v1/rest/decode_file"
        headers = {
                    'token': 'kzrnyfWGD9hOUGDOSV164YGqiUmxGY-Ln5q6wpn9Y68hiJ-h3H8cvNABiFdLJGFO',
                    #'sample_rate': 16000,
                    #'format':'S16LE',
                    #'num_of_channels':1,
                    'asr_model': 'model code'
                    }

        s = requests.Session()
        AUDIO_PATH=data['filename']
        files= {'file': open(AUDIO_PATH,'rb')}
        response = requests.post(url,files=files, headers=headers, verify='wwwvtccai.crt')
        result=json.loads(response.text)
        if result[0]['msg']=="STATUS_SUCCESS":
            return result[0]['result']['hypotheses'][0]['transcript']
        else:
            print("Error in calling Viettel ASR API.")
            return jsonify("Can't transform audio to text.")
    else:
        print("Can't authorize")
        return jsonify({"error": "Can't authorize"})


def concanate(arr):
    for i in range(1,len(arr)):
        arr[0]+=arr[i]
    return arr[0]


def divide_paragraph_into_chunks(paragraph, chunk_length=1):
    sentences = [chunk.strip() for chunk in paragraph.strip().split(".") if chunk.strip()!= '']
    count_sentence = len(sentences)
    if count_sentence <= chunk_length:
        return [paragraph]
    else:
        left = divide_paragraph_into_chunks('. '.join(sentences[:count_sentence // 2]))
        right = divide_paragraph_into_chunks('. '.join(sentences[count_sentence // 2:]))
        return left + right


@concurrent
def get_audio_from_Viettel_TTS(data, key, voice_data):
    '''
    Get voice data from text
    :output:
        voice_data[key] = {'voice': audio data, 'text': text}
    '''
    url = "https://vtcc.ai/voice/api/tts/v1/rest/syn"
    headers = {'Content-type': 'application/json', 'token': 'kzrnyfWGD9hOUGDOSV164YGqiUmxGY-Ln5q6wpn9Y68hiJ-h3H8cvNABiFdLJGFO'}
    print(data[key])
    response = requests.get(url, data=json.dumps(data[key]), headers=headers)
    if response.status_code == 200:
        voice_data[key] = {'voice': response.content, 'text': data[key]['text']}
        return True
    else:
        voice_data[key] = None
        return False


@app.route("/v1/voice",methods=['GET'])
def get_audio():
    ''' 
    #Transform text to speech and get back mp3 data and subtitle data
    #:input:
        #body: {'voice': 0..4, 'text': [string], ['id': id], ['without_filter: boolean], [speed: 0.7-1.3]}
    #:output:
        {
                'file': wav byte stream
                'subtitle': ['caption': text, 'duration': voice_duration+silent_duration]
        }
    '''

    lst_voice=['doanngocle','trinhthiviettrinh','phamtienquan','lethiyen','nguyenthithuyduyen']

    #data get from request article_API
    body = request.json
    header = request.headers
    auth_token = header['Authorization'].replace('Bearer ', '')

    if decode_auth_token(auth_token) == THEODOIBAOCHI_USER_ID:
        # prepare data to call Viettel TTS API
        # https://viettelgroup.ai/document/tts
        data = body
        if 'id' not in body:
            data['id'] = str(uuid.uuid4())
        if 'without_filter' not in body:
            data['without_filter'] = False
        if 'speed' not in body:
            data['speed'] = 1.0
        if 'voice' not in body:
            data['voice'] = lst_voice[2]
        else:
            data['voice']=lst_voice[int(body['voice'])]

        data['tts_return_option'] = 2 # wav
        origin_text = body['text'].copy() #body may change after concurrent request in this function

        long_silent_duration = 1 if 'long_silent_duration' not in body else body['long_silent_duration']
        short_silent_duration = 1 if 'short_silent_duration' not in body else body['short_silent_duration']
        break_into_small_chunks = True if 'break_large_paragraph_into_small_chunks' not in body else body['break_large_paragraph_into_small_chunks']
        chunk_length = 1 if 'chunk_length' not in body else body['chunk_length']

        audio_data = dict()
        input_data = dict()
        long_silent = AudioSegment.silent(duration=long_silent_duration)
        short_silent = AudioSegment.silent(duration=short_silent_duration)
        

        # get paragraph and chunks voice
        #print("Before chunking %s" % origin_text)
        for indexp, paragraph in enumerate(origin_text, 1):
            #print(indexp)
            #print(paragraph)
            if paragraph.strip() != '':
                if break_into_small_chunks: # create paragraph audio from joining smaller chunks audio
                    paragraph_audio = long_silent

                    chunks = divide_paragraph_into_chunks(paragraph.strip(), chunk_length)            
                    for indexc, chunk in enumerate(chunks):
                        data['text'] = chunk
                        key = str(indexp) + ',' + str(indexc)
                        input_data[key] = data.copy()
                        get_audio_from_Viettel_TTS(input_data, key, audio_data)
                else: # create paragraph audio from one call to Viettel TTS
                    data['text'] = paragraph.strip()
                    key = str(indexp)
                    input_data[key] = data.copy()
                    get_audio_from_Viettel_TTS(input_data, key, audio_data)
         
        get_audio_from_Viettel_TTS.wait() # wait until all audio are get

        # combine paragraph and chunks into final audio and caculate subtitle data
        subtitle=[]
        combined_audio = AudioSegment.silent(duration=0.5)
        #print("after chunking: %s" % origin_text)
        for indexp, paragraph in enumerate(origin_text, 1):
            if str(indexp) in audio_data: # this paragraph is not chunked
                if audio_data[str(indexp)] == None:
                    abort("500")
                    return jsonify({"error": "Can't get voice from Viettel TTS"})
                paragraph_audio = AudioSegment(io.BytesIO(audio_data[str(indexp)]['voice'])) + long_silent
                combined_audio += paragraph_audio
                subtitle.append({'caption': paragraph, 'duration': paragraph_audio.duration_seconds})
                print(paragraph)
            else:
                indexc = 0
                key = str(indexp) + ',' + str(indexc) 
                subtitle_duration = 0

                while key in audio_data:
                    if audio_data[key] == None:
                        abort("500")
                        return jsonify({"error": "Can't get voice from Viettel TTS"})
                    chunk_audio =  AudioSegment(io.BytesIO(audio_data[key]['voice'])) + short_silent
                    combined_audio += chunk_audio
                    subtitle_duration = chunk_audio.duration_seconds
                    subtitle.append({'caption': audio_data[key]['text'], 'duration': subtitle_duration})
                    indexc+=1
                    key = str(indexp) + ',' + str(indexc) 
                combined_audio += short_silent
                subtitle[-1]['duration'] += short_silent.duration_seconds
                print(paragraph)

        # export and return data
        combined_audio.export("voice.wav", format="wav")

        data = None
        with open_binary_file_to_read("voice.wav") as stream:
            data = stream.read()
        os.remove("voice.wav")
        
        result = {'audio': base64.b64encode(data).decode('utf-8'), 'subtitle': subtitle}
        return jsonify(result)
        #return combined_audio.raw_data
    else:
        print("Can't authorize")
        return jsonify({"error": "Can't authorize"})
 

if __name__ == '__main__':
    # load database
    print("Start Docbao API Server")
    # start API server
    app.run(host='0.0.0.0', port=API_PORT, debug=True)

