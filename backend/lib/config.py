from lib.utils import *
from lib.category import *

import yaml

# class represents config to crawl a specific website
class WebParsingConfig:
    def __init__(self, web):
        self._web = web # dict of dict {"webname":{"url":...,date_tag:[...], date_class:[...]}
    def get_config(self, key, default):
        if key not in self._web[self.get_webname()]:
            return default
        else:
            return self._web[self.get_webname()][key]

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
    def get_use_browser(self):
        return self._web[self.get_webname()]['use_browser']
    def get_display_browser(self):
        return self.get_config("display_browser", False)

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
    def get_timeout(self, default=1000):
        if "time_out" in self._config:
            return int(self._config['time_out'])
        else:
            return default

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

    def get_waiting_time_between_each_crawl(self):
        return int(self._config['waiting_time_between_each_crawl']) #wait n second before continuing to crawl to avoid blocked

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
    def get_minimum_weight(self):
        return self._config['minimum_weight']
    def get_max_crawler(self):
        return self._config['max_crawler']

