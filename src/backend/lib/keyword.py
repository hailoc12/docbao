from src.backend.lib.utils import *
import underthesea
import nltk
import yaml                   # text-based object serialization
import re                     # regular expression to extract data from article
import pickle                 # python object serialization to save database
import jsonpickle             # json serialization
import math
import operator
import time
from datetime import datetime
from collections import deque # a queue that keep n-last-added item, use for keyword frequent data
import sys

# class represent single keyword that is extracted form article topic
class Keyword:
    def __init__(self, keyword, article):
        self._keyword = keyword
        self._freq_timeseries = deque(maxlen=90)
        self._freq_timeseries_maxlen = 90
        self._article_set = set()

        # For TF-IDF algorithm
        topic = article.get_topic()
        self._accumulated_tf = len(keyword) / len(topic)

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

    def get_keyword_freq(self, series):
        has_found = False
        freq = 0
        for i in range(0, len(self._freq_timeseries)):
            if self._freq_timeseries[i][0] == series:
                freq = self._freq_timeseries[i][1]
                has_found = True
                break
        if not has_found:
            return None
        else:
            return freq

    def remove_keyword_freq_with_article(self, article, current_iterator, crawl_duration):
        article_iterator = int(current_iterator - ((get_utc_now_date() - article.get_date()).total_seconds()/60/ crawl_duration))
        for series in self._freq_timeseries:
            if series[0] >= article_iterator:
                series[1] = series[1]-1

    def update_keyword_freq_with_new_article(self, article, current_iterator, crawl_duration):
        #print("update keyword freq: %s" % self._keyword)

        article_iterator = int(current_iterator - ((get_utc_now_date() - article.get_date()).total_seconds()/60/ crawl_duration))

        #print("article_iterator: %s" % str(article_iterator))

        has_freq = False
        set_new_freq_pos = False
        new_freq_pos = 0
        new_freq = 0

        for i in range(0, len(self._freq_timeseries)):
            series = self._freq_timeseries[i]
            if series[0] == article_iterator:
                has_freq = True
                self._freq_timeseries[i][1] += 1

            if series[0] > article_iterator:
                if set_new_freq_pos == False:
                    # remember to create new freq series here
                    new_freq_pos = i
                    set_new_freq_pos = True
                self._freq_timeseries[i][1] += 1

        if has_freq == False:
            if set_new_freq_pos == False: # there is no freq greater than article_iterator
                if len(self._freq_timeseries) == 0: # there is no freq_series yet
                    new_freq = 1
                else:
                    new_freq = self._freq_timeseries[len(self._freq_timeseries)-1][1] + 1 #get freq of last iterator plus 1
                self._freq_timeseries.append([article_iterator, new_freq]) #note: article_iterator may be negative
            else: # there is series hat have greater iterator than article_iterator
                if new_freq_pos == 0:
                    new_freq = 1
                else:
                    new_freq = self._freq_timeseries[new_freq_pos-1][1]+1
                #print("new freq: %s" % str(new_freq))
                #print("new_freq_post: %s" % str(new_freq_pos))

                if len(self._freq_timeseries) == self._freq_timeseries_maxlen: # deque is full
                    self._freq_timeseries.popleft()
                    new_freq_pos -= 1

                if new_freq_pos >= 0:
                    self._freq_timeseries.insert(new_freq_pos, [article_iterator, new_freq]) #note: article_iterator may be negative

        #print("has_freq: %s" % str(has_freq))
        #print("freq_timeseries")
        #print(self._freq_timeseries)
        #print()

    def get_keyword(self):
        return self._keyword
    def get_keyword_length(self):
        return len(self._keyword.split())

    def get_freq_series(self, iterator=None):
        # Return freq at specific iterator or last iterator if iterator = None
        # Output:
        #   0: if there are no series
        #   number: if there are exact iterator
        #   None: if can't find exact iterator
        if len(self._freq_timeseries) == 0:
            return 0
        else:
            if iterator is not None:
                for series in self._freq_timeseries:
                    if series[0] == iterator:
                        return series[1]
            else:
                return self._freq_timeseries[-1][1]
        return None
    def get_length(self):
        return len(self._keyword)
    def get_len_of_freq_series(self):
        return len(self._freq_timeseries)
    def get_last_iterator(self):
        return self._freq_timeseries[len(self._freq_timeseries)-1][0]

    def get_first_iterator(self, current_iterator, crawl_duration, trending_duration):
        #function: return first iterator that happended after (now - trending_duration)
        found = False
        # while haven't reach the first ite and duration still smaller than trending_duration
        for i in range(0, len(self._freq_timeseries)):
            iterator = self._freq_timeseries[i][0]
            gap = (current_iterator - iterator) * crawl_duration
            if gap < trending_duration:
                found = True
                return iterator
        if not found:
            return None

    def accumulate_tf(self, topic): # accumulate tf when found new article contain keyword
        self._accumulated_tf += len(self._keyword.split())/len(topic.split())

    def dissipate_tf(self, topic):
        self._accumulated_tf -= len(self._keyword.split())/len(topic.split())

    def get_accumulated_tf(self):
        '''
        function: return sum of every tf = sum(len(keyword)/len(article))
        '''
        return self._accumulated_tf


    def calculate_weight(self, data_manager):
        freq = self.get_freq_series()
        accumulated_freq = 0
        max_freq = data_manager.count_database()
        if freq!=0:
            average_tf = self.get_accumulated_tf() / freq
            return freq
            #return freq * average_tf
            #print("average_tf of %s is %s" % (self.get_keyword(), str(average_tf)))
            #calculate freq with considering to article publish date. Older articles will devote less to freq (<=1)

            #for article_id in self._article_set:
            #  article = data_manager.get_article_by_id(article_id)
            #  day_difference = abs((datetime.now() - article.get_date()).days) #get_date may return wrong value, because real article may provide wrong published date
            #  freq_fading_ratio = day_difference #older article will fade more quickly
            #  accumulated_freq += max(0, 1 - 0.1 * math.pow(1.5, freq_fading_ratio))
            #if accumulated_freq == 0:
            #    return 0
            #else:
            #    return (accumulated_freq)
                #return (average_tf  + math.log(accumulated_freq)) #calculate tf-idf
        else:
           return 0

#class represents keyword database and provides functions to extract keywords from article database
class KeywordManager:
    _other_keyword_dict = None
    _hot_keyword_dict = None
    _hot_keyword_list = None
    _keyword_list = None
    _optimized_keyword_list = None
    _fast_growing_list = dict()
    _new_keyword = None
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

    def get_keyword(self, keyword):
        """return Keyword object with keyword string"""
        for keyword_obj in self._keyword_list:
            if keyword_obj.get_keyword() == keyword:
                return keyword_obj
        return None

    def load_data(self):

        stream = open_binary_file_to_read(self._data_filename)
        if stream is not None:
           self._keyword_list = pickle.load(stream)
           stream.close()
        else:
           self._keyword_list = list()
           self._data_manager.reset_tokenize_status() #reset tokenized status of all article to recount keywords

        stream = open_binary_file_to_read(self._data_filename + ".optimized")
        if stream is not None:
           self._optimized_keyword_list = pickle.load(stream)
           stream.close()

        stream = open_binary_file_to_read(self._data_filename + ".trend")
        if stream is not None:
           self._fast_growing_list = pickle.load(stream)
           stream.close()

        stream = open_binary_file_to_read(self._data_filename+ ".log")
        if stream is not None:
           self._series_iterator = pickle.load(stream)
           print("ITERATOR: " + str(self._series_iterator))
           stream.close()

        for category in self._config_manager.get_categories():
           self._category_set= self._category_set | category.get_category_set()

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

        with open_binary_file_to_write(self._data_filename + ".trend") as stream:
            pickle.dump(self._fast_growing_list, stream)
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
            if item.get_keyword() in topic.lower(): #Note: topic is in original format, so it's important to add .lower() here
                # update keyword after removing article
                item.remove_keyword_freq_with_article(article, self.get_series_iterator(), self._config_manager.get_crawling_interval())
                item.remove_covering_article(article.get_id)

                if item.get_freq_series() <=0:
                    remove_list.append(pos)
                    print("Removing keyword: " + item.get_keyword())
                else:
                    #update tf
                    item.dissipate_tf(topic)

        #remove keywords
        while(len(remove_list)>0):
            pos = remove_list.pop()
            if pos < len(self._keyword_list):
                del self._keyword_list[pos]

    def get_topic_keyword_list(self, topic, language):
        split_words = self.split_words(topic, language)
        keyword_list = [word.replace('_', ' ').strip() for word in split_words]
        return list(set(keyword_list)) # remove duplicate keywords

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
            #print("Analyzing article " + str(count) + "/" + str(total) + ":")
            if article.is_tokenized() is False: #Found new article in database
                article.tokenize(self)
                new_article.append(article)
                for keyword in article.get_keywords():
                    if not self.is_in_keyword_list(keyword):
                        new_obj = Keyword(keyword, article) #provide article topic to calculate keyword TF
                        self.add_new_keyword(new_obj)
                        new_keyword.append(new_obj)
            else:
                #print("tokenized")
                pass
        # update keyword based on new articles
        print("UPDATE OLD KEYWORD FREQ")
        count=0
        total = len(self._keyword_list)
        count_database = self._data_manager.count_database()
        self.increase_series_iterator()
        #print("Keyword_Iterator: " + str(self.get_series_iterator()) + " loops")
        for keyword in self._keyword_list:
            count+=1
            #print("Updating keyword " + str(count) + "/" + str(total) + ":")
            #print("-keyword: " + keyword.get_keyword())
            #print("-old_freq: " + str(keyword.get_freq_series()))
            #print("-old_covering_article: " + str(keyword.get_covering_article_length()))
            #print("-old_weight" + str(keyword.calculate_weight(self._data_manager)))
            for article in new_article:
                if keyword.get_keyword() in article.get_topic().lower():
                    #print('found "' + keyword.get_keyword() + '" in article: "' + article.get_topic() + '"')
                    #print("article id: " + str(article.get_id()))
                    keyword.update_keyword_freq_with_new_article(article, self._series_iterator, self._config_manager.get_crawling_interval())
                    keyword.add_covering_article(article.get_id())
                    keyword.accumulate_tf(article.get_topic())
            #print("-new_freq: " + str(keyword.get_freq_series()))
            #print("-new_covering_article: " + str(keyword.get_covering_article_length()))
            #print("-new_weight: " + str(keyword.calculate_weight(self._data_manager)))

        # auto reduce keyword base on covering article
        print("OPTIMIZE KEYWORD LIST")
        count = 0
        total = len(new_keyword)
        for keyword in new_keyword:
            count+=1
            #print("Optimizing with " + str(count) + "/" + str(total) + " keyword: " + keyword.get_keyword())
            self.optimize_with_new_keyword(keyword)
        count=0
        for keyword in self._keyword_list:
            if keyword.is_covering_nothing():
                count+=1
                #print("remove " + str(count) + " keyword: " + keyword.get_keyword())
        self._optimized_keyword_list = [x for x in self._keyword_list if not x.is_covering_nothing()]

        # find fast growing keyword
        self.detect_fast_growing_keyword()
        # detect new keyword
        self.detect_new_keyword()

    def is_contain_category_keyword(self, tag):
        for keyword in self._category_set:
            if keyword.strip() not in ["", " "] and keyword.strip() in tag:
                return True
        return False

    # reduce common covering article then reduce covering nothing keyword
    def optimize_with_new_keyword(self,keyword):
        for other_keyword in self._keyword_list:
            if other_keyword is not keyword:
                common = other_keyword.get_covering_article() & keyword.get_covering_article()
                if len(common) > 0:
                    #if other_keyword.calculate_weight(self._data_manager) > keyword.calculate_weight(self._data_manager): #higher tf-idf will cover common articles
                    if other_keyword.get_keyword_length() > keyword.get_keyword_length():
                        #longer keyword will cover common articles
                        #print('favor "' + other_keyword.get_keyword() + '" over "' + keyword.get_keyword() + '"')
                        #print(common)
                        keyword.reduce_covering_article(common)
                    else:
                        #print('favor "' + keyword.get_keyword() + '" over "' + other_keyword.get_keyword() + '"')
                        #print(common)
                        other_keyword.reduce_covering_article(common)

    def get_hot_keyword_dict(self):
        '''
        function: return a dict of keywords with hightest weight value

        output:
            dict[keyword] = freq
        '''

        tag_list = self._optimized_keyword_list
        hot_tag = dict()
        hot_list = list()
        print("CHOOSE HOT KEYWORD DICTS BASE ON TF-IDF")
        count = 0
        minimum_weight = self._config_manager.get_minimum_weight()

        for keyword in sorted(tag_list, key=lambda x:x.calculate_weight(self._data_manager), reverse=True):
            weight = keyword.calculate_weight(self._data_manager)
            #print()
            #print("keyword %s" % keyword.get_keyword())
            #print("freq: %s" % str(keyword.get_freq_series()))
            #print("weight: %s" % str(weight))

            if count <= self._config_manager.get_hot_keyword_number() and weight >= minimum_weight:
                #print("add %s to hot keyword dict" % keyword.get_keyword())
                hot_tag[keyword.get_keyword()]= keyword.get_freq_series()
                hot_list.append((keyword.get_keyword(), keyword.get_freq_series()))
                count+=1
            else:
                pass
                #print("weight of %s is too low to add to hot keyword dict" % keyword.get_keyword())
        self._hot_keyword_dict = hot_tag
        self._hot_keyword_list = hot_list
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
            data='{"iterator":' + str(self.get_series_iterator()) + ',"time":"' + get_date_string(get_utc_now_date(),"%d-%m-%Y %H:%M:%S", self._config_manager.get_display_timezone()) + '"}'
            #print(data)
            stream.write(data)
            stream.close()

    def write_keyword_dicts_to_json_file(self):
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
        min_weight = self._config_manager.get_minimum_weight()
        if self._hot_keyword_dict is None:
            self.get_hot_keyword_dict()
        tag_list = self._hot_keyword_list
        tag_dict = self._hot_keyword_dict
        count = 0
        hot_dict = dict()
        print("Write Trending keyword to file")
        with open_utf8_file_to_write(get_independent_os_path(["export","trending_keyword.json"])) as stream:
            for keyword, freq in tag_list:
                if keyword.strip() not in self.stopwords:
                    #tf_idf = keyword.calculate_weight(self._article_manager.count_database())
                    #print(tf_idf)
                    #if keyword.calculate_weight() >= min_weight:
                    if (len(keyword.split()) >=2 and tag_dict[keyword] >= min_two_keywords) or (len(keyword.split()) >=3 and tag_dict[keyword] >=min_three_keywords): #hot keywords is long enough and have at leats 4 sources mention
                        count+=1
                        if count <= max_trending_keyword:
                            #print(keyword)
                            #print(freq)
                            hot_dict[keyword] = freq
                            #hot_dict[keyword] = tag_dict[keyword]
                            #hot_list[keyword] = self._data_manager.count_articles_contain_keyword(keyword) # count by actual articles contain keywords
            stream.write(jsonpickle.encode(hot_dict))
            stream.close()

    def write_trending_keyword_by_growing_speed_to_json_file(self):
        max_trending_keyword = self._config_manager.get_number_of_trending_keywords()
        min_two_keywords = self._config_manager.get_minimum_freq_for_two_length_keyword()
        min_three_keywords = self._config_manager.get_minimum_freq_for_more_than_two_length_keyword()
        min_weight = self._config_manager.get_minimum_weight()

        trending_list = list()
        if max_trending_keyword > len(self._fast_growing_list['720']):
            max_trending_keyword = len(self._fast_growing_list['720'])

        count = 0
        i=0
        print("Write Trending keyword to file")
        with open_utf8_file_to_write(get_independent_os_path(["export","trending_keyword.json"])) as stream:
            while count < max_trending_keyword:
                item = self._fast_growing_list['720'][i]
                keyword = item["keyword"]
                increase_freq = item["increase_freq"]
                if keyword.strip() not in self.stopwords:
                        if count <= max_trending_keyword:
                            count+=1
                            #print(keyword)
                            #print(increase_freq)
                            trending_list.append({"keyword": keyword, "increase_freq": increase_freq})
                i+=1
            trending_duration = self._config_manager.get_trending_duration()
            if trending_duration > 1440: # more than 24 hours
                trending_duration = int(trending_duration / 1440)
                trending_duration_string = str(trending_duration) + " ngày qua"
            else:
                if trending_duration > 60:
                    trending_duration = int(trending_duration / 60)
                    trending_duration_string = str(trending_duration) + " giờ qua"
                else:
                    trending_duration_string = str(trending_duration) + " phút qua"

            stream.write(jsonpickle.encode({"trending_keyword_list":trending_list, 'trending_duration':trending_duration_string}))
            stream.close()
        trending_keyword_list = [x['keyword'] for x in trending_list]
        return trending_keyword_list

    def get_trending_keywords(self):
        """
        Get keywords list those freq grow fastest
        """
        return self._fast_growing_list['720']

    def write_trending_article_to_json_file(self, only_newspaper=True):
        number = self._config_manager.get_number_of_trending_keywords()
        if number > len(self._fast_growing_list['720']):
            number = len(self._fast_growing_list['720'])

        # Write trending articles to json file
        article = None
        article_list = list()
        with open_utf8_file_to_write(get_independent_os_path(["export","trending_article.json"])) as stream:
            for i in range(0, number):
                article = None
                item = self._fast_growing_list['720'][i]
                keyword = item["keyword"]
                articles = self._data_manager.get_latest_article_contain_keyword(keyword, only_newspaper)
                if articles is not None:
                    article = articles[0] # get only latest article
                    update_time = int((get_utc_now_date() - article.get_date()).total_seconds() / 60)
                    update_time_string=""
                    if update_time >= 720:
                        update_time = int(update_time / 720)
                        update_time_string = str(update_time) + " ngày trước"
                    else:
                        if update_time >= 60:
                            update_time = int(update_time / 60)
                            update_time_string = str(update_time) + " giờ trước"
                        else:
                            update_time_string = str(update_time) + " phút trước"
                    max_length = self._config_manager.get_maximum_topic_display_length()
                    article_list.append({
                                'keyword': keyword,
                                'topic': trim_topic(article.get_topic(), max_length),
                                'href': article.get_href(),
                                'newspaper': article.get_newspaper(),
                                'update_time': update_time_string
                                })
            stream.write(jsonpickle.encode({'trending_article_list': article_list}))
            stream.close()

    def write_hot_growing_article_to_json_file(self, only_newspaper=True):
        floor = self._config_manager.get_minimum_freq_of_hot_growing_article()
        upper = self._config_manager.get_maximum_freq_of_hot_growing_article()
        article_list = list()
        with open_utf8_file_to_write(get_independent_os_path(["export","hot_growing_article.json"])) as stream:
            for i in range(0, len(self._fast_growing_list['720'])):
                item = self._fast_growing_list['720'][i]
                keyword = item["keyword"]
                freq = item["count"]
                if freq >= floor and freq <= upper:

                    articles = self._data_manager.get_latest_article_contain_keyword(keyword, only_newspaper)
                    if articles:
                        article = articles[0]
                        update_time = int((get_utc_now_date() - article.get_creation_date()).total_seconds() / 60)
                        update_time_string=""
                        if update_time >= 720:
                            update_time = int(update_time / 720)
                            update_time_string = str(update_time) + " ngày trước"
                        else:
                            if update_time >= 60:
                                update_time = int(update_time / 60)
                                update_time_string = str(update_time) + " giờ trước"
                            else:
                                update_time_string = str(update_time) + " phút trước"
                        max_length = self._config_manager.get_maximum_topic_display_length()
                        article_list.append({
                                    'keyword': keyword,
                                    'topic': trim_topic(article.get_topic(), max_length),
                                    'href': article.get_href(),
                                    'newspaper': article.get_newspaper(),
                                    'update_time': update_time_string
                                    })
            stream.write(jsonpickle.encode({'hot_growing_article_list': article_list}))
            stream.close()

    def write_uncategorized_keyword_to_text_file(self):
        if self._hot_keyword_dict is None:
            self.get_hot_keyword_dict()
        tag_dict = self._other_keyword_dict
        with open_utf8_file_to_write(get_independent_os_path(["export","uncategorized_keyword.txt"])) as stream:
            for keyword in sorted(tag_dict, key=tag_dict.get, reverse=True):
                stream.write(keyword + '\r\n')
            stream.close()

    def detect_new_keyword(self):
        print("DETECT NEW KEYWORDS")
        #keyword first appear in three iterator will be considered new keyword
        keyword_list = self._optimized_keyword_list
        new_keyword = []
        current_iterator = self._series_iterator
        trending_duration = self._config_manager.get_trending_duration() # in minutes
        crawl_interval = self._config_manager.get_crawling_interval()
        count = 0
        #print("Current iterator: " + str(current_iterator))
        min_freq = self._config_manager.get_minimum_freq_for_new_keyword()
        loop_interval = self._config_manager.get_loop_interval_for_new_keyword_accepted()
        for item in keyword_list:
            #print("Processing keyword: " + item.get_keyword())
            first_iterator = item.get_first_iterator(current_iterator, crawl_interval, trending_duration)
            if first_iterator:
                if item.get_len_of_freq_series() >= 1 and (current_iterator - first_iterator <= loop_interval) and (item.get_freq_series() >= min_freq) and (item.get_keyword_length() > 2):
                    new_keyword.append({"keyword":item.get_keyword(),"count": item.get_freq_series()})
                    count+=1
                    #print("Found " + str(count) + " new keywords: " + item.get_keyword())
        self._new_keyword = new_keyword

    def write_new_keyword_to_json_file(self):
        with open_utf8_file_to_write(get_independent_os_path(['export', 'new_keyword.json'])) as stream:
            stream.write(jsonpickle.encode(self._new_keyword))
            stream.close()


    def detect_fast_growing_keyword(self):
        """Detect trending keyword for the last 3h, 6h, 12h, 24h, 48h, 1 week"""

        durations = [180, 360, 720, 1440, 2880, 10080]

        # Function: detect fast growing keyword in trending duration time
        print("DETECT FAST GROWING KEYWORDS")
        keyword_list = self._optimized_keyword_list
        self._fast_growing_list = dict()
        for trending_duration in durations:
            fast_growing_list = list()
            result = fast_growing_list
            iterator = self._series_iterator
            count = 0
            #print("Current iterator: " + str(iterator))
            # a fast growing keyword is a keyword being updated frequently and have publish speed greater than minimum
            min_freq_series = self._config_manager.get_minimum_freq_series_for_fast_growing_keyword()
            min_freq = self._config_manager.get_minimum_freq_for_fast_growing_keyword()
            crawl_interval = self._config_manager.get_crawling_interval()
            publish_speed = self._config_manager.get_minimum_publish_speed()
            # trending_duration = self._config_manager.get_trending_duration() # in minutes
            min_fast_growing_keyword_length = self._config_manager.get_minimum_keyword_length_for_fast_growing_keyword()
            #print("trending_duration: %s" % str(trending_duration))
            for item in keyword_list:
                length = item.get_len_of_freq_series()
                last_iterator= item.get_last_iterator()
                #print("Processing keyword: " + item.get_keyword())
                if length >= min_freq_series and item.get_keyword_length() >= min_fast_growing_keyword_length:
                    first_iterator = item.get_first_iterator(iterator, crawl_interval, trending_duration)
                    if (first_iterator is not None) and (first_iterator != last_iterator):
                        duration = (iterator - first_iterator) * crawl_interval
                        increase_freq = item.get_keyword_freq(last_iterator) - item.get_keyword_freq(first_iterator)
                        #print("first_iterator: %s" % str(first_iterator))
                        #print("last_iterator: %s" % str(last_iterator))
                        #print("increase_freq: %s" % str(increase_freq))

                        if increase_freq == 0:
                            speed = 2 * publish_speed
                        else:
                            speed = duration / increase_freq

                        if speed < publish_speed:
                            count+=1
                            #print("Found " + str(count) + " fast growing keywords: " + item.get_keyword())
                            #print("First Iterator: %s" % str(first_iterator))
                            #print("Duration: " + str(duration))
                            #print("Articles: " + str(item.get_freq_series()))
                            #print("Speed: " + str(speed) + " min/article")
                            result.append({"keyword": item.get_keyword(),
                                            "count": item.get_freq_series(),
                                            "increase_freq": increase_freq})

            # sort fast growing keyword by descending increased frequency
            fast_growing_list = sorted(result, key=lambda k:k["increase_freq"], reverse=True)

            # remove keyword that have the same latest article
            compact_list = []
            latest_article_set = set()

            for index in range(0, len(fast_growing_list)):
                keyword = fast_growing_list[index]['keyword']
                articles = self._data_manager.get_latest_article_contain_keyword(keyword)
                if articles:
                    article = articles[0]
                    if article.get_id() not in latest_article_set:
                        latest_article_set.add(article.get_id())
                        compact_list.append(fast_growing_list[index])

            self._fast_growing_list[str(trending_duration)] = compact_list

        #print(self._fast_growing_list)
        #print("Fast Growing List")

    def write_fast_growing_keyword_to_json_file(self):
        with open_utf8_file_to_write(get_independent_os_path(["export","fast_growing_keyword.json"])) as stream:
            stream.write(jsonpickle.encode(self._fast_growing_list['720']))
