from src.backend.lib.utils import print_exception, get_independent_os_path
from src.backend.lib.utils import open_binary_file_to_read, open_binary_file_to_write
from src.backend.lib.utils import open_utf8_file_to_read, open_utf8_file_to_write
from src.backend.lib.utils import check_contain_filter, get_utc_now_date, get_fullurl

from src.backend.lib.rabbitmq_client import RabbitMQ_Client
#from .cdn import CDNManager
import yaml                   # text-based object serialization
import re                     # regular expression to extract data from article
import pickle                 # python object serialization to save database
import jsonpickle             # json serialization
import json
import math
import operator
import time
from datetime import datetime
from collections import deque # a queue that keep n-last-added item, use for keyword frequent data
import sys
from lxml import etree
import pytz
import uuid
import epdb
from datetime import timedelta
import textdistance
import requests
import html
import random

DUMMY_AVATAR = "https://cdn.pixabay.com/photo/2015/10/05/22/37/blank-profile-picture-973460_960_720.png"

# GLOBAL VARIABLES


count_duyet = 0
count_bo = 0
count_lay = 0


# class represents a single article
class Article:
    def __init__(self, article_id,href, topic, date, newspaper, language, sapo, content, feature_image, avatar, post_type, author_id=None, author_fullname = '', tags=[]):
        self._id = article_id
        self._href=href
        self._topic=topic.strip()
        self._date=date  # date is stored in UTC timezone
        self._newspaper=newspaper
        self._creation_date = pytz.utc.localize(datetime.utcnow()) # set utc now time
        self._keywords = []
        self._tokenized = False
        self._language = language
        self._sapo = sapo.strip()
        self._content = content # content is a list of dict [{'type':'text', 'content':''}, {'type':'image', 'link':'url'}]
        self._feature_image = feature_image # feature_image is an array  [url]
        self._avatar = avatar
        self._post_type = post_type # 0= newspaper, 1=facebook
        self._tags = tags

        non_unicode_author_id = remove_accents(author_id)
        self._author_id = non_unicode_author_id.strip().replace(' ', '_')
        self._author_fullname = author_fullname

        self._wordpress_id = -1

    def set_wordpress_id(self, post_id):
        self._wordpress_id = post_id

    def get_wordpress_id(self):
        return self._wordpress_id

    def get_id(self):
        return self._id

    def get_tags(self):
        return self._tags

    def get_author_fullname(self):
        return self._author_fullname

    def get_author_id(self):
        return self._author_id

    def get_avatar(self):
        return self._avatar

    def get_post_type(self):
        return self._post_type

    def get_href(self):
        return self._href

    def get_date(self):
        if type(self._date) != bool:
            return self._date
        else:
            return get_utc_now_date()

    def get_topic(self):
        return self._topic

    def get_newspaper(self):
        return self._newspaper

    def get_category(self):
        return self._category

    def get_sapo(self):
        return self._sapo
    def get_content(self):
        return self._content

    def get_full_content(self):
        return self.get_topic() + ' ' + self.get_sapo() + ' ' + self.get_content_as_string()

    def get_semi_full_content(self):
        return self.get_topic() + ' ' + self.get_sapo()

    def get_feature_image(self):
        return self._feature_image

    def get_all_image(self):
        '''
        Get both feature_image and content_image of article
        '''
        feature_image =  self.get_feature_image()
        if feature_image:
            if feature_image[0] != '':
                image_list = feature_image.copy() #if not copy(), edit to image_list means edit to self._feature_image
            else:
                image_list = []
        else:
            image_list = []
        try:
            first_image = True
            for image in self.get_content():
                if image['type'] == 'image':
                    core_url = image['link']
                    # first image in content is feature_image
                    if not first_image:
                        image_list.append(core_url)
                    else:
                        first_image = False
        except:
            print_exception()
            pass
        return image_list


    def get_creation_date(self):
        return self._creation_date

    def get_keywords(self):
        return self._keywords

    def get_language(self):
        return self._language

    def get_date_string(self, timezone, strformat="%d-%m-%y %H:%M"):
        return self.get_date().astimezone(timezone).strftime(strformat)

    def get_creation_date_string(self, timezone, strformat="%d-%m-%y %H:%M"):
        return self._creation_date.astimezone(timezone).strftime(strformat)


    def is_tokenized(self):
        return self._tokenized

    def set_tokenized(self, value):
        self._tokenized = value

    def get_content_as_string(self, delimiter = ' '):
        text_list = [x['content'].strip() for x in self.get_content() if x['type']=='text']
        content = delimiter.join(text_list).strip()
        return content

    def get_content_as_html(self, delimiter = ' '):
        html=[]
        for item in self.get_content():
            if item['type'] == 'text':
                html.append(item['content'].strip())
            elif item['type'] == 'image':
                html.append('<img class="aligncenter" src="%s"> <p style="text-align: center;">%s</p> </img>' % (item['link'], item['content']))
        html = delimiter.join(html).strip()
        return html

    def tokenize(self, keyword_manager):
        '''
        function: tokenize topic or content (if not null)
        '''
        text= self.get_topic()
        self._keywords = keyword_manager.get_topic_keyword_list(text, self.get_language())
        self._tokenized = True


    def is_positive(self, neg_prob=3, neu_prob=7):
        return True
        # """Check if this article is positive or not too negative"""

        # try:
        #     URL = 'http://103.192.236.77:2020/sentiment'
        #     title = self.get_topic()
        #     content = self.get_semi_full_content()
        #     #content = article.get_content_as_string()
        #     response = requests.post(URL, json={'title' : title, 'content':content})
        #     result = response.json()
        #     choice = random.randint(1, 10)
        #     if result == "neg":
        #         if choice <= neg_prob:
        #             print("accept negative post")
        #             return True
        #         else:
        #             print("Do not accept negative post")
        #             return False
        #     elif result == "pos":
        #         print("Positive post")
        #         return True
        #     else:
        #         if choice <= neu_prob:
        #             print("accept neutral post")
        #             return True
        #         else:
        #             print("Do not accept neutral post")
        #             return False
        # except:
        #     return True


    def is_quality_content(self, min_word=50, min_long_image=1, min_image=3):
        '''
        Check if this article is long and have many images
        '''
        content = self.get_content_as_string()
        images = self.get_all_image()

        if (len(content.split()) >= min_word and len(images) >=min_long_image) or len(images) >= min_image:
            return self.is_positive()
        else:
            return False

# class represents article database
class ArticleManager:
    _data = dict()  # a dict of (href: article)
    _blacklist = dict()  # a dict if {href: lifecount}
    _new_blacklist = dict()
    _new_article = dict()
    _sorted_article_list = None

    def __init__(self, config_manager, data_filename, blacklist_filename):
        self._config_manager = config_manager
        self._default_blacklist_count = 50 # will be removed after 10 compression
        self._data_filename = data_filename
        self._blacklist_filename = blacklist_filename
        self._id_iterator = 0

    def update_last_run(self):
        self._last_run = get_utc_now_date()

    def create_article_uuid(self):
        return str(uuid.uuid4())

    def load_data(self):
        stream = open_binary_file_to_read(self._data_filename)
        if stream is not None:
            self._data = pickle.load(stream)
        else:
            print("khong mo duoc file " + self._data_filename)
            self._data = {}

        stream = open_binary_file_to_read(self._blacklist_filename)
        if stream is not None:
            self._blacklist = pickle.load(stream)
        else:
            print("khong mo duoc file " + self._blacklist_filename)
            self._blacklist = {}
        stream = open_binary_file_to_read(self._data_filename + ".log")
        if stream is not None:
            self._id_iterator = pickle.load(stream)
        else:
            print("khong mo duoc file " + self._data_filename + ".log")
            self._id_iterator = 0


    def load_blacklist_data(self):
        stream = open_binary_file_to_read(self._blacklist_filename)
        if stream is not None:
            self._blacklist = pickle.load(stream)
        else:
            print("khong mo duoc file " + self._blacklist_filename)
            self._blacklist = {}
        stream = open_binary_file_to_read(self._data_filename + ".log")
        if stream is not None:
            self._id_iterator = pickle.load(stream)
        else:
            print("khong mo duoc file " + self._data_filename + ".log")
            self._id_iterator = 0


    def save_data(self):

        stream = open_binary_file_to_write(self._data_filename)
        pickle.dump(self._data, stream)
        stream.close()

        stream = open_binary_file_to_write(self._blacklist_filename)
        pickle.dump(self._blacklist, stream)
        stream.close()

        stream = open_binary_file_to_write(self._data_filename+".log")
        pickle.dump(self._id_iterator, stream)
        stream.close()

    def push_data_to_mysql(self):
        print("push data to mysql")
        print(len(self._data))
        for article in self._data:
            print(article.get_topic())

    def get_sorted_article_list(self, only_newspaper=False):
        if only_newspaper:
            article_list = [x for x in list(self._data.values()) if x.get_post_type() == 0]
        else:
            article_list = list(self._data.values())

        article_list.sort(key=lambda x: x.get_date(), reverse=True)

        return article_list

    def get_article(self, article_id):
        if article_id in self._data:
            return self._data[article_id]
        else:
            return None

    def get_article_by_id(self, id):
        for key in self._data:
            if self._data[key]._id == id:
                return self._data[key]
        return None

    def get_latest_article_contain_keyword(self, keyword, only_newspaper=False, number=1):
        '''
        function
        --------
        return article containing a specific keyword

        input
        -----
        number: number of return article

        output
        ------
        a list of article
        '''
        articles = []

        if self._sorted_article_list is None:
            self._sorted_article_list = self.get_sorted_article_list()
        count = 0
        for i in range(0, len(self._sorted_article_list)):
            article = self._sorted_article_list[i]
            # find in topic and in content
            if keyword.strip() in article.get_topic().lower():
                if only_newspaper and (article.get_post_type() != 0):
                    pass
                else:
                    count+=1
                    articles.append(article)
            if count==number:
                break
        if len(articles) == 0:
            return None
        else:
            return articles

    def get_similarity(self, id1, id2, full_content=False, algorithm='cosine'):
        '''
        return similarity between articles has id1 and id2
        :input:
            full_content: compare title or all content
            algorithm: from https://pypi.org/project/textdistance/#description
        :output:
            normalized_similarity(0..1)
            None if error
        '''
        article_1 = self.get_article(id1)
        article_2 = self.get_article(id2)
        if article_1 and article_2:
            if full_content:
                content_1 = article_1.get_full_content()
                content_2 = article_2.get_full_content()
            else:
                content_1 = article_1.get_topic()
                content_2 = article_2.get_topic()
            similarity = eval("textdistance." + algorithm.lower()).normalized_similarity(content_1, content_2)
            return similarity
        else:
            print("Can't find article has id: %s or %s" % (id1, id2))
            return None

    def search_in_database(self, search_string, search_content=True, tag_filter=None, max_number=None):
        """
        Get articles in database that satisfy search_string
        :param:
            search_string: "a,b,c; x,y,z" -> return article that contain (a or b or c) and (x or y or z)
            search_content: search in both content and topic. False mean search in topic only
            tag_filter: "a,b,c;x,y,z" -> article must have tag satisfy (a or b or c) and (x or y or z)
        :return:
            list of articles or None
        """
        result = []
        for id, article in self._data.items(): # search in all database
            if search_content: # create search_string for this article
                text_list = [x['content'] for x in article.get_content() if x['type'] == 'text']
                text_list.append(article.get_topic())
                text_list.append(article.get_sapo())
                content_string = ' '.join(text_list).lower()
            else:
                content_string = article.get_topic().lower()
            search_string = search_string.lower()
            if check_contain_filter(content_string, search_string):
                if tag_filter:
                    if check_contain_filter(article.get_tags(), tag_filter):
                        result.append(article)
                else:
                    result.append(article)
        if result:
            sorted_result = sorted(result, key=lambda x: x.get_date(), reverse=True)
            if max_number:
                return sorted_result[0: max_number]
            else:
                return sorted_result
        else:
            return None

    def get_topic_of_an_url(self, url, webconfig, detail_page_html_tree=None, browser=None, extract_xpath=''):
        '''
        function
        --------
        try to find topic on the page url args point to

        algorithm
        -------
        try to find tag / class that are defined in config.txt

        output
        -------
        topic in string
        '''
        use_browser = webconfig.get_use_browser()
        display_browser = webconfig.get_display_browser()
        topic_type = webconfig.get_topic_type()

        if detail_page_html_tree is None:
            #try:
            html = read_url_source(url, webconfig, browser)
            if html is None:
                return None

            #except:
            #    return None

        if webconfig.get_output_html():
            print(html) #for test

        detail_page_html_tree = etree.HTML(html)

        if "text" in topic_type:
            topic_xpath = webconfig.get_topics_xpath()
            topic = detail_page_html_tree.xpath(topic_xpath)[0].text

            if topic is not None:
                topic = str(topic).strip()
                return (topic, detail_page_html_tree)
            else:
                return (False, detail_page_html_tree)
        else:
            tagstring = get_tagstring_from_etree(detail_page_html_tree)

            #print("html tag that contain date: %s" % tagstring)
            topic = remove_html(tagstring)
            # print(' _ '* 100)
            return (topic, detail_page_html_tree)

    def get_time_of_an_url(self, url, webconfig, detail_page_html_tree, browser=None, index=0, date_xpath=""):
        '''
        function
        --------
        try to find published date on the page url args point to

        algorithm
        -------
        use date_xpath to get html tag and try all date pattern to parse html tag to date

        '''
        display_browser = webconfig.get_display_browser()
        use_index_number = webconfig.get_use_index_number()

        if detail_page_html_tree is None:
            try:
                html = read_url_source(url, webconfig, browser)
                if html is None:
                    return None
                else:
                    detail_page_html_tree= etree.HTML(html)
            except:
                print_exception()
                print("Can't open detail page to get time")
                return None


        if webconfig.get_output_html():
            print(html) #for testing


        a= True
        while a:
        #try:
            result = detail_page_html_tree.xpath(date_xpath)
            #print(result)
            if isinstance(result, list):
                if len(result) > 0:
                    #print("use_index_number %s" % str(use_index_number))
                    #print("index: %s" % str(index))
                    #print(result)
                    if use_index_number == True:
                        result=result[index]
                    else:
                        result=result[0]
                else:
                    print("date_xpath return no result")
                    ignore_topic_not_have_publish_date = webconfig.get_ignore_topic_not_have_publish_date()
                    if ignore_topic_not_have_publish_date:
                        return False
                    else:
                        print("use current time instead")
                        return (pytz.utc.localize(datetime.utcnow()), detail_page_html_tree)
            a=False
        #except:
            #print("Exception in date_xpath")
            #print("use current time instead")
            #return pytz.utc.localize(datetime.utcnow())

        tagstring = get_tagstring_from_etree(result)
        print(tagstring)
        remove_date_tag_html = webconfig.get_remove_date_tag_html()
        if remove_date_tag_html:
            tagstring = remove_html(tagstring)
        print("html tag that contain date: %s" % tagstring)

        result = parse_date_from_string(tagstring, webconfig)
        if result != False:
            return (result, detail_page_html_tree)
        else:
            return False

    def is_repeat_topic_of_same_newspaper(self, topic, webconfig):
        my_newspaper = webconfig.get_webname()
        for key in self._data:
            article = self._data[key]
            first_topic = article.get_topic().strip()
            second_topic = topic.strip()
            if first_topic[-4:] == 'icon':
                first_topic = first_topic[:-4]
            if second_topic[-4:] == 'icon':
                second_topic = second_topic[:-4]
            if first_topic[-2:] == ' .':
                first_topic = first_topic[:-2]
            if second_topic[-2:] == ' .':
                second_topic = second_topic[:-2]

            if (first_topic == second_topic) and (my_newspaper.strip() == article.get_newspaper().strip()):
                return True

        for key in self._new_article:
            article = self._new_article[key]
            first_topic = article.get_topic().strip()
            second_topic = topic.strip()
            if first_topic[-4:] == 'icon':
                first_topic = first_topic[:-4]
            if second_topic[-4:] == 'icon':
                second_topic = second_topic[:-4]
            if first_topic[-2:] == ' .':
                first_topic = first_topic[:-2]
            if second_topic[-2:] == ' .':
                second_topic == second_topic[:-2]
            if (first_topic == second_topic) and (my_newspaper.strip() == article.get_newspaper().strip()):
                return True

        return False


    def investigate_if_link_is_valid_article(self, link, webconfig, home_html_tree, browser, xpath_index, topic_index):
        '''
        function
        --------
        check if atag link point to an article

        algorithm
        --------
        an article will be valid if:
        - href dont' contain any webname in blacklist
        - have published date
        input
        -----
        - link: lxml element
        - home_html_tree: homepage etree
        - xpath_index: index of topic_xpath, date_xpath, content_xpath...to be used
        - topic_index: index of topic to be used (use to extract data  in situation that topic and date lies in them same page like Facebook Page)
        return:
        (topic, publish_date, sapo, content, feature_image_url) or None if link is not an article
        false if browser can't open url
        '''
        #cdn_manager = CDNManager(self._config_manager)
        id_type = webconfig.get_id_type()

        if "href" in id_type:
            detail_page_html_tree = None # to reuse between crawl topic and crawl publish date function
            fullurl = get_fullurl(webconfig.get_weburl(), link.get('href'))
        else: # don't have detail page
            fullurl = ''
            detail_page_html_tree = home_html_tree
            # expect that date_place is not detail_page

        use_browser= webconfig.get_use_browser()
        date_place = webconfig.get_date_place()
        topic_type = webconfig.get_topic_type()
        get_detail_content = webconfig.get_detail_content()
        extract_xpath = webconfig.get_extract_xpath()[xpath_index]
        date_xpath = webconfig.get_date_xpath()[xpath_index]

        contain_filter = webconfig.get_contain_filter()
        topic = ""
        topic_word_list = []
        has_visit = False

        if(webconfig.get_topic_from_link()):
            a=True
            while a:
            #try:

                if "text" in topic_type:
                    result= link.xpath(extract_xpath)

                    if (isinstance(result, list)) and len(result) > 0:
                        #print(result)
                        topic = str(result[0]).strip()
                        max_length = self._config_manager.get_maximum_topic_display_length()
                        print("Topic found: %s" % trim_topic(topic, max_length))
                        topic_word_list = topic.split()
                    else:
                        print("Ignore. Extract result none. This link is not an article")
                        return (None, has_visit)
                else:
                    topic = remove_html(get_tagstring_from_etree(link)).strip()
                    topic = topic.replace('/r', '')
                    print("TOPIC found: %s" % topic)
                    topic_word_list = topic.split()
                a=False
            #except:
                #print("Exception in topic extract xpath. This link is not an article")
                #return (None, has_visit)
        else:
            #try to crawl topic
            (result, detail_page_html_tree) = self.get_topic_of_an_url(fullurl, webconfig, detail_page_html_tree=detail_page_html_tree, browser=browser, extract_xpath=extract_xpath )
            has_visit=True
            if result is not None:
                if result != False:
                    (topic, detail_page_html_tree) = result
                    print("Topic found: %s" % trim_string(topic))
                    topic_word_list = topic.split()
                else:
                    print("Ignore. Can't find topic. This link is not an article")
                    return (False, has_visit)
            else:
                print("Can't open %s" % fullurl)
                return (None, has_visit)

        # check minimun topic length
        minimum_topic_length = webconfig.get_minimum_topic_length()
        if len(topic.strip().split()) < minimum_topic_length:
            print("Ignore. Topic don't satisfy minimum length")
            return (False, has_visit)

        # check contain filter
        if not check_contain_filter(topic, contain_filter):
            print("Ignore. Topic don't satisfy contain filter")
            return (False, has_visit)

        # check repeat topic
        repeat_topic = webconfig.get_limit_repeat_topic()
        if repeat_topic:
            if self.is_repeat_topic_of_same_newspaper(topic, webconfig):
                print("Ignore. This is repeated topic")
                return (False, has_visit)


        if(webconfig.get_skip_crawl_publish_date()):
            newsdate = pytz.utc.localize(datetime.utcnow())
            print("Published at: " + newsdate.strftime("%d-%m-%y %H:%M") + " UTC")
        else:
            # try to find published date
            if "detail_page" in date_place:
                result = self.get_time_of_an_url(fullurl, webconfig, detail_page_html_tree=detail_page_html_tree,browser=browser, index=topic_index, date_xpath=date_xpath)

                has_visit=True
            else:
                result = self.get_time_of_an_url(fullurl, webconfig, detail_page_html_tree=home_html_tree,browser=browser, index=topic_index, date_xpath=date_xpath)
        if (result is not None): # found an article
            if result != False:
                newsdate, detail_page_html_tree = result #extract result
                if self.is_not_outdated(newsdate) or webconfig.get_skip_crawl_publish_date():
                    print("Topic publish date (in newspaper timezone): %s" % get_date_string(newsdate, "%d/%m/%Y %H:%M", webconfig.get_timezone()))
                    # get detail content
                    sapo = ''
                    content = []
                    feature_image_url = ''
                    avatar_url = ''
                    feature_image_fullurl = ''

                    try:
                        if get_detail_content:
                            content_xpath = webconfig.get_content_xpath()[xpath_index]

                            feature_image_xpath = webconfig.get_feature_image_xpath()[xpath_index]
                            avatar_xpath = webconfig.get_avatar_xpath()

                            # get sapo

                            try:
                                sapo_xpath = webconfig.get_sapo_xpath()[xpath_index]
                                sapo = detail_page_html_tree.xpath(sapo_xpath)[0]
                                if not isinstance(sapo, str): # sapo_xpath return an element
                                    sapo = remove_html(get_tagstring_from_etree(sapo)).strip() # clean html
                                else: # sapo_xpath return text
                                    sapo = str(sapo).strip()
                            except:
                                print_exception()
                            print("sapo: " + sapo)


                            # get detail contents: text, image, video, audio...

                            content_etree = ''

                            try:
                                content_etree = detail_page_html_tree.xpath(content_xpath)[0]
                            except:
                                print_exception()

                            # remove unneeded from content etree
                            ignore_xpaths = webconfig.get_remove_content_html_xpaths()
                            try:
                                for xpath in ignore_xpaths:
                                    ignore_elements = content_etree.xpath(xpath)
                                    ignore_elements.reverse() # reverse to remove bottom element to top
                                    for element in ignore_elements:
                                        parent = element.getparent()
                                        if parent is not None:
                                            parent.remove(element)
                            except:
                                print_exception()

                            # clean all span tag
                            for element in content_etree.iter():
                                if element.tag == 'span':
                                    element_text = remove_html(str(get_tagstring_from_etree(element)), ' ')
                                    parent = element.getparent()

                                    if element_text is not None:
                                        if parent is not None:
                                            if parent.text is None:
                                                parent.text = element_text
                                            else:
                                                parent.text = parent.text + element_text
                                    if parent is not None:
                                        parent.remove(element)


                            image_box_xpaths = webconfig.get_image_box_xpath()  # xpath to extract all imagebox element
                            image_title_xpaths = webconfig.get_image_title_xpath()  # xpath to extract title element

                            video_box_xpaths = webconfig.get_video_box_xpath()  # xpath to extract all videobox element
                            video_title_xpaths = webconfig.get_video_title_xpath()  # xpath to extract title element

                            audio_box_xpaths = webconfig.get_audio_box_xpath()  # xpath to extract all audiobox element
                            audio_title_xpaths = webconfig.get_audio_title_xpath()  # xpath to extract title element

                            content = []

                            text_xpaths =  webconfig.get_text_xpath()
                            if text_xpaths == '':
                                text_xpaths = []
                            elif isinstance(text_xpaths, str):
                                text_xpaths = [text_xpaths]

                            text_elements = []
                            try:
                                for text_xpath in text_xpaths:
                                    elements = content_etree.xpath(text_xpath)
                                    text_elements.extend(elements)
                            except:
                                print_exception()

                            # extract all content elements

                            # image
                            image_boxes = [] # elements
                            image_titles = [] # elements

                            if image_box_xpaths == '':
                                image_box_xpaths = []

                            for image_index in range(0, len(image_box_xpaths)):
                                image_box_xpath = image_box_xpaths[image_index]
                                try:
                                    if image_box_xpath != '':
                                        boxes = content_etree.xpath(image_box_xpath)
                                    for box in boxes:
                                        if box not in image_boxes:
                                            image_boxes.append(box)

                                    for box in boxes:
                                        # get image_title from image box
                                        image_title_xpath = image_title_xpaths[image_index]
                                        image_title = box.xpath(image_title_xpath)[0]
                                        image_titles.append(image_title)

                                except:
                                    print_exception()

                            # video
                            video_boxes = []
                            video_titles = []
                            if video_box_xpaths == '':
                                video_box_xpaths = []

                            for video_index in range(0, len(video_box_xpaths)):
                                video_box_xpath = video_box_xpaths[video_index]
                                try:
                                    if video_box_xpath != '':
                                        boxes = content_etree.xpath(video_box_xpath)
                                    for box in boxes:
                                        if box not in video_boxes:
                                            video_boxes.append(box)

                                    for box in boxes:
                                        # get video_title from video box
                                        video_title_xpath = video_title_xpaths[video_index]
                                        video_title = box.xpath(video_title_xpath)[0]
                                        video_titles.append(video_title)

                                except:
                                    print_exception()


                            # audio
                            audio_boxes = []
                            audio_titles = []

                            if audio_box_xpaths == '':
                                audio_box_xpaths = []

                            for audio_index in range(0, len(audio_box_xpaths)):
                                audio_box_xpath = audio_box_xpaths[audio_index]
                                try:
                                    if audio_box_xpath != '':
                                        boxes = content_etree.xpath(audio_box_xpath)
                                    for box in boxes:
                                        if box not in audio_boxes:
                                            audio_boxes.append(box)

                                    for box in boxes:
                                        # get audio_title from audio box
                                        audio_title_xpath = audio_title_xpaths[audio_index]
                                        audio_title = box.xpath(audio_title_xpath)[0]
                                        audio_titles.append(audio_title)

                                except:
                                    print_exception()


                            # remove DOM
                            for element in content_etree.iter():
                                if element in text_elements:
                                    if element not in image_titles and element not in video_titles and element not in audio_titles:
                                        # TODO: remove_html don't remove b, i, em, u
                                        text_content = remove_html(str(get_tagstring_from_etree(element)), ' ').strip()
                                        content.append({'type':'text', 'content':text_content})

                                elif element in image_boxes: # catch image box
                                    # get image_url
                                    image_url = element.xpath('.//img')[0].xpath('./@src')[0]
                                    image_url = get_fullurl(webconfig.get_weburl(), str(image_url))


                                    image_title = ''

                                    # try to get image_title from image box because can't specify image_index
                                    for image_title_xpath in image_title_xpaths:
                                        try:
                                            # TODO: remove_html don't remove b, i, em, u
                                            image_title = remove_html(str(get_tagstring_from_etree(element.xpath(image_title_xpath)[0])))
                                            break
                                        except:
                                            print("Can't extract image title using %s" % image_title_xpath)

                                    content.append({'type':'image', 'link':image_url, 'content':image_title})

                                elif element in video_boxes: # catch video box
                                    # get video_url
                                    video_url = element.xpath('.//video')[0].xpath('./@src')[0]
                                    video_url = get_fullurl(webconfig.get_weburl(), str(video_url))

                                    video_title = ''

                                    # try to get video_title from video box because can't specify video_index
                                    for video_title_xpath in video_title_xpaths:
                                        try:
                                            video_title = str(element.xpath(video_title_xpath)[0].xpath('./text()'))
                                            break
                                        except:
                                            print("Can't extract video title using %s" % video_title_xpath)

                                    content.append({'type':'video', 'link':video_url, 'content':video_title})

                                elif element in audio_boxes: # catch audio box
                                    # get audio_url
                                    audio_url = element.xpath('.//audio')[0].xpath('./@src')[0]
                                    audio_url = get_fullurl(webconfig.get_weburl(), str(audio_url))

                                    audio_title = ''

                                    # try to get audio_title from audio box because can't specify audio_index
                                    for audio_title_xpath in audio_title_xpaths:
                                        try:
                                            audio_title = str(element.xpath(audio_title_xpath)[0].xpath('./text()'))
                                            break
                                        except:
                                            print("Can't extract audio title using %s" % audio_title_xpath)

                                    content.append({'type':'audio', 'link':audio_url, 'content':audio_title})

                            # print content
                            print("content: " )
                            for item in content:
                                if item['type'] == 'text':
                                    print(item['content'])
                                elif item['type'] == 'video' or item['type'] == 'audio' or item['type']=='image':
                                    item['link'] = item['link'].replace(' ', '')
                                    print((item['link'], item['content']))

                            # feature image can be none, because some post don't have any image
                            image_url = content_etree.xpath(feature_image_xpath)
                            if len(image_url) > 0:
                                image_url = str(image_url[0])
                                feature_image_fullurl = get_fullurl(webconfig.get_weburl(), str(image_url))
                                feature_image_fullurl = feature_image_fullurl.replace(' ', '')
                                feature_image = [feature_image_fullurl]
                            else:
                                image_url = ''
                                feature_image = []


                            print("feature image: " + feature_image_fullurl)

                            # get avatar/logo
                            avatar_type = webconfig.get_avatar_type()
                            avatar_xpath = webconfig.get_avatar_xpath()
                            avatar_url = webconfig.get_avatar_url()

                            if avatar_type == 'xpath':
                                try:
                                    avatar_url = str(detail_page_html_tree.xpath(avatar_xpath)[0])
                                except:
                                    print_exception()

                            print("avatar url: %s" % avatar_url)

                    except:
                        print_exception()
                        print("Ignore. Can't extract detail content. This might not be an article")

                        return (False, has_visit)

                    return ((topic, newsdate, sapo, content, feature_image, avatar_url), has_visit)
                else:
                    print("Ignore. This article is outdated")
                    return (False, has_visit)
            else:
                print("Ignore. This href don't have published date. It is not an article.")
                return (False, has_visit)
        else:
            return (None, has_visit)

    def is_in_database(self, href):
        return href in self._data

    def is_blacklisted(self, href):
        return (href in self._blacklist) or (href in self._new_blacklist)

    def add_url_to_blacklist(self, href):
        self._blacklist[href] = self._default_blacklist_count
        self._new_blacklist[href] = self._default_blacklist_count # note: new_blacklist is used for multiprocessing

    def remove_url_from_blacklist(self, href):
        self._blacklist.pop(href)

    def compress_blacklist(self):
        remove =[]
        for href in self._blacklist:
            self._blacklist[href]-=1
            if self._blacklist[href] == 0:
                remove.append(href)
        for href in remove:
            self.remove_url_from_blacklist(href)

    def refresh_url_in_blacklist(self, href): #reward to href when it proves value
        self._blacklist[href] = self._default_blacklist_count
        self._new_blacklist[href]= self._blacklist[href] # note: new_blacklist is used for multiprocessing and will be saved, blacklist is readonly in multiprocessing. Without this line will cause program to crawl one item multiple times

    def add_article(self, new_article):
        self._new_article[new_article.get_id()] = new_article

    def add_articles_from_facebook_by_smcc(self, my_pid, webconfig):
        '''
        function: get kols post from facebook by using smcc service that are ordered from last run (in ConfigManager.load_data())
        '''
        #cdn_manager = CDNManager(self._config_manager)
        MIN_COMMENTS_TO_BE_POPULAR = 20
        try:
            rb = RabbitMQ_Client()
            rb.connect()
            kol_posts = rb.get_kols_post_from_queue() # kol_post is an array of each kols posts
            rb.disconnect()
        except:
            print_exception()
            print("Can't get post from SMCC queue")
            return None
        count = 0
        for posts in kol_posts:
            for post in posts:
                try: # for some reason, smcc crawler return post that is list but not dict
                    if 'id' in post:
                        post_id = post['id']
                    else:
                        post_id = self.create_article_uuid()
                    if 'story' in post:
                        topic = post['story']
                    elif 'message' in post:
                        topic = post['message']
                    else:
                        topic = ''
                    print("Found a new kol post")
                    print("Post content: %s" % topic)
                except:
                    continue
                if not self.is_blacklisted(post_id):
                    if topic!='':
                        publish_date = parse_date_from_string(post['created_time'], webconfig) # check lại timezone
                        if self.is_not_outdated(publish_date):
                            if 'comments' in post:
                                if post['comments']['count'] <= MIN_COMMENTS_TO_BE_POPULAR:
                                    print("This post don't have enought comments to be considered popular")
                                else:
                                    if len(topic.split()) > 100:
                                        if 'shares' in post:
                                            if post['shares']['count'] >= 2:
                                                content = [{'type':'text', 'content':topic}]
                                                avatar_url = DUMMY_AVATAR
                                                author_name = post['from']['name']
                                                newspaper = author_name
                                                author_id = post['from']['id']
                                                if 'link' in post:
                                                    href = post['link']
                                                else:
                                                    href = ''
                                                if 'full_picture' in post:
                                                    #picture = cdn_manager.convert_image(post['full_picture'], type='feature_image')
                                                    feature_image = [post['full_picture']]
                                                else:
                                                    feature_image = []

                                                tags = webconfig.get_tags()

                                                article = Article(article_id=post_id,
                                                                         topic=topic,
                                                                         date=publish_date,
                                                                         newspaper=author_name,
                                                                         href=href,
                                                                         language='vietnamese',
                                                                         sapo='',
                                                                         content=content,
                                                                         feature_image=feature_image,
                                                                         avatar=avatar_url,
                                                                         post_type=1,
                                                                         author_id=author_id,
                                                                         author_fullname=author_name,
                                                                         tags=tags)
                                                #article.set_tokenized(True)
                                                self.add_article(article)
                                                count+=1
                                                print("Crawled articles: %s" % str(count))
                                                self.add_url_to_blacklist(post_id)
                                            else:
                                                print("Ignore. This post don't have enough share")
                                        else:
                                            print("Ignore. This post don't have any share")

                                    else:
                                        print("Ignore. This post is too short")
                            else:
                                print("Ignore. This post don't have any comments")
                        else:
                            print("Ignore. This post is outdated")
                    else:
                        print("Ignore. This post don't have any text")

                else:
                    print("Ignore. This kols post is blacklisted")

    def add_articles_from_facebook(self, my_pid, webconfig, browser):
        '''
        function: crawl post from facebook profile, group or fanpage
        '''
        #cdn_manager = CDNManager(self._config_manager)
        #use_cdn = self._config_manager.get_use_CDN()
        webname = webconfig.get_webname()
        crawl_url = webconfig.get_crawl_url()
        crawl_type = webconfig.get_crawl_type()
        tags = webconfig.get_tags()

        if 'unknown' in webname: # crawl facebook by id
            profile_id = crawl_url
            crawl_url = "https://facebook.com/profile.php?id=" + profile_id
            current_author_id = profile_id


        post_wrapper_xpath = "//div[@class='_5pcr userContentWrapper']"
        post_xpath = ".//div[@data-testid='post_message']"
        date_xpath = "./div/div/div/div/div/div/div/div/div[2]/div/span/span/a/abbr"
        image_ajax_xpath = ".//a[contains(@data-ploi, 'jpg') and not(parent::span)]/@data-ploi"
        #image_url_xpath = "//img[@class='spotlight']/@src"
        avatar_xpath = ".//img/@src"
        post_author_xpath = ".//a[@title and @href and not(descendant::img)]/@href"


        feature_image_url = ''

        count_lay = 0

        print("Crawler pid %s: Crawling %s" % (my_pid, webname))
        html = read_url_source(crawl_url, webconfig, browser)

        if html is not None:
            print("Crawler pid %s: getting data, please wait" % my_pid)
            html_tree = etree.HTML(html)

            if 'unknown' in webname:
                try:
                    webname = html_tree.xpath("//span[@data-testid='profile_name_in_profile_page']/a/text()")[0].strip()
                    crawl_url = html_tree.xpath("//span[@data-testid='profile_name_in_profile_page']/a/@href")[0].strip()
                    current_author_id = get_facebook_id_from_url(crawl_url)
                    print("FB name: %s" % webname)

                except:
                    webname = current_author_id

            current_author_id = get_facebook_id_from_url(crawl_url)
            print("Current Author id: %s" % current_author_id)

            post_wrappers = None
            post = None

            try:
                post_wrappers = html_tree.xpath(post_wrapper_xpath)
            except:
                print_exception()

            if post_wrappers is None:
                print("Can't find any post")
            else: # posts found
                for post_wrapper in post_wrappers: # for each post

                    post_etree = None
                    post_content = ''
                    # get post_content
                    try:
                        post_etree = post_wrapper.xpath(post_xpath)[0]
                        post_content = remove_html(get_tagstring_from_etree(post_etree), '\n')
                    except:
                        print_exception()
                        print("This post wrapper don't have post content?")
                        continue

                    if self.is_blacklisted(post_content): # check if post existed
                        print("Ignore. This post is in blacklist")
                    else:
                        print("New post found: %s" % post_content)

                        if crawl_type == 'facebook user':
                            # check if this post is from current author

                            post_author_id = ''
                            try:
                                post_author_id = get_facebook_id_from_url(str(post_wrapper.xpath(post_author_xpath)[0]))
                                print("Author id of this post: %s" % post_author_id)
                            except:
                                print_exception()
                            if post_author_id != current_author_id:
                                print("Ignore. This post is from another author")
                                continue

                        # Try to get publish date
                        publish_date = None
                        try:
                            publish_date_etree = post_wrapper.xpath(date_xpath)[0]

                            publish_date = parse_date_from_string(get_tagstring_from_etree(publish_date_etree), webconfig)
                            display_timezone = self._config_manager.get_display_timezone()
                            print(publish_date)
                            print(display_timezone)
                            print("Post publish date: %s" % get_date_string(publish_date, "%d/%m/%Y %H:%M", display_timezone))
                        except:
                            print_exception()
                        if publish_date is None:
                            publish_date = get_utc_now_date()

                        # Try to get images
                        images= None
                        post_images = []
                        try:
                            images = post_wrapper.xpath(image_ajax_xpath)
                        except:
                            print_exception()
                            pass

                        if images is not None: # have images
                            print("This post have %s images" % str(len(images)))
                            '''
                            for image_ajax_url in images:
                                # open image page
                                sleep(1) # sleep 1 second
                                image_html = read_url_source(image_ajax_url, webconfig, browser)
                                sleep(1) # sleep 1 second
                                image_html_etree = etree.HTML(image_html)
                                image_html_url = None
                                try:
                                    image_html_url = image_html_etree.xpath(image_url_xpath)
                                    epdb.set_trace()
                                except:
                                    print_exception()
                                if image_html_url is not None:
                                    if len(image_html_url) > 0:
                                        post_images.append({'small': image_html_url[0], 'large': image_html_url[0]})
                            '''
                            post_images = images

                            print("Post images:")
                            print(post_images)
                        else:
                            print("This post don't have any images")

                        # try to get author avatar
                        avatar_url = ''
                        try:
                            avatar_url = str(post_wrapper.xpath(avatar_xpath)[0])
                        except:
                            print_exception()
                        print("Author avatar: %s" % avatar_url)

                        # add new post
                        next_id = self.create_article_uuid()

                        count_lay += 1
                        self.add_article(Article(article_id=next_id,
                                                 topic=post_content,
                                                 date=publish_date,
                                                 newspaper = webname,
                                                 href=crawl_url,
                                                 language=webconfig.get_language(),
                                                 sapo=post_content,
                                                 content=[{'type':'text', 'content':post_content}],
                                                 feature_image=post_images,
                                                 avatar=avatar_url,
                                                 post_type=1,
                                                 author_id=current_author_id,
                                                 author_fullname=webname,
                                                 tags = tags))
                        print("Crawled articles: %s" % str(count_lay))
                        print()
                        self.add_url_to_blacklist(post_content)
        else:
            print("Can't open %s" % crawl_url)



    def add_articles_from_newspaper(self, my_pid, webconfig, browser):
        '''
        function: crawl articles from a specific website
        input:
            - my_pid: pid of process that crawl this newspaper
            - webconfig: config of this newspaper
            - browser: browser that is used to crawl this newspaper
        '''
        #cdn_manager = CDNManager(self._config_manager)
        # get web config properites
        webname = webconfig.get_webname()
        weburl = webconfig.get_weburl()
        crawl_url = webconfig.get_crawl_url()
        web_language = webconfig.get_language()
        get_topic = webconfig.get_topic_from_link()
        topics_xpath = webconfig.get_topics_xpath()
        dates_xpath = webconfig.get_date_xpath()
        extract_xpath = webconfig.get_extract_xpath()
        sapos_xpath = webconfig.get_sapo_xpath()
        contents_xpath = webconfig.get_content_xpath()
        feature_images_xpath = webconfig.get_feature_image_xpath()
        id_type = webconfig.get_id_type()
        use_browser = webconfig.get_use_browser()
        maximum_url_to_visit = webconfig.get_maximum_url()
        get_detail_content = webconfig.get_detail_content()
        only_quality_post = webconfig.get_only_quality_post()
        tags = webconfig.get_tags()

        count_visit = 0 # to limit number of url to visit in each turn
        count_lay = 0
        full_url = ""
        blacklist =  []


        print()
        print("Crawler pid %s: Crawling newspaper: %s" % (my_pid,webname))


        a=True
        while a==True:
        #try:
            count_visit+=1
            html = read_url_source(crawl_url, webconfig, browser)

            if html is not None:
                print("Crawler pid %s: Getting data, please wait..." % my_pid)
                html_tree =  etree.HTML(html)

                for xpath_index in range(0, len(topics_xpath)):
                    print(topics_xpath[xpath_index])
                    topics_list = html_tree.xpath(topics_xpath[xpath_index])

                    for topic_index in range(0, len(topics_list)):
                        link = topics_list[topic_index]
                        # loc ket qua
                        if "href" in id_type:
                            fullurl = get_fullurl(weburl, str(link.get("href")))
                            print()
                            print("Crawler pid %s: Processing page: %s" % (my_pid, fullurl))

                        else:
                            fullurl = remove_html(get_tagstring_from_etree(link))
                            print()
                            print("Crawler pid %s: Processing topic" % my_pid)
                            print("Note: this website don't use href as id_type. Don't set date_place as detail_page")
                        #epdb.set_trace()
                        if not self.is_blacklisted(fullurl):
                            if not self.is_in_database(fullurl):
                                # check if fullurl satisfies url pattern
                                filter = re.compile(webconfig.get_url_pattern_re(), re.IGNORECASE)
                                if ('href' in id_type) and (filter.match(fullurl) is None):
                                    print("Crawler pid %s: Ignore. This url is from another site" % my_pid)
                                else:
                                    (result, has_visit_page) = self.investigate_if_link_is_valid_article(link, webconfig, html_tree, browser, xpath_index, topic_index)
                                    if has_visit_page:
                                        count_visit+=1

                                    print(count_visit)

                                    if result is not None: # no errors happend
                                        if result != False: # valid url
                                            (topic, publish_date, sapo, content, feature_image, avatar_url) = result
                                            if topic[-4:] == 'icon':
                                                topic = topic[:-4]
                                            if topic[-1:] == '.':
                                                topic = topic[:-1]
                                            topic = topic.strip()
                                            tpo_index = topic.find('TPO - ')
                                            if tpo_index != -1:
                                                topic = topic[:tpo_index]
                                            next_id = self.create_article_uuid()

                                            if 'href' not in id_type:
                                                href = webconfig.get_crawl_url()
                                            else:
                                                href = fullurl
                                            
                                            new_article = Article(article_id=next_id,
                                                                     topic=topic,
                                                                     date = publish_date,
                                                                     newspaper = webname,
                                                                     href=href,
                                                                     language=web_language,
                                                                     sapo=sapo,
                                                                     content=content,
                                                                     feature_image=feature_image,
                                                                     avatar = avatar_url,
                                                                     post_type = 0,
                                                                     author_id=webname,
                                                                     author_fullname=webname,
                                                                     tags = tags)
                                            if only_quality_post:
                                                if new_article.is_quality_content():
                                                    self.add_article(new_article)
                                                    self.add_url_to_blacklist(fullurl)
                                                    count_lay +=1
                                                    print("Crawler pid %s: Crawled articles: %s" % (my_pid, str(count_lay)))
                                                else:
                                                    print("Ignore. Not a quality post")
                                            else:
                                                self.add_article(new_article)
                                                self.add_url_to_blacklist(fullurl)
                                                count_lay +=1
                                                print("Crawler pid %s: Crawled articles: %s" % (my_pid, str(count_lay)))

                                            if has_visit_page:
                                                # wait for n second before continue crawl
                                                waiting_time = self._config_manager.get_waiting_time_between_each_crawl()
                                                print("Crawler pid %s: Waiting %s seconds before continue crawling" % (my_pid, str(waiting_time)))
                                                time.sleep(waiting_time + random.random()*3)

                                        else: #not valid link
                                            #self.add_url_to_blacklist(fullurl)
                                            blacklist.append(fullurl) # add invalid link to blacklist later to allow all link refer to the same fullurl will be checked
                                            print("Crawler pid %s: Wait finish crawling to add to blacklist" % my_pid)
                                    else: #timeout or smt else happended
                                        print("Some errors happen. Check this link later")

                                    if count_visit >= maximum_url_to_visit:  # Stop crawling to not get caught by server
                                        print("Crawler pid %s: Stop crawling %s to avoid being caught by server" % (my_pid, webname))
                                        for item in blacklist:
                                           self.add_url_to_blacklist(item)
                                        return None
                            else:
                                print("Crawler pid %s: This article has been in database" % my_pid)
                        else:
                            print("Crawler pid %s: This link is in blacklist database" % my_pid)
                            self.refresh_url_in_blacklist(fullurl)
            else:
                print("Crawler pid %s: Can't open: %s" % (my_pid, webname))
            a=False
            for item in blacklist:
                self.add_url_to_blacklist(item)

        #except:
        #    print("Crawler pid %s: Can't open: %s" % (my_pid, webname))
    def reset_data(self):
        self._data= dict()
        self._blacklist = dict()
        self._new_blacklist= dict()

    def is_not_outdated(self, date):
        diff = (pytz.utc.localize(datetime.utcnow()) - date).days
        return (diff >=0 and diff <= self._config_manager.get_maximum_day_difference())

    def is_article_topic_too_short(self, article):
        return len(article.get_topic().split()) < self._config_manager.get_minimum_word()

    def remove_article(self, article):
        self._data.pop(article.get_id())

    def count_database(self):
        return len(self._data)

    def count_blacklist(self):
        return len(self._blacklist)

    def count_tokenized_articles_contain_keyword(self, keyword):
        count = 0
        for href in self._data:
            article = self._data[href]
            if (article.is_tokenized is True) and (keyword in article.get_topic().lower()):
                count+=1
        return count

    def count_articles_contain_keyword(self, keyword):
        count = 0
        for href in self._data:
            article = self._data[href]
            if keyword in article.get_topic().lower():
                count+=1
        return count

    def compress_database(self, _keyword_manager):
        remove = []
        for url, article in self._data.items():
            if not self.is_not_outdated(article.get_date()):
                remove.append(article)
                self.add_url_to_blacklist(url)
        for article in remove:
            _keyword_manager.build_keyword_list_after_remove_article(article)
            self.remove_article(article)

    def reset_tokenize_status(self):
        for href, article in self._data.items():
            article._tokenized = False

    def get_articles(self, number=None):
        """
        Return latest articles list
        :input:
            number: number of articles to get. None = all
        :output:
            list of articles
            else: None
        """
        article_list = []
        count = 0
        sorted_article_list = self.get_sorted_article_list()

        if not number:
            number = len(sorted_article_list)
        return sorted_article_list[:number]

    def get_articles_as_json(self, number=None):
        """
        Return latest articles list in json format
        :input:
            number: number of articles to get. None = all
        :output:
            json string
            else: None
        """
        json_article_list = []
        count = 0
        sorted_article_list = self.get_sorted_article_list(only_newspaper=True)
        print("Number of articles: %s" % str(len(sorted_article_list)))

        if not number:
            number = len(sorted_article_list)

        for index in range(0, number):
            article = sorted_article_list[index]
            count += 1
            update_time = int((get_utc_now_date() - article.get_date()).total_seconds() / 60)
            update_time_string=""

            if update_time < 0: # publish date on newspaper may be on future (because wrongly typed)
                continue

            if update_time > 1440: # more than 24 hours
                update_time = int(update_time / 1440)
                update_time_string = str(update_time) + " ngày trước"
            else:
                if update_time > 60:
                    update_time = int(update_time / 60)
                    update_time_string = str(update_time) + " giờ trước"
                else:
                    update_time_string = str(update_time) + " phút trước"
            max_length = self._config_manager.get_maximum_topic_display_length()


            json_article_list.append({'stt':str(count),
                                      'topic':trim_topic(article.get_topic(), max_length),
                                      'href':article.get_href(),
                                      'newspaper': article.get_newspaper(),
                                      'update_time': update_time_string,
                                      'publish_time': article.get_date_string(self._config_manager.get_display_timezone()),
                                      'sapo': article.get_sapo(),
                                      'id': article.get_id(),
                                      'feature_image': article.get_all_image()
                                     })
        return json_article_list

    def export_to_json(self, number=None):
        json_article_list = self.get_articles_as_json(number)
        print("Ready to write to file")
        with open_utf8_file_to_write(get_independent_os_path(["export", "article_data.json"])) as stream:
            json.dump({'article_list': json_article_list}, stream)
        print("OK")

    def export_suggestion_list_to_json_file(self):
        pass


