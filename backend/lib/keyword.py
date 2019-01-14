from lib.utils import *
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
    def __init__(self, keyword, topic):
        self._keyword = keyword
        self._freq_timeseries = deque(maxlen=90) 
        self._article_set = set()
        
        # For TF-IDF algorithm
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
                item.set_keyword_freq(item.get_freq_series()-1, self.get_series_iterator())
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
                        new_obj = Keyword(keyword, article.get_topic()) #provide article topic to calculate keyword TF
                        self.add_new_keyword(new_obj)
                        new_keyword.append(new_obj)
            else:
                print("tokenized")
        # update keyword based on new articles
        print("UPDATE OLD KEYWORD FREQ")
        count=0
        total = len(self._keyword_list)
        count_database = self._data_manager.count_database()
        self.increase_series_iterator()
        print("Keyword_Iterator: " + str(self.get_series_iterator()) + " loops")
        for keyword in self._keyword_list:
            count+=1
            print("Updating keyword " + str(count) + "/" + str(total) + ":")
            print("-keyword: " + keyword.get_keyword())
            print("-old_freq: " + str(keyword.get_freq_series()))
            print("-old_covering_article: " + str(keyword.get_covering_article_length()))
            print("-old_weight" + str(keyword.calculate_weight(self._data_manager)))
            for article in new_article:
                if keyword.get_keyword() in article.get_topic().lower():
                    print('found "' + keyword.get_keyword() + '" in article: "' + article.get_topic() + '"')
                    print("article id: " + str(article.get_id()))
                    keyword.set_keyword_freq(keyword.get_freq_series()+1, self._series_iterator)
                    keyword.add_covering_article(article.get_id())
                    keyword.accumulate_tf(article.get_topic())
            print("-new_freq: " + str(keyword.get_freq_series()))
            print("-new_covering_article: " + str(keyword.get_covering_article_length()))
            print("-new_weight: " + str(keyword.calculate_weight(self._data_manager)))

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
                    #if other_keyword.calculate_weight(self._data_manager) > keyword.calculate_weight(self._data_manager): #higher tf-idf will cover common articles
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
            print() 
            print("keyword %s" % keyword.get_keyword())
            print("freq: %s" % str(keyword.get_freq_series()))
            print("weight: %s" % str(weight))
            
            if count <= self._config_manager.get_hot_keyword_number() and weight >= minimum_weight:
                print("add %s to hot keyword dict" % keyword.get_keyword())
                hot_tag[keyword.get_keyword()]= keyword.get_freq_series()
                hot_list.append((keyword.get_keyword(), keyword.get_freq_series()))
                count+=1
            else:
                print("weight of %s is too low to add to hot keyword dict" % keyword.get_keyword())
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
                            print(keyword)
                            print(freq)
                            hot_dict[keyword] = freq
                            #hot_dict[keyword] = tag_dict[keyword]
                            #hot_list[keyword] = self._data_manager.count_articles_contain_keyword(keyword) # count by actual articles contain keywords
            stream.write(jsonpickle.encode(hot_dict))
            stream.close()

    def write_uncategorized_keyword_to_text_file(self):
        tag_dict = self._other_keyword_dict
        with open_utf8_file_to_write(get_independent_os_path(["export","uncategorized_keyword.txt"])) as stream:
            for keyword in sorted(tag_dict, key=tag_dict.get, reverse=True):
                stream.write(keyword + '\r\n')
            stream.close()
            

