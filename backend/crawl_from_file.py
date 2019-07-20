#####################################################################################################################
#Program: Doc bao theo tu khoa (keyword-based online journalism reader)
#Author: hailoc12
#Version: 1.1.0
#Date: 09/01/2018 
#Repository: http://github.com/hailoc12/docbao
#File: crawl_from_file.py
#Function: crawl data from file, analyse and push to frontend 
#####################################################################################################################

# IMPORT LIB
from lib import *
import os
import time

config_manager = ConfigManager(get_independent_os_path(['input', 'config.txt'])) #config object

data_manager = ArticleManager(config_manager, get_independent_os_path(["data", "article.dat"]),get_independent_os_path(["data","blacklist.dat"]) ) #article database object

keyword_manager = KeywordManager(data_manager, config_manager, get_independent_os_path(["data", "keyword.dat"]), get_independent_os_path(["input", "collocation.txt"]), get_independent_os_path(["input", "keywords_to_remove.txt"]))    #keyword analyzer object

print("Load shared data from files")
config_manager.load_data()

# load data from files
articles=[]
with open_utf8_file_to_read(get_independent_os_path(['input', 'article_data.json'])) as f:
    articles = jsonpickle.encode(f.read())['article_list']

for article in articles:
    article_date = strptime(article['publish_time'], "%d-%m-%y %H:%M")

    item = Article(article_id=article['id'], href=article['href'], topic=article['topic'], date=article_date, newspaper = article['newspaper'], language=article['language'])

print("%s: %s" % (article.get_newspaper(), article.get_topic()))

data_manager.add_article(item)

# analyze keyword

keyword_manager.build_keyword_list()

# export data 
data_manager.export_to_json()
#keyword_manager.write_keyword_dicts_to_json_files()
#keyword_manager.write_keyword_freq_series_to_json_file()
keyword_manager.write_trending_keyword_by_growing_speed_to_json_file()
keyword_manager.write_fast_growing_keyword_to_json_file()
keyword_manager.write_uncategorized_keyword_to_text_file() 
keyword_manager.write_trending_article_to_json_file()
keyword_manager.write_hot_growing_article_to_json_file()
keyword_manager.write_keyword_dicts_to_json_file()
keyword_manager.write_keyword_freq_series_to_json_file()

# write log data
with open_utf8_file_to_write(get_independent_os_path(["export", "log_data.json"])) as stream:
    log_dict = dict()
    log_dict['update_time'] = datetime.now().strftime("%d/%m/%Y %H:%M")
    log_dict['newspaper_count'] = str(config_manager.get_newspaper_count())
    log_dict['database_count'] = str(data_manager.count_database())
    stream.write(jsonpickle.encode(log_dict))
    stream.close()

print("FINISH")

