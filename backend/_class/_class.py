from _class._utility import * # lib provides general utilities like read/write files...
import underthesea            # NLP package that provide tokenizer, pos_tag functions
import nltk                   # NLP package for English
import yaml                   # text-based object serialization
import re                     # regular expression to extract data from article
import pickle                 # python object serialization to save database
import jsonpickle             # json serialization
from datetime import datetime
from collections import deque # a queue that keep n-last-added item, use for keyword frequent data
import sys

# GLOBAL VARIABLES
count_duyet = 0
count_lay = 0
count_bo = 0

# CLASS DEFINITION
# class represents config to crawl a specific website
class WebParsingConfig:
    def __init__(self, web):
        self._web = web # dict of dict {"webname":{"url":...,date_tag:[...], date_class:[...]}

    def get_webname(self):
        return next(iter(self._web))

    def get_weburl(self):
        return self._web[self.get_webname()]['web_url']

    def get_crawl_url(self):
        return self._web[self.get_webname()]['crawl_url']

    def get_url_pattern_re(self):
        return self._web[self.get_webname()]['url_pattern_re']

    def get_date_tag_list(self):
        return self._web[self.get_webname()]['date_tag']

    def get_date_class_list(self):
        return self._web[self.get_webname()]['date_class']

    def get_date_re(self):
        return self._web[self.get_webname()]['date_re']

    def get_date_pattern(self):
        return self._web[self.get_webname()]['date_pattern']
    
    def get_language(self):
        return self._web[self.get_webname()]['language']

    def get_skip_checking_topic_length(self):
        return self._web[self.get_webname()]['skip_checking_topic_length']

    def get_skip_crawl_publish_date(self):
        return self._web[self.get_webname()]['get_publish_date_as_crawl_date']

    def get_topic_tag_list(self):
        return self._web[self.get_webname()]['topic_tag']

    def get_topic_class_list(self):
        return self._web[self.get_webname()]['topic_class']

    def get_topic_id_list(self):
        return self._web[self.get_webname()]['topic_id']

    def get_topic_from_link(self):
       return self._web[self.get_webname()]['get_topic_from_link']
    def get_topic_re(self):
        return self._web[self.get_webname()]['topic_re']
    def get_output_html(self):
        return self._web[self.get_webname()]['output_html']

# class that manage config defined in /input/config.txt
class ConfigManager:
    _filename = ""
    _config={}

    def __init__(self, filename):
        self._filename = filename

    def load_data(self):
        print(self._config)
        stream = open_utf8_file_to_read(self._filename)
        self._config = yaml.load(stream)
        stream.close()

    def get_minimum_word(self):
        return int(self._config['minimum_topic_length'])

    def get_maximum_day_difference(self):
        return int(self._config['days_to_crawl'])

    def get_newspaper_list(self):
        return [WebParsingConfig(web) for web in self._config['crawling_list']]

    def get_blacklist_web(self): #list of string that a href will be ignored if contain
        return self._config['blacklist']

    def get_newspaper_count(self):
        return len(self._config['crawling_list'])

    def get_hot_keyword_number(self):
        return int(self._config['number_of_hot_keywords']) #this config is too limit number of keywords in database

    def get_categories(self):
        categories = list()
        #for k in self._config['danh_sach_chuyen_muc']:
        #    print(k[next(iter(k))]['vi_tri_xuat_hien'])
        test_list = sorted(self._config['category_list'], key=lambda k: int(k[next(iter(k))]['index']))
        for category in test_list:
            name = next(iter(category))
            categories.append(Category(name=name, filename=category[name]['filename']))
        return categories
    
    def get_minimum_freq_for_two_length_keyword(self):
        return self._config['minimum_freq_for_two_length_keyword_appear_in_hot_keywords'] #this creates a threshold for two-word length keyword to appear in trending list

    def get_minimum_freq_for_more_than_two_length_keyword(self): # this creates a threshold for more than two-word-length keyword to appear in trending list
        return self._config['minimum_freq_for_more_than_two_length_keyword_appear_in_hot_keywords']

    def get_minimum_freq_for_new_keyword(self): #this create a threshold for accepting a keyword a new keyword
        return self._config['mininum_freq_for_new_keyword_accepted']

    def get_minimum_freq_for_fast_growing_keyword(self): #this create a threshold for a new keyword to be checked in fast_growing_keyword_dectector algorithm
        return self._config['minimum_freq_for_fast_growing_keyword_accepted']

    def get_minimum_freq_series_for_fast_growing_keyword(self): #a new keyword must have updated several times to be checked in fast_growing_keyword_dectector algorithm
        return self._config['minimum_freq_series_for_fast_growing_keyword_accepted']

    def get_number_of_trending_keywords(self): #number of keywords to be listed in trending graph
        return self._config['number_of_trending_keywords']

    def get_crawling_interval(self): #inveral in minutes between each crawling loop. This is important for to calculate exact time of each keyword_freq_time_series
        return self._config['crawling_interval']

    def get_loop_interval_for_new_keyword_accepted(self): #new keyword must first appear in loop_interval back from current loop iterator. If crawling_interval = 10, loop_interval = 3, then new keyword appeart in 3*10 = 30 min from current time will be counted
        return self._config['loop_interval_for_new_keyword_accepted']

    def get_minimum_publish_speed(self): # minimum articles published / minute for a keyword to be consider fast growing
        return self._config['minimum_publish_speed']

    def get_running_path(self):
        return self._config['running_path']

    def get_maximum_url_to_visit_each_turn(self):
        return self._config['maximum_url_to_visit_each_turn']


# class represents a single article
class Article:
    def __init__(self,article_id,href, topic, date, newspaper, language, summary = ""):
        self._id = article_id
        self._href=href
        self._topic=topic
        self._date=date # date is string ìn format %d/%m%/%Y
        self._summary=summary
        self._newspaper=newspaper
        self._creation_date = datetime.now()
        self._keywords = []
        self._tokenized = False
        self._language = language

    def get_id(self):
        return self._id

    def get_href(self):
        return self._href

    def get_date(self):
        return self._date

    def get_topic(self):
        return self._topic

    def get_newspaper(self):
        return self._newspaper

    def get_summary(self):
        return self._summary

    def get_creation_date(self):
        return self._creation_date

    def get_keywords(self):
        return self._keywords

    def get_language(self):
        return self._language

    def get_date_string(self):
        return self._date.strftime("%d-%m-%y %H:%M")

    def is_tokenized(self):
        return self._tokenized

    def tokenize(self, keyword_manager):
        self._keywords = keyword_manager.get_topic_keyword_list(self.get_topic(), self.get_language())
        self._tokenized = True

# class represents article database
class ArticleManager:
    _data = dict()  # a dict of (href: article)
    _blacklist = dict()  # a dict if {href: lifecount}
    def __init__(self, config_manager, data_filename, blacklist_filename):
        self._config_manager = config_manager
        self._default_blacklist_count = 10 # will be removed after 10 compression
        self._data_filename = data_filename
        self._blacklist_filename = blacklist_filename
        self._id_iterator = 0
    def get_and_increase_id_iterator(self):
        self._id_iterator+=1
        if self._id_iterator==sys.maxsize:
            self._id_iterator = 1
        return self._id_iterator
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


    def get_sorted_article_list(self):
        article_list = list(self._data.values())
        article_list.sort(key=lambda x: x.get_creation_date(), reverse=True)
        return article_list

    def get_article(self, href):
        return self._data[href]

    def get_topic_of_an_url(self, url, webconfig, soup=None):
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
        if soup is None:
            try:
                soup = read_url_source_as_soup(url)
                if soup is None:
                    return None
            except:
                return None

        if webconfig.get_output_html(): 
            print(soup) #for test

        topic_tag = webconfig.get_topic_tag_list()
        topic_class = webconfig.get_topic_class_list()
        topic_id = webconfig.get_topic_id_list()
       
        topic = None 
        filter = re.compile(webconfig.get_topic_re())
        if topic_tag is not None:
            for tag in topic_tag:
                for foundtag in soup.find_all(tag):
                    tagstring = str(foundtag)
                    searchobj = filter.search(tagstring)  #Search all html tag
                    if searchobj is not None:
                        topic = searchobj.group(1) #Get content of tag

        elif topic_class is not None:
            for _class in topic_class:
                for foundtag in soup.find_all(class_=_class):
                    tagstring = str(foundtag)
                    searchobj = filter.search(tagstring)
                    if searchobj is not None:
                        topic = searchobj.group(1) #Get content of tag


        elif topic_id is not None:
            for topic_id in topic_id:
                for foundtag in soup.find_all(id_=topic_id):
                    tagstring = str(foundtag)
                    searchobj = filter.search(tagstring)
                    if searchobj is not None:
                        topic = searchobj.group(1) #Get content of tag

        if topic is not None:
            return (topic.strip(), soup)
        else:
            return None

    def get_time_of_an_url(self, url, webconfig, soup=None):
        '''
        function
        --------
        try to find published date on the page url args point to

        algorithm
        -------
        try to find tag / class that are defined in config.txt

        '''
        if soup is None:
            try:
                soup = read_url_source_as_soup(url)
                if soup is None:
                    return None
            except:
                return None

        if webconfig.get_output_html():
            print(soup) # for testing
 

        datere = webconfig.get_date_re()
        datetag = webconfig.get_date_tag_list()
        dateclass = webconfig.get_date_class_list()
        date_pattern = webconfig.get_date_pattern()
        filter = re.compile(datere)

        if datetag is not None:
            for tag in datetag:
                for foundtag in soup.find_all(tag):
                    tagstring = str(foundtag) # Get all html of tag
                    # for tagstring in foundtag.contents:
                    searchobj = filter.search(str(tagstring))
                    if searchobj:
                        return datetime.strptime(searchobj.group(1), date_pattern)
        else:
            for date in dateclass:
                for foundtag in soup.find_all(class_=date):
                    tagstring = str(foundtag) # Get all html of tag
                    #for tagstring in foundtag.contents:
                    searchobj = filter.search(str(tagstring))
                    if searchobj:
                        return datetime.strptime(searchobj.group(1), date_pattern)
        return None

    def investigate_if_link_is_valid_article(self, atag, webconfig):
        '''
        function
        --------
        check if atag link point to an article

        algorithm
        --------
        an article will be valid if:
        - href dont' contain any webname in blacklist
        - have published date
        
        return:
        (topic, publish_date) or None if link is not an article
        '''
        global count_bo
        soup = None # to reuse soup between crawl topic and crawl publish date function

        fullurl = get_fullurl(webconfig.get_weburl(), atag['href'])
        topic = ""
        topic_word_list = []
        
        if(webconfig.get_topic_from_link()):
            topic = str(atag.string).strip() # str() is very important !. atag.string is not string and can cause error in jsonpickle
            print("Topic found: %s" % topic)
            topic_word_list = topic.split()
        else:
            #try to crawl topic
            result = self.get_topic_of_an_url(fullurl, webconfig)            
            if result is not None:
                (topic, soup) = result
                print("Topic found: %s" % topic)
                topic_word_list = topic.split()
            else:
                print("Ignore. Can't find topic. This link is not an article")
                return None
        skip_checking_length = webconfig.get_skip_checking_topic_length()
        if (skip_checking_length or len(topic_word_list) >= self._config_manager.get_minimum_word()): # if title length is too short, it might not be an article

            if(webconfig.get_skip_crawl_publish_date()):
                newsdate = datetime.now()
                print("Published at: " + newsdate.strftime("%d-%m-%y %H:%M"))
            else:
                # try to find published date
                newsdate = self.get_time_of_an_url(fullurl, webconfig, soup=soup) 

            if (newsdate is not None): # found an article
                if self.is_not_outdated(newsdate) or webconfig.get_skip_crawl_publish_date():
                    return (topic, newsdate) 
                else:
                    print("Ignore. This article is outdated")
                    count_bo+=1
                    return None
            else:
                print("Ignore. This href don't have published date. It is not an article.")
                count_bo += 1
                return None 
        else:
            print("Ignore. Title is too short. It can't be an article")
            count_bo += 1
            return None 

    def is_in_database(self, href):
        return href in self._data

    def is_blacklisted(self, href):
        return href in self._blacklist

    def add_url_to_blacklist(self, href):
        self._blacklist[href] = self._default_blacklist_count

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
        self._blacklist[href]+=1

    def add_article(self, new_article):
        self._data[new_article.get_href()]= new_article

    def add_articles_from_newspaper(self, webconfig): #Get article list from newspaper with webconfig parsing
        global count_lay, count_duyet
        
        webname = webconfig.get_webname()
        weburl = webconfig.get_weburl()
        crawl_url = webconfig.get_crawl_url()
        web_language = webconfig.get_language()
        get_topic = webconfig.get_topic_from_link()
        count_visit = 0 # to limit number of url to visit in each turn
        maximum_url_to_visit = self._config_manager.get_maximum_url_to_visit_each_turn()
        print()
        print("Crawling newspaper: " + webname)
        #a=True
        #while(a==True):
        try:
            soup = read_url_source_as_soup(crawl_url)
            if get_topic: #from link
                ataglist = soup.find_all("a", text=True, href=True)
            else:
                ataglist = soup.find_all("a", href=True)
               
            print("Getting data, please wait...")
            for atag in ataglist:
                # loc ket qua
                fullurl = get_fullurl(weburl, atag['href'])
                print()
                print("Processing page: " + fullurl)
                count_duyet += 1

                if not self.is_blacklisted(fullurl):
                    if not self.is_in_database(fullurl):
                        # check if fullurl satisfies url pattern
                        filter = re.compile(webconfig.get_url_pattern_re(), re.IGNORECASE)
                        if filter.match(fullurl) is None:
                            print("Ignore. This url is from another site")
                        else:
                            count_visit +=1
                            result = self.investigate_if_link_is_valid_article(atag, webconfig)
                            if result is not None: # is valid article 
                                (topic, publish_date) = result

                                next_id = self.get_and_increase_id_iterator()
                                
                                self.add_article(Article(article_id=next_id,topic=topic, 
                                                 date = publish_date,
                                                 newspaper = webname, href=fullurl, language=web_language))
                                count_lay +=1
                                print("Crawled articles: " + str(count_lay))
                            else:
                                self.add_url_to_blacklist(fullurl)
                                print("Add to blacklist")
                            if count_visit >= maximum_url_to_visit:  # Stop crawling to not get caught by server
                                print("Stop crawling %s to avoid being caught by server" % webname)
                                return None
                    else:
                        print("This article has been in database")
                else:
                    print("This link is in blacklist database")
                    self.refresh_url_in_blacklist(fullurl)
            #a=False
        except:
            print("Can't open: " + webname)

    def is_not_outdated(self, date):
        return (datetime.now() - date).days <= self._config_manager.get_maximum_day_difference()

    def is_article_topic_too_short(self, article):
        return len(article.get_topic().split()) < self._config_manager.get_minimum_word()

    def remove_article(self, article):
        self._data.pop(article.get_href())

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

    def compress_database(self, _keyword_manager):
        remove = []
        for url, article in self._data.items():
            if not self.is_not_outdated(article.get_date()) or self.is_article_topic_too_short(article):
                remove.append(article)
                self.add_url_to_blacklist(url)
        for article in remove:
            _keyword_manager.build_keyword_list_after_remove_article(article)
            self.remove_article(article)

    def reset_tokenize_status(self):
        for href, article in self._data.items():
            article._tokenized = False

# class reprents a single category that keyword belongs to
class Category:
    def __init__(self, name, filename):
        self._name = name
        self._filename = filename
        self._category_set = None
    def get_name(self):
        return self._name

    def get_filename(self):
        return self._filename

    def get_category_set(self):
        if self._category_set is None:
            with open_utf8_file_to_read(self._filename) as stream:
                self._category_set = set([keyword.strip().lower() for keyword in stream.readlines()])        
                stream.close()
        return self._category_set
 
# class represent single keyword that is extracted form article topic
class Keyword:
    def __init__(self, keyword):
        self._keyword = keyword
        self._freq_timeseries = deque(maxlen=90) 
        self._article_set = set()
    def add_covering_article(self, article_id):
        self._article_set.add(article_id)
    def is_covering_nothing(self):
        return len(self._article_set) == 0
    def get_covering_article(self):
        return self._article_set
    def get_covering_article_length(self):
        return len(self._article_set)
    def remove_covering_article(self, article_id):
        self._article_set.discard(article_id)
    def reduce_covering_article(self, reduce_set):
        self._article_set= self._article_set - reduce_set
    def set_keyword_freq(self, freq, series): #set new freq at series time
        has_set = False
        for i in range(0, len(self._freq_timeseries)):
            if self._freq_timeseries[i][0] == series:
                self._freq_timeseries[i][1] = freq
                has_set = True
                break
        if not has_set:
            self._freq_timeseries.append([series, freq])
            
    def get_keyword(self):
        return self._keyword
    def get_keyword_length(self):
        return len(self._keyword.split())
    def get_freq_series(self):
        if len(self._freq_timeseries) == 0:
            return 0
        else:
            return self._freq_timeseries[len(self._freq_timeseries)-1][1]
    def get_length(self):
        return len(self._keyword)
    def get_len_of_freq_series(self):
        return len(self._freq_timeseries)
    def get_last_iterator(self):
        return self._freq_timeseries[len(self._freq_timeseries)-1][0]
    def get_first_iterator(self):
        return self._freq_timeseries[0][0]

#class represents keyword database and provides functions to extract keywords from article database
class KeywordManager:
    _other_keyword_dict = None
    _hot_keyword_dict = None
    _keyword_list = None
    _optimized_keyword_list = None
    def __init__(self, data_manager, config_manager, filename, collocation_filename, remove_keywords_filename):
        self._data_manager = data_manager
        self._config_manager = config_manager
        self._data_filename = filename
        self._collocation_filename = collocation_filename
        self._remove_keywords_filename = remove_keywords_filename
        self._set_stopwords()
        self.get_collocation()
        self._series_iterator = 1
        self._category_set = set()
    def increase_series_iterator(self):
        self._series_iterator+=1
    def get_series_iterator(self):
        return self._series_iterator
    def add_new_keyword(self,keyword):
        self._keyword_list.append(keyword)
    def load_data(self):
        try:
           with open_binary_file_to_read(self._data_filename) as stream:
               self._keyword_list = pickle.load(stream)
               stream.close()
           with open_binary_file_to_read(self._data_filename + ".optimized") as stream:
               self._optimized_keyword_list = pickle.load(stream)
               stream.close()
 
           with open_binary_file_to_read(self._data_filename+ ".log") as stream:
               self._series_iterator = pickle.load(stream)
               print("ITERATOR: " + str(self._series_iterator))
               stream.close()
 
           for category in self._config_manager.get_categories():
               self._category_set= self._category_set | category.get_category_set()
        except:
            self._keyword_list = list()
            self._data_manager.reset_tokenize_status() #reset tokenized status of all article to recount keywords
   

    def save_data(self):
        with open_binary_file_to_write(self._data_filename) as stream:
            print(self._data_filename)
            pickle.dump(self._keyword_list, stream)
            stream.close()
        with open_binary_file_to_write(self._data_filename + ".optimized") as stream:

            pickle.dump(self._optimized_keyword_list, stream)
            stream.close()

        with open_binary_file_to_write(self._data_filename + ".log") as stream:
            pickle.dump(self._series_iterator, stream)
            stream.close()


    def _set_stopwords(self):
        with open_utf8_file_to_read(self._remove_keywords_filename) as f:
            stopwords = set([w.strip() for w in f.readlines()])
        self.stopwords = stopwords

    def get_collocation(self):
        with open_utf8_file_to_read(self._collocation_filename) as f:
            self._collocation =  set([w.strip() for w in f.readlines()])
    
    
    def smart_tokenize(self, sentence, language): # use under_the_sea/nltk tokenizer and pos_tag to keep noun phrase only
        print(sentence)
        if language == "vietnamese":
            tags = underthesea.pos_tag(sentence)
        else:
            sentence = nltk.word_tokenize(sentence)
            tags = nltk.pos_tag(sentence)
        tokens = []
        noun_phrase = ""
        for i in range(0,len(tags)):
            if tags[i][1] in ["N", "Np", "Nu", "Nc", "M", "NN", "NNP", "NNPS", "NNS"] and tags[i][0].strip() not in ["", " "]:
                if noun_phrase != "" :
                    noun_phrase += " " + tags[i][0].strip()
                else:
                    noun_phrase = tags[i][0].strip()
            else:
                if noun_phrase not in ["", " "] and len(noun_phrase.strip().split()) >=2:
                    tokens.append(noun_phrase.strip())
                noun_phrase = ""
        if noun_phrase.strip() not in ["", " "] and len(noun_phrase.strip().split()) >=2:
            tokens.append(noun_phrase.strip())
            
        print(tokens)
        return tokens


    def segmentation(self, topic, language):
        # use collocation first
        temp1 = topic.lower()
        for collo in self._collocation:
            if collo in temp1:
                temp1 = temp1.replace(collo, collo.replace(' ','_'))
        return self.smart_tokenize(temp1, language)


    def split_words(self, topic, language):
        SPECIAL_CHARACTER = '@$.,=+-!;/()*"&^:#><[]|\n\t\'`'
        for ch in SPECIAL_CHARACTER:
            topic.replace(ch, " ")
        tokens = self.segmentation(topic.strip().lower(), language)
        return tokens

    def build_keyword_list_after_remove_article(self, article):
        #assume that article has been tokenized
        remove_list = list()
        topic = article.get_topic()
        print("Removing article: " + article.get_topic())
        for pos in range(len(self._keyword_list)):
            item = self._keyword_list[pos]
            if item.get_keyword() in topic:
                item.set_keyword_freq(item.get_freq_series()-1, self.get_series_iterator())
                item.remove_covering_article(article.get_id)
                if item.get_freq_series() <=0: 
                    remove_list.append(pos)
                    print("Removing keyword: " + item.get_keyword())
        #remove keywords
        while(len(remove_list)>0):
            pos = remove_list.pop()
            if pos < len(self._keyword_list):
                del self._keyword_list[pos]

    def get_topic_keyword_list(self, topic, language):
        split_words = self.split_words(topic, language)
        return [word.replace('_', ' ').strip() for word in split_words] #cau pop de loai bo keyword ''

    def get_series_iterator(self):
        return self._series_iterator
    def is_in_keyword_list(self, keyword):
        for i in range(0, len(self._keyword_list)):
            if self._keyword_list[i].get_keyword() == keyword:
                return True
        return False

    # Rebuild keyword dict
    def build_keyword_list(self):
        print("ANALYZE NEW ARTICLES")
        count = 0
        total = len(self._data_manager._data)
        new_article = []
        new_keyword = []
        # tokenize all new article and collect them into a list
        for article in self._data_manager.get_sorted_article_list():
            count+=1
            print("Analyzing article " + str(count) + "/" + str(total) + ":")
            if article.is_tokenized() is False: #Found new article in database
                article.tokenize(self)
                new_article.append(article)
                for keyword in article.get_keywords():
                    if not self.is_in_keyword_list(keyword):
                        new_obj = Keyword(keyword)
                        self.add_new_keyword(new_obj)
                        new_keyword.append(new_obj)
            else:
                print("tokenized")
        # update keyword based on new articles
        print("UPDATE OLD KEYWORD FREQ")
        count=0
        total = len(self._keyword_list)
        self.increase_series_iterator()
        print("Keyword_Iterator: " + str(self.get_series_iterator()) + " loops")
        for keyword in self._keyword_list:
            count+=1
            print("Updating keyword " + str(count) + "/" + str(total) + ":")
            print("-keyword: " + keyword.get_keyword())
            print("-old_freq: " + str(keyword.get_freq_series()))
            print("-old_covering_article: " + str(keyword.get_covering_article_length()))
            for article in new_article:
                if keyword.get_keyword() in article.get_topic().lower():
                    print('found "' + keyword.get_keyword() + '" in article: "' + article.get_topic() + '"')
                    print("article id: " + str(article.get_id()))
                    keyword.set_keyword_freq(keyword.get_freq_series()+1, self._series_iterator)
                    keyword.add_covering_article(article.get_id())
            print("-new_freq: " + str(keyword.get_freq_series()))
            print("-new_covering_article: " + str(keyword.get_covering_article_length()))

        # auto reduce keyword base on covering article
        print("OPTIMIZE KEYWORD LIST")
        count = 0
        total = len(new_keyword)
        for keyword in new_keyword:
            count+=1
            print("Optimizing with " + str(count) + "/" + str(total) + " keyword: " + keyword.get_keyword())
            self.optimize_keyword_list_with_new_keyword(keyword)
        count=0
        for keyword in self._keyword_list:
            if keyword.is_covering_nothing():
                count+=1
                print("remove " + str(count) + " keyword: " + keyword.get_keyword())
        self._optimized_keyword_list = [x for x in self._keyword_list if not x.is_covering_nothing()]
    def is_contain_category_keyword(self, tag):
        for keyword in self._category_set:
            if keyword.strip() not in ["", " "] and keyword.strip() in tag:
                return True
        return False
    # reduce common covering article then reduce covering nothing keyword
    def optimize_keyword_list_with_new_keyword(self,keyword):
        for other_keyword in self._keyword_list:
            if other_keyword is not keyword:
                common = other_keyword.get_covering_article() & keyword.get_covering_article()
                if len(common) > 0:
                    if other_keyword.get_keyword_length() > keyword.get_keyword_length():
                        #longer keyword will cover common articles
                        print('favor "' + other_keyword.get_keyword() + '" over "' + keyword.get_keyword() + '"')
                        print(common)
                        keyword.reduce_covering_article(common)
                    else:
                        print('favor "' + keyword.get_keyword() + '" over "' + other_keyword.get_keyword() + '"')
                        print(common)
                        other_keyword.reduce_covering_article(common)

    def get_hot_keyword_dict(self):
        tag_list = self._optimized_keyword_list
        hot_tag = dict()
        print("CHOOSE HOT KEYWORD DICTS")
        count = 0
        for keyword in sorted(tag_list, key=lambda x:x.get_length(), reverse=True):
            if count <= self._config_manager.get_hot_keyword_number():
                hot_tag[keyword.get_keyword()]= keyword.get_freq_series()
                count+=1
        self._hot_keyword_dict = hot_tag
        self._other_keyword_dict = dict(hot_tag)
        return hot_tag

    def get_hot_keyword_dict_by_category(self, category):
        if(category.get_name() == "Khác"): return self._other_keyword_dict
        else:
            try:
                with open_utf8_file_to_read(category._filename) as stream:
                    keyword_list = set([k.strip().lower() for k in stream.readlines()])
                    category_keyword = dict()
                    if self._hot_keyword_dict is None:
                        self.get_hot_keyword_dict() # fill self._hot_keyword_dict and self._other_keyword_dict
                    for tag,count in self._hot_keyword_dict.items():
                        for keyword in keyword_list: # keyword must be lowercase
                            if keyword.strip() not in ["", " "] and keyword.strip() in tag and count > 1: # tag contain keyword to diplay in category
                                category_keyword[tag] = count
                                if tag in self._other_keyword_dict:
                                    self._other_keyword_dict.pop(tag)
                                break
                    stream.close()
                    return category_keyword
            except:
                open_utf8_file_to_write(category._filename).close()
                return dict()
    def write_keyword_freq_series_to_json_file(self):
        with open_utf8_file_to_write(get_independent_os_path(["export","keyword_freq_series.json"])) as stream:
            data = dict()
            for item in self._keyword_list:
                keyword = item.get_keyword()
                if keyword not in [""," "]:
                    data[keyword] = []
                    for freq in item._freq_timeseries:
                        data[keyword].append(freq)
            stream.write(jsonpickle.encode({"data": data}))
            stream.close()
        with open_utf8_file_to_write(get_independent_os_path(["export", "keyword_freq_log.json"])) as stream:
            data='{"iterator":' + str(self.get_series_iterator()) + ',"time":"' + datetime.now().strftime("%d-%m-%Y %H:%M:%S") + '"}'
            print(data)
            stream.write(data)
            stream.close()

    def write_keyword_dicts_to_json_files(self):
        category_list = list()
        for category in self._config_manager.get_categories():
            keyword_list = list()
            for keyword, count in self.get_hot_keyword_dict_by_category(category).items():
                keyword_list.append({"keyword": keyword, "count": count})
            category_list.append({"category": category.get_name(), "keywords": keyword_list})
        with open_utf8_file_to_write(get_independent_os_path(["export","keyword_dict.json"])) as stream:
            stream.write(jsonpickle.encode({"data": category_list}))
        stream.close()

    def write_hot_keyword_to_text_file(self):
        tag_dict = self.get_hot_keyword_dict()
        with open_utf8_file_to_write("hot_tag.txt") as stream:
            for keyword in sorted(tag_dict, key=tag_dict.get, reverse=True):
                stream.write(keyword + '\r\n')
            stream.close()

    def write_trending_keyword_to_json_file(self):
        max_trending_keyword = self._config_manager.get_number_of_trending_keywords()
        min_two_keywords = self._config_manager.get_minimum_freq_for_two_length_keyword()
        min_three_keywords = self._config_manager.get_minimum_freq_for_more_than_two_length_keyword()

        if self._hot_keyword_dict is None:
            self.get_hot_keyword_dict()
        tag_dict = self._hot_keyword_dict
        count = 0
        hot_dict = dict()
        with open_utf8_file_to_write(get_independent_os_path(["export","trending_keyword.json"])) as stream:
            for keyword in sorted(tag_dict, key=tag_dict.get, reverse=True):
                if keyword.strip() not in self.stopwords:
                    if (len(keyword.split()) >=2 and tag_dict[keyword] >= min_two_keywords) or (len(keyword.split()) >=3 and tag_dict[keyword] >=min_three_keywords): #hot keywords is long enough and have at leats 4 sources mention
                        count+=1
                        if count <= max_trending_keyword:
                            hot_dict[keyword] = tag_dict[keyword]
                            #hot_list[keyword] = self._data_manager.count_articles_contain_keyword(keyword) # count by actual articles contain keywords
            stream.write(jsonpickle.encode(hot_dict))
            stream.close()

    def write_uncategoried_keyword_to_text_file(self):
        tag_dict = self._other_keyword_dict
        with open_utf8_file_to_write(get_independent_os_path(["export","uncategorized_keyword.txt"])) as stream:
            for keyword in sorted(tag_dict, key=tag_dict.get, reverse=True):
                stream.write(keyword + '\r\n')
            stream.close()
