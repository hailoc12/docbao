#####################################################################################################################
#Program: Doc bao theo tu khoa (keyword-based online journalism reader)
#Author: hailoc12
#Version: 1.0.0
#Date: 09/01/2018 
#Repository: http://github.com/hailoc12/docbao
#####################################################################################################################

# IMPORT LIB
from lib import *

# CHECK IF ANOTHER SESSION IS RUNNING

#Because unknown reason, os.remove() can't delete docbao.lock
#if is_another_session_running():
#    print("ANOTHER SESSION IS RUNNING !")
#    print("If you believe this is error, please delete docbao.lock file")
#    exit()
#else:
#    new_session()

# GLOBAL OBJECT

config_manager = ConfigManager(get_independent_os_path(['input', 'config.txt'])) #config object
data_manager = ArticleManager(config_manager, get_independent_os_path(["data", "article.dat"]),get_independent_os_path(["data","blacklist.dat"]) ) #article database object
keyword_manager = KeywordManager(data_manager, config_manager, get_independent_os_path(["data", "keyword.dat"]), get_independent_os_path(["input", "collocation.txt"]), get_independent_os_path(["input", "keywords_to_remove.txt"]))    #keyword analyzer object

# MAIN PROGRAM

# init data
config_manager.load_data()
data_manager.pull_blacklist_data() #fetch blacklist data from mysql database
keyword_manager.load_data()

# console output
version = "1.0.0"
print("DOC BAO VERSION " + version + "       Days to crawl: " + str(config_manager.get_maximum_day_difference()+1))

# crawling data
print("CRAWLING DATA")
for webconfig in config_manager.get_newspaper_list():
    data_manager.add_articles_from_newspaper(webconfig)

print("Number of new crawled articles: " + str(data_manager.count_database()))

data_manager.push_data() # push new articles and blacklist data to mysql database

# close firefox browser
quit_browser()

print("FINISH")
# clear lock file to finish this session
# finish_session()
