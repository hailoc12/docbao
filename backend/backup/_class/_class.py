from _class._utility import *
from pyvi import ViTokenizer
from underthesea import *
import yaml
import re
import pickle
import jsonpickle
from datetime import datetime

# GLOBAL VARIABLES
count_duyet = 0
count_lay = 0
count_bo = 0

# CLASS DEFINITION

class Article:
    def __init__(self, href, topic, date, newspaper, summary = ""):
        self._href=href
        self._topic=topic
        self._date=date # date is string ìn format %d/%m%/%Y
        self._summary=summary
        self._newspaper=newspaper
        self._creation_date = datetime.now()
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

class ArticleManager:
    _data = dict()  # a dict of (href: article)
    _blacklist = dict()  # a dict if {href: lifecount}
    def __init__(self, config_manager, data_filename, blacklist_filename):
        self._config_manager = config_manager
        self._default_blacklist_count = 10 # will be removed after 10 compression
        self._data_filename = data_filename
        self._blacklist_filename = blacklist_filename

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

    def save_data(self):
        stream = open_binary_file_to_write(self._data_filename)
        pickle.dump(self._data, stream)
        stream.close()

        stream = open_binary_file_to_write(self._blacklist_filename)
        pickle.dump(self._blacklist, stream)
        stream.close()

    def get_sorted_article_list(self):
        article_list = list(self._data.values())
        article_list.sort(key=lambda x: x.get_creation_date(), reverse=True)
        return article_list

    def get_article(self, href):
        return self._data[href]

    def get_time_of_an_url(self, url, webconfig):
        try:
            soup = read_url_source_as_soup(url)
        except:
            return None
        datere = webconfig.get_date_re()
        datetag = webconfig.get_date_tag_list()
        dateclass = webconfig.get_date_class_list()
        filter = re.compile(datere)

        if datetag is not None:
            for tag in datetag:
                for foundtag in soup.find_all(tag):
                    tagstring = str(foundtag) # Get all html of tag
                    # for tagstring in foundtag.contents:
                    searchobj = filter.search(str(tagstring))
                    if searchobj:
                        return searchobj.group(1)
        else:
            for date in dateclass:
                for foundtag in soup.find_all(class_=date):
                    tagstring = str(foundtag) # Get all html of tag
                    #for tagstring in foundtag.contents:
                    searchobj = filter.search(str(tagstring))
                    if searchobj:
                        return searchobj.group(1)
        return None

    def is_a_valid_article(self, atag, webconfig, ):
        global count_bo
        fullurl = get_fullurl(webconfig.get_weburl(), atag['href'])
        topic_word_list = atag.string.split()
        print("Dang xu ly bai: " + atag.string.strip())
        if (len(topic_word_list) >= self._config_manager.get_minimum_word()):
            newsdate = self.get_time_of_an_url(fullurl, webconfig) #note: date is string
            if (newsdate is not None):
                print("Xuat ban ngay: " + newsdate)
                if is_not_outdated(newsdate, self._config_manager.get_maximum_day_difference()):
                    return True
                else:
                    print("Loai bai nay vi bai viet qua han")
                    count_bo+=1
                    return False
            else:
                print("Loai bai nay vi khong phai bai bao")
                count_bo += 1
                return False
        else:
            print("Loai bai nay vi tieu de khong du so tu cho phep")
            count_bo += 1
            return False

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
        print("Dang quet bao: " + webname)
        try:
            soup = read_url_source_as_soup(weburl)
            ataglist = soup.find_all("a", text=True, href=True)
            print("Dang lay du lieu, xin doi...")
            for atag in ataglist:
                # loc ket qua
                fullurl = get_fullurl(weburl, atag['href'])
                print("Dang xu ly trang: " + fullurl)
                count_duyet += 1

                if not self.is_blacklisted(fullurl):
                    if not self.is_in_database(fullurl):
                        if self.is_a_valid_article(atag, webconfig):
                            self.add_article(Article(topic=atag.string.strip(), date = datetime.strftime(get_date(self.get_time_of_an_url(fullurl,webconfig)), "%d/%m/%Y")
                                            , newspaper = webname, href=fullurl))
                            count_lay +=1
                            print("So bai viet da lay: " + str(count_lay))
                        else:
                            self.add_url_to_blacklist(fullurl)
                            print("Them vao blacklist")
                    else:
                        print("Bai nay da co trong co so du lieu")
                else:
                    print("Link nay nam trong blacklist")
                    self.refresh_url_in_blacklist(fullurl)
        except:
            print("Khong the mo bao: " + webname)

    def is_article_out_of_date_to_compress(self, article):
        return not is_not_outdated(article.get_date(), self._config_manager.get_maximum_day_difference())

    def is_article_topic_too_short(self, article):
        return len(article.get_topic().split()) < self._config_manager.get_minimum_word()

    def remove_article(self, article):
        self._data.pop(article.get_href())

    def count_database(self):
        return len(self._data)

    def count_blacklist(self):
        return len(self._blacklist)

    def count_articles_contain_keyword(self, keyword):
        count = 0
        for href in self._data:
            if keyword in self._data[href].get_topic().lower():
                count+=1
        return count

    def compress_database(self):
        remove = []
        for url, article in self._data.items():
            if self.is_article_out_of_date_to_compress(article) or self.is_article_topic_too_short(article):
                remove.append(article)
                self.add_url_to_blacklist(url)
        for article in remove:
            self.remove_article(article)


class Category:
    def __init__(self, name, filename):
        self._name = name
        self._filename = filename

    def get_name(self):
        return self._name

    def get_filename(self):
        return self._filename

class WebParsingConfig:
    def __init__(self, web):
        self._web = web # dict of dict {"webname":{"url":...,date_tag:[...], date_class:[...]}

    def get_webname(self):
        return next(iter(self._web))

    def get_weburl(self):
        return self._web[self.get_webname()]['url']

    def get_date_tag_list(self):
        return self._web[self.get_webname()]['date_tag']

    def get_date_class_list(self):
        return self._web[self.get_webname()]['date_class']

    def get_date_re(self):
        return self._web[self.get_webname()]['date_re']

class Keyword:
    def __init__(self, keyword, count):
        self._keyword = keyword
        self._count = count

class TagExtractor():
    _other_keyword_dict = None
    _hot_keyword_dict = None
    def __init__(self, data_manager, config_manager):
        self._data_manager = data_manager
        self._config_manager = config_manager
        self.__set_stopwords()
        self.get_collocation()

    def __set_stopwords(self):
        with open_utf8_file_to_read('keywords_to_remove.txt') as f:
            stopwords = set([w.strip().replace(' ', '_') for w in f.readlines()])
        self.stopwords = stopwords

    def get_collocation(self):
        with open_utf8_file_to_read("collocation.txt") as f:
            self._collocation =  set([w.strip() for w in f.readlines()])
    
    
    def smart_tokenize(self, sentence): # use under_the_sea tokenizer and pos_tag to keep noun phrase only
        print(sentence)
        tags = pos_tag(sentence)
        tokens = []
        noun_phrase = ""
        for i in range(0,len(tags)):
            if tags[i][1] in ["N", "Np", "Nu", "Nc", "M"]:
                if noun_phrase != "" and tags[i][0].strip() !="":
                    noun_phrase += " " + tags[i][0].strip()
                else:
                    noun_phrase = tags[i][0].strip()
            else:
                if noun_phrase != "" and len(noun_phrase.split()) >=2:
                    tokens.append(noun_phrase)
                noun_phrase = ""
        if noun_phrase != "" and len(noun_phrase.split()) >=2:
            tokens.append(noun_phrase)
            
        print(tokens)
        return tokens


    def segmentation(self, topic):
        # use collocation first
        temp1 = topic.lower()
        for collo in self._collocation:
            if collo in temp1:
                temp1 = temp1.replace(collo, collo.replace(' ','_'))
        #return ViTokenizer.tokenize(temp1)
        #return word_tokenize(temp1, format="text")
        return self.smart_tokenize(temp1)


    def split_words(self, topic):
        tokens = self.segmentation(topic)
        SPECIAL_CHARACTER = '0123456789%@$.,=+-!;/()*"&^:#|\n\t\''
        try:
            return [x.strip(SPECIAL_CHARACTER).lower() for x in tokens]
        except TypeError:
            return []

    def get_topic_keyword_list(self, topic):
        split_words = self.split_words(topic)
        return [word.replace('_', ' ') for word in split_words if word not in self.stopwords] #cau pop de loai bo keyword ''

    def get_keyword_dict(self):
        keyword_dict = dict()
        print("GET KEYWORD DICTIONARY")
        count = 0
        total = len(self._data_manager._data)

        for article in self._data_manager.get_sorted_article_list():
            count+=1
            print("Analysizing article " + str(count) + "/" + str(total) + ":")
            for keyword in self.get_topic_keyword_list(article.get_topic()):
                if keyword in keyword_dict and keyword != '':
                    keyword_dict[keyword.strip()]+=1
                else:
                    keyword_dict[keyword.strip()] = 1
        return keyword_dict

    def get_hot_keyword_dict(self):
        tag_dict = self.get_keyword_dict()
        hot_tag = dict()
        print("RECALCULATE KEYWORD APPERANCE")
        total = len(tag_dict)
        count = 0
        for keyword in tag_dict:
            count+=1
            print("Calculate keyword " + str(count) + "/" + str(total) + ": " + keyword)
            tag_dict[keyword] = self._data_manager.count_articles_contain_keyword(keyword)
        print("CHOOSE HOT KEYWORD DICTS")
        count = 0
        #for keyword in sorted(tag_dict, key=tag_dict.get, reverse=True): #get hot keyword based on count
        for keyword in sorted(tag_dict, key=len, reverse=True):           #get hot keywords based on length
            if count <= self._config_manager.get_hot_keyword_number():
                hot_tag[keyword]= tag_dict[keyword]
                count+=1
        self._hot_keyword_dict = hot_tag
        self._other_keyword_dict = dict(hot_tag)

    def get_hot_keyword_dict_by_category(self, category):
        if(category.get_name() == "Khác"): return self._other_keyword_dict
        else:
            try:
                with open_utf8_file_to_read(category._filename) as stream:
                    keyword_list = set([k.strip() for k in stream.readlines()])
                    category_keyword = dict()
                    if self._hot_keyword_dict is None:
                        self.get_hot_keyword_dict() # fill self._hot_keyword_dict and self._other_keyword_dict
                    for tag, count in self._hot_keyword_dict.items():
                        for keyword in keyword_list: # keyword must be lowercase
                            if keyword.strip()!="" and keyword in tag: # tag contain keyword
                                category_keyword[tag] = count
                                if tag in self._other_keyword_dict:
                                    self._other_keyword_dict.pop(tag)
                                break
                    stream.close()
                    return category_keyword
            except:
                open_utf8_file_to_write(category._filename).close()
                return dict()


    def write_keyword_dicts_to_json_files(self):
        category_list = list()
        for category in self._config_manager.get_categories():
            keyword_list = list()
            for keyword, count in self.get_hot_keyword_dict_by_category(category).items():
                keyword_list.append({"keyword": keyword, "count": count})
            category_list.append({"category": category.get_name(), "keywords": keyword_list})
        with open_utf8_file_to_write("keyword_dict.json") as stream:
            stream.write(jsonpickle.encode({"data": category_list}))
        stream.close()
    
    def write_hot_keyword_to_text_file(self):
        tag_dict = self.get_hot_keyword_dict()
        with open_utf8_file_to_write("hot_tag.txt") as stream:
            for keyword in sorted(tag_dict, key=tag_dict.get, reverse=True):
                stream.write(keyword + '\r\n')
            stream.close()

    def write_hot_keyword_to_json_file(self):
        max_hot_keyword = 100  
        if self._hot_keyword_dict is None:
            self.get_hot_keyword_dict()
        tag_dict = self._hot_keyword_dict
        count = 0
        hot_dict = dict()
        with open_utf8_file_to_write("hot_keyword.json") as stream:
            for keyword in sorted(tag_dict, key=tag_dict.get, reverse=True):
                if (len(keyword.split()) >=2 and tag_dict[keyword] >= 15) or (len(keyword.split()) >=3 and tag_dict[keyword] >= 6): #hot keywords is long enough and have at leats 4 sources mention
                    count+=1
                    if count <= max_hot_keyword:
                        hot_dict[keyword] = tag_dict[keyword] 
                        #hot_dict[keyword] = self._data_manager.count_articles_contain_keyword(keyword) # count by actual articles contain keywords
            stream.write(jsonpickle.encode(hot_dict))
            stream.close()

    def write_uncategoried_keyword_to_text_file(self):
        tag_dict = self.get_hot_keyword_dict_by_category(Category(name="Khác", filename=""))
        with open_utf8_file_to_write("uncategorized_keyword.txt") as stream:
            for keyword in sorted(tag_dict, key=tag_dict.get, reverse=True):
                stream.write(keyword + '\r\n')
            stream.close()


class ConfigManager:
    _filename = ""
    _config={}
    def __init__(self, filename):
        self._filename = filename

    def load_data(self):
        stream = open_utf8_file_to_read(self._filename)
        self._config = yaml.load(stream)

    def get_minimum_word(self):
        return int(self._config['so_tu_toi_thieu_cua_tieu_de'])

    def get_maximum_day_difference(self):
        return int(self._config['so_ngay_toi_da_lay_so_voi_hien_tai'])

    def get_newspaper_list(self):
        return [WebParsingConfig(web) for web in self._config['dia_chi_bao_can_quet']]

    def get_newspaper_count(self):
        return len(self._config['dia_chi_bao_can_quet'])

    def get_hot_tag_number(self):
        return int(self._config['so_hot_tag_toi_da'])

    def get_categories(self):
        categories = list()
        #for k in self._config['danh_sach_chuyen_muc']:
        #    print(k[next(iter(k))]['vi_tri_xuat_hien'])
        test_list = sorted(self._config['danh_sach_chuyen_muc'], key=lambda k: int(k[next(iter(k))]['vi_tri_xuat_hien']))
        for category in test_list:
            name = next(iter(category))
            categories.append(Category(name=name, filename=category[name]['filename']))
        return categories
