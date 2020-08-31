import random
from src.backend.lib.utils import print_exception, get_independent_os_path
from src.backend.lib.utils import get_utc_now_date
from src.backend.lib.utils import open_utf8_file_to_read, open_utf8_file_to_write
from src.backend.lib.utils import open_binary_file_to_read, open_binary_file_to_write
from src.backend.lib.utils import get_date_string

from src.backend.lib.category import Category
import pytz
import yaml
from datetime import datetime
from datetime import timedelta
from src.backend.lib.rabbitmq_client import RabbitMQ_Client

# class represents config to crawl a specific website
class WebConfig:
    def __init__(self, web=None):
        if web is None:
            self._web = {"default":{}}
        else:
            self._web = web # dict of dict {"webname":{"url":...,date_tag:[...], date_class:[...]}

    def get_config(self, key, default):
        if key not in self._web[self.get_webname()]:
            self.set_config(key, default)
            return default
        else:
            value = self._web[self.get_webname()][key]
            try:
                return int(value)
            except:
                return value

    def delete_config(self, key):
        try:
            del self._web[self.get_webname()][key]
            return True
        except:
            return False

    def get_only_quality_post(self):
        return self.get_config('only_quality_post', False)

    def get_text_xpath(self):
        return self.get_config('text_xpath', './/node()[text()]')
    def get_image_box_xpath(self):
        return self.get_config('image_box_xpath', [])
    def get_image_title_xpath(self):
        return self.get_config('image_title_xpath', [])
    def get_video_box_xpath(self):
        return self.get_config('video_box_xpath', [])
    def get_video_title_xpath(self):
        return self.get_config('video_title_xpath', [])
    def get_audio_box_xpath(self):
        return self.get_config('audio_box_xpath', [])
    def get_audio_title_xpath(self):
        return self.get_config('audio_title_xpath', [])

    def get_avatar_type(self):
        return self.get_config('avatar_type', 'url') # or 'xpath'

    def get_avatar_xpath(self):
        return self.get_config('avatar_xpath', '')

    def get_avatar_url(self):
        return self.get_config('avatar_url', '')

    def get_webname(self):
        return next(iter(self._web))

    def get_weburl(self):
        return self._web[self.get_webname()]['web_url']

    def get_crawl_url(self):
        return self._web[self.get_webname()]['crawl_url']

    def get_url_pattern_re(self):
        return self._web[self.get_webname()]['url_pattern_re']
    def get_ignore_topic_not_have_publish_date(self):
        return self.get_config('ignore_topic_not_have_publish_date', False)
    def get_prevent_auto_redirect(self):
        return self.get_config('prevent_auto_redirect', False)

    def get_crawl_type(self):
        return self.get_config('crawl_type', 'newspaper')

    def get_remove_content_html(self):
        return self.get_config('remove_content_html', True)

    def get_topics_xpath(self):
        return self.get_config('topics_xpath', '//a')
    def get_topic_type(self):
        return self.get_config('topic_type', "text")
    def get_remove_date_tag_html(self):
        return self.get_config('remove_date_tag_html', False)
    def get_date_xpath(self):
        return self.get_config('date_xpath', '')
    def get_detail_content(self):
        return self.get_config('get_detail_content', False)
    def get_sapo_xpath(self):
        return self.get_config('sapo_xpath', '')
    def get_content_xpath(self):
        return self.get_config('content_xpath', '')
    def get_remove_content_html_type(self):
        return self.get_config('remove_content_html_type', 'basic')
    def get_remove_content_html_xpaths(self):
        return self.get_config('remove_content_html_xpaths', [])
    def get_feature_image_xpath(self):
        return self.get_config('feature_image_xpath', '')
    def get_date_re(self):
        result = self._web[self.get_webname()]['date_re']
        if(not isinstance(result, list)): #compatible with older config version
            return [result]
        else:
            return result

    def get_date_pattern(self):
        result = self._web[self.get_webname()]['date_pattern']
        if(not isinstance(result, list)):
            return [result]
        else:
            return result

    def get_date_place(self):
        return self.get_config('date_place', 'detail_page')
    def get_limit_repeat_topic(self):
        return self.get_config('skip_repeat_topic', True)

    def get_timezone(self):
        '''
        output: pytz.timezone class
        '''
        try:
            result = pytz.timezone(self.get_config('timezone', 'UTC'))
        except:
            print("Wrong timezone format. Please provide one in tz database (google it)")
            print("Choose UTC by default")
            result = pytz.timezone("UTC")
        return result

    def get_language(self):
        return self._web[self.get_webname()]['language']
    def get_id_type(self):
        return self.get_config('id_type', 'href')

    def get_skip_crawl_publish_date(self):
        return self._web[self.get_webname()]['get_publish_date_as_crawl_date']

    def get_extract_xpath(self):
        return self.get_config('extract_xpath', ["*/text()"])
    def get_use_index_number(self):
        return self.get_config('use_index_number', False)

    def get_topic_from_link(self):
       return self.get_config('get_topic_from_link', True)
    def get_output_html(self):
        return self._web[self.get_webname()]['output_html']
    def get_use_browser(self):
        return self._web[self.get_webname()]['use_browser']
    def get_display_browser(self):
        return self.get_config("display_browser", False)
    def get_browser_timeout(self):
        return self.get_config("browser_timeout", 60)
    def get_browser_fast_load(self):
        return self.get_config('browser_fast_load', True)
    def get_browser_profile(self):
        return self.get_config('browser_profile', None)
    def get_contain_filter(self):
        return self.get_config("contain", "")
    def get_maximum_url(self):
        '''
        function: get max number of link that will be crawl in this website in one call
        '''
        return self.get_config("maximum_url", 10)

    def get_tags(self):
        """get metadata to label post crawled from this webconfig"""
        return self.get_config("tags", [])

    def set_tags(self, tags):
        self.set_config("tags", tags)

    def get_last_run(self):
        last_run_string = self.get_config('last_run', get_utc_now_date() - timedelta(days=7))
        if isinstance(last_run_string, str):
            naive_last_run = datetime.strptime(last_run_string, "%d/%m/%Y %H:%M")
            aware_last_run = self.get_timezone().localize(naive_last_run)
            return aware_last_run
        else:
            last_run = last_run_string
            self.set_last_run(last_run)
            return last_run

    def get_minimum_topic_length(self):
        return self.get_config('minimum_topic_length', 4)

    def set_last_run(self, date=None):
        if date is None:
            date = get_utc_now_date()
        self.set_config('last_run', get_date_string(date, "%d/%m/%Y %H:%M", pytz.timezone("UTC")))

    def get_minimum_duration_between_crawls(self):
        return self.get_config('minimum_duration_between_crawls', 5)

    def set_minimum_duration_between_crawls(self, value):
        self.set_config('minimum_duration_between_crawls', value)
    def set_config(self, key, value):
        self._web[self.get_webname()][key] = value

    def export(self, filepath):
        with open_utf8_file_to_write(filepath) as stream:
            yaml.dump([self._web], stream, default_flow_style=False, allow_unicode=True, sort_keys=False)

    def print_config(self):
        webname = self.get_webname()

        count = 1
        config_list = []
        print(str(count) + ' ' + webname + ':')
        config_list.append(webname)
        count = 2
        for key in self._web[webname]:
            value = self._web[webname][key]
            print(str(count) + '   - ' + key + ': ' + str(value))
            config_list.append((key, value))
            count+=1
        return config_list

    def get_config_by_index(self, index):
        count = 0
        for key in self._web[self.get_webname()]:
            if count == index:
                return (key, self._web[self.get_webname()][key])
            count+=1
        return None


    def load_default_config(self, site_type=None, config_base_path=None):
        if config_base_path is None:
            config_base_path = get_independent_os_path(['resources', 'configs', 'newspaper'])

        if site_type is None:
            filepath = get_independent_os_path([config_base_path,'website_template.md'])
            self.load_config_from_file(filepath)
        elif site_type == 'newspaper':
            filepath = get_independent_os_path([config_base_path,'newspaper_template.md'])
            self.load_config_from_file(filepath)
        elif site_type == 'wordpress':
            filepath = get_independent_os_path([config_base_path,'wordpress_template.md'])
            self.load_config_from_file(filepath)
        elif site_type == 'facebook user':
            filepath = get_independent_os_path([config_base_path,'facebook_template.md'])
            self.load_config_from_file(filepath)
        elif site_type == 'facebook fanpage':
            filepath = get_independent_os_path([config_base_path,'fanpage_template.md'])
            self.load_config_from_file(filepath)

    def load_config_from_file(self, filepath):
        with open_utf8_file_to_read(filepath) as stream:
            self._web = yaml.full_load(stream)[0]

    def set_webname(self, webname):
        old_name = self.get_webname()
        self._web={webname: self._web[old_name]}



# class that manage config defined in /input/config.txt
class ConfigManager:
    _filename = ""
    _config={}

    def __init__(self, config_filename, kol_filename=None, fb_account_filename=None):
        self._filename = config_filename
        self._kol_filename = kol_filename
        self._fb_account_filename = fb_account_filename

    def load_data(self, crawl_newspaper=True, crawl_kols=False, crawl_kols_by_smcc=False, random_kols=True, random_fb_account=True, max_kols=5, base_path='..'):
        '''
        input
        -----
        crawl_newspaper: crawl newspaper configs in /backend/input/config.yaml
        crawl_kols: crawl kols post from kols id list in /backend/input/kols_list.txt by using facebook bot
            random_kols: choose random (max_kols) from kols list to crawl
            random_fb_account: set random fb bot (presetup in /backend/input/fb_list.txt file to crawl kol posts
        crawl_kols_by_smcc: crawl kols posts using smcc service (push some kol id to queue and get back post from queue). Choose random kols id (100 in number) by default and create only one webconfig with crawl_type = "kols smcc"
        base_path: get value '..' or '.' to specify path to resources folder in comparision with running path
        '''
        #print(self._config)
        stream = open_utf8_file_to_read(self._filename)
        self._config = yaml.full_load(stream)
        stream.close()

        newspaper_list = []

        if not crawl_newspaper:
            self.replace_crawl_list([])
        else:
            newspaper_list = self.get_newspaper_list()         # crawl newspaper last to init browser with random profiles first
            self.replace_crawl_list([])

        if crawl_kols:

            # get kols_list
            kols_list = []
            with open_utf8_file_to_read(self._kol_filename) as stream:
                kols_list = [x for x in stream.read().split('\n') if x.strip() != '']

            # get fb account list
            fb_list = []
            if random_fb_account:
                with open_utf8_file_to_read(self._fb_account_filename) as stream:
                    fb_list = [x for x in stream.read().split('\n') if x.strip() != '']

            count = 0
            index = 0
            choosen = set()

            while count < max_kols and count < len(kols_list): # finish when get max_kols
                count+=1
                if random_kols:
                    index = random.randint(0, len(kols_list)-1)
                    while index in choosen: # no repeat value
                        index = random.randint(0, len(kols_list)-1)
                    choosen.add(index)
                    print(f"Choose random kols: {kols_list[index]}") # print choosen kol for debugging
                else:
                    index += 1
                    if index == len(kols_list): # end of kols list
                        break

                if ';' not in kols_list[index]: # this line contain just id, not name;url
                    kol_name = 'unknown_id_' + kols_list[index]
                    crawl_url = kols_list[index].strip() # profile id
                else:
                    kol_name = kols_list[index].split(';')[0]
                    crawl_url = kols_list[index].split(';')[1]

                webconfig = WebConfig()
                webconfig.load_default_config('facebook user', get_independent_os_path([base_path, 'resources', 'configs', 'newspaper']))
                webconfig.set_webname(kol_name)
                webconfig.set_config('crawl_url', crawl_url)
                webconfig.set_config('remove_me', True) # tag for delete when program finish
               # set random fb account to crawl
                if random_fb_account:
                    profile_index = random.randint(0, len(fb_list) -1)
                    profile = fb_list[profile_index]
                    webconfig.set_config('browser_profile', profile)

                self.add_newspaper(webconfig)
        # print(self._config)
        # crawl kols by smcc
        if crawl_kols_by_smcc:
            # create a 'crawl_type: kols smcc' WebConfig
            webconfig = WebConfig()
            webconfig.load_default_config('facebook user', get_independent_os_path([base_path, 'resources', 'configs', 'newspaper']))
            webconfig.set_config('crawl_type', 'kols smcc')
            webconfig.set_config('remove_me', True)
            webconfig.set_config('timezone', 'UTC')
            webconfig.set_webname('kol posts')
            webconfig.set_config('minimum_duration_between_crawls', -5)

            self.add_newspaper(webconfig)

        # append newspaper list
        if crawl_newspaper:
            for newspaper in newspaper_list:
                    self.add_newspaper(newspaper, beginning=True)

    def save_data(self, crawl_newspaper=True, crawl_kols=False, crawl_kols_by_smcc=False):
        new_crawl_list = [WebConfig(x) for x in self._config['crawling_list'] if WebConfig(x).get_config('remove_me', False) != True]
        self.replace_crawl_list(new_crawl_list)

        if crawl_newspaper: # only save configs if crawl_newspaper
            with open_utf8_file_to_write(self._filename) as stream:
                yaml.dump(self._config, stream, default_flow_style=False, allow_unicode=True, sort_keys=False)

    def get_timeout(self, default=1000):
        if "timeout" in self._config:
            return int(self._config['timeout'])
        else:
            return default

    def get_use_CDN(self, default = False):
        return self.get_config('use_CDN', default)

    def get_trending_duration(self, default=600):
        if "trending_duration" in self._config:
            return int(self._config['trending_duration'])
        else:
            return default
    def get_hub_title(self):
        return self.get_config('hub_title', 'Theo Dõi Báo Chí')
    def get_hub_href(self):
        return self.get_config('hub_href', 'https://theodoibaochi.com')

    def get_minimum_freq_of_hot_growing_article(self, default=3):
        if "minimum_freq_of_hot_growing_article" in self._config:
            return int(self._config["minimum_freq_of_hot_growing_article"])
        else:
            return default

    def get_maximum_freq_of_hot_growing_article(self, default=10):
        if "maximum_freq_of_hot_growing_article" in self._config:
            return int(self._config["maximum_freq_of_hot_growing_article"])
        else:
            return default

    def get_minimum_word(self):
        return int(self._config['minimum_topic_length'])

    def get_config_dict(self):
        return self._config

    def get_config(self, config_string, default_value):
        if config_string not in self._config:
            self._config[config_string] = default_value
            return default_value
        else:
            try:
                return int(self._config[config_string])
            except:
                return self._config[config_string]

    def set_config(self, config_string, value):
        self._config[config_string] = value

    def print_crawl_list(self):
        print("Websites in crawling list:")
        newspaper_list = self.get_newspaper_list()
        index=0
        for newspaper in newspaper_list:
            index+=1
            print("%s. %s" % (str(index), newspaper.get_webname()))
        return newspaper_list

    def get_maximum_topic_display_length(self):
        return int(self.get_config('maximum_topic_display_length', 20))

    def get_maximum_day_difference(self):
        return int(self._config['days_to_crawl'])

    def get_display_timezone(self):
        '''
        output: pytz.timezone class
        '''
        try:
            result = pytz.timezone(self._config['display_timezone'])
        except:
            print("Wrong timezone format. Please provide one in tz database (google it)")
            print("Choose UTC by default")
            result = pytz.timezone("UTC")
        return result

    def get_newspaper_list(self):
        return [WebConfig(web) for web in self._config['crawling_list']]

    def add_newspaper(self, webconfig, beginning=False):

        found = False
        webname = webconfig.get_webname()

        # update old config if there is one
        for i in range(0, len(self._config['crawling_list'])):
            web = self._config['crawling_list'][i]
            if WebConfig(web).get_webname() == webname:
                self._config['crawling_list'][i] = webconfig._web
                found  = True

        # if not, add new config
        if not found:
            if not beginning:
                self._config['crawling_list'].append(webconfig._web)
            else:
                self._config['crawling_list'].insert(0, webconfig._web)

    def replace_crawl_list(self, newspaper_list):
        self._config['crawling_list'] = []
        for webconfig in newspaper_list:
            self.add_newspaper(webconfig)

    def print_config(self):
        '''
        note
        ====
        - print all properties without crawling list
        return
        ======
        list of (key, value) that is printed on screen
        '''
        config_list = []
        index = 0
        for key in self._config:
            value = self._config[key]
            if key != 'crawling_list':
                config_list.append((key, value))
                index+=1
                print("%s. %s: %s" % (str(index), key, str(value)))
        return config_list

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
        test_list = sorted(self._config['category_list'], key=lambda k: int(k[next(iter(k))]['index']))
        for category in test_list:
            name = next(iter(category))
            categories.append(Category(name=name, filename=category[name]['filename']))
        return categories

    def get_minimum_freq_for_two_length_keyword(self):
        return int(self._config['minimum_freq_for_two_length_keyword_appear_in_hot_keywords']) #this creates a threshold for two-word length keyword to appear in trending list

    def get_minimum_freq_for_more_than_two_length_keyword(self): # this creates a threshold for more than two-word-length keyword to appear in trending list
        return int(self._config['minimum_freq_for_more_than_two_length_keyword_appear_in_hot_keywords'])

    def get_minimum_freq_for_new_keyword(self): #this create a threshold for accepting a keyword a new keyword
        return int(self.get_config('minimum_freq_for_new_keyword_accepted', 1))

    def get_minimum_freq_for_fast_growing_keyword(self): #this create a threshold for a new keyword to be checked in fast_growing_keyword_dectector algorithm
        return int(self._config['minimum_freq_for_fast_growing_keyword_accepted'])

    def get_minimum_freq_series_for_fast_growing_keyword(self): #a new keyword must have updated several times to be checked in fast_growing_keyword_dectector algorithm
        return int(self._config['minimum_freq_series_for_fast_growing_keyword_accepted'])
    def get_minimum_keyword_length_for_fast_growing_keyword(self):
        return self.get_config('minimum_keyword_length_for_fast_growing_keyword_accepted', 3)

    def get_number_of_trending_keywords(self): #number of keywords to be listed in trending graph
        return int(self._config['number_of_trending_keywords'])

    def get_crawling_interval(self): #inveral in minutes between each crawling loop. This is important for to calculate exact time of each keyword_freq_time_series
        return int(self._config['crawling_interval'])

    def get_loop_interval_for_new_keyword_accepted(self): #new keyword must first appear in loop_interval back from current loop iterator. If crawling_interval = 10, loop_interval = 3, then new keyword appeart in 3*10 = 30 min from current time will be counted
        return int(self.get_config('loop_interval_for_new_keyword_accepted', 2))

    def get_minimum_publish_speed(self): # minimum articles published / minute for a keyword to be consider fast growing
        return int(self._config['minimum_publish_speed'])

    def get_maximum_url_to_visit_each_turn(self):
        return int(self._config['maximum_url_to_visit_each_turn'])
    def get_minimum_weight(self):
        return int(self._config['minimum_weight'])
    def get_max_crawler(self):
        return int(self._config['max_crawler'])

