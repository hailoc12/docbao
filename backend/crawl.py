#####################################################################################################################
#Program: Doc bao theo tu khoa (keyword-based online journalism reader)
#Author: hailoc12
#Version: 1.1.0
#Date: 09/01/2018 
#Repository: http://github.com/hailoc12/docbao
#File: crawl.py
#Function: crawl data from newspaper and push to mysql database. It also supports multiprocessed crawling
#####################################################################################################################

# IMPORT LIB
from lib import *
import multiprocessing
import os
import time

def crawler_process(process_name, lock, crawl_queue, data_manager, crawled_articles, new_blacklists):
    # Function: work as an worker in multiprocessed crawling
    # Input:
    #   lock: to acquire and release shared data
    #   crawl_queue: a shared queue of "crawl task"
    #   data_manager: an object that support method to crawl. Important: this object can't be shared by multiprocessing lib, so output data must be shared in another queue. But input data have cleared _data articles but initial _blacklists link
    #   blacklists: Queue that contain blacklist links
    #   crawled_articles: Queue that contain new crawled articles
    # Output:
    #   blacklists will contain new and old blacklisted links
    #   crawled_aritlces: contain new crawled articles

    print("Crawler %s has been started" % process_name)
    browser = BrowserWrapper()
    try:
        while True:
            # get a web config from crawl_queue
            webconfig = None
            lock.acquire()
            if not crawl_queue.empty():
                webconfig = crawl_queue.get()
                lock.release()
                # crawl data
                print("Crawler %s is crawling newspaper %s" % (process_name, webconfig.get_webname()))
                data_manager.add_articles_from_newspaper_async(process_name, lock, webconfig, browser)
            else:
                print("Browser is")
                print(browser)

                if browser is not None:
                    print("Quit browser in Crawler %s" % process_name)
                    browser.quit()
                print("Crawler %s has finished" % process_name)
                # output data to shared data
                    # push crawled articles to Queue
                for href, article in data_manager._data.items():
                    crawled_articles.put(article)
                    # push newly added blacklist to Queue
                for href, count in data_manager._new_blacklist.items():
                    new_blacklists.put((href, count))
                lock.release()
                return None
    except:
        if browser is not None:
            print("Quit browser in Crawler %s" % process_name)
            browser.quit()

# Create Manager Proxy to host shared data for multiprocessed crawled
with multiprocessing.Manager() as manager:
    time.sleep(1)
    print("Create Manager Proxy")
    time.sleep(1)
    print("Create shared object")
    # Create shared object
    config_manager = ConfigManager(get_independent_os_path(['input', 'config.txt'])) #config object
    data_manager = ArticleManager(config_manager, get_independent_os_path(["data", "article.dat"]),get_independent_os_path(["data","blacklist.dat"]) ) #article database object
    keyword_manager = KeywordManager(data_manager, config_manager, get_independent_os_path(["data", "keyword.dat"]), get_independent_os_path(["input", "collocation.txt"]), get_independent_os_path(["input", "keywords_to_remove.txt"]))    #keyword analyzer object
    crawl_queue = manager.Queue() 
    crawled_articles = manager.Queue()
    new_blacklists = manager.Queue()
    lock = manager.Lock()

    # Load data from file
    time.sleep(1)
    print("Load shared data from files")
    config_manager.load_data()
    data_manager.load_data()
    backup_old_articles = data_manager._data
    data_manager._data = dict()
    keyword_manager.load_data()
    
    # Init crawl queue
    time.sleep(1)
    print("Init crawl queue")
    for webconfig in config_manager.get_newspaper_list():
        crawl_queue.put(webconfig)

    # Start crawl process
    max_crawler = config_manager.get_max_crawler()
    crawler_processes = []
    time.sleep(1)
    print("Init %s crawlers" % str(max_crawler))
    for i in range(max_crawler):
        crawler = multiprocessing.Process(target=crawler_process, args=(str(i+1), lock, crawl_queue, data_manager, crawled_articles, new_blacklists))
        crawler_processes.append(crawler)
        crawler.start()
        time.sleep(1)
        print("Start crawler number %s (pid: %s)" % (str(i+1), crawler.pid))

    # join process to wait for all crawler to finish
    for crawler in crawler_processes:
        crawler.join()
        
    time.sleep(1)
    print("Finish crawling")
    time.sleep(1)
    print("New crawled articles")
    data_manager._data = backup_old_articles
    while not crawled_articles.empty():
        article = crawled_articles.get()
        data_manager._data[article._href] = article
        print("%s: %s" % (article.get_newspaper(), article.get_topic()))

    while not new_blacklists.empty():
        href, count = new_blacklists.get()
        data_manager._blacklist[href] = count

    # push crawled_articles to mysql
    time.sleep(1)
    
    # save data
    time.sleep(1)
    print("Save data")
    data_manager.compress_database(keyword_manager)
    data_manager.compress_blacklist()
    data_manager.save_data()

    # analyze keyword
    keyword_manager.build_keyword_list()

    # export data 
    data_manager.export_to_json()
    keyword_manager.write_trending_keyword_to_json_file()
    keyword_manager.write_keyword_dicts_to_json_files()

    keyword_manager.write_uncategorized_keyword_to_text_file() 
    keyword_manager.write_keyword_freq_series_to_json_file()

    # save data
    keyword_manager.save_data()

        # write log data
    with open_utf8_file_to_write(get_independent_os_path(["export", "log_data.json"])) as stream:
        log_dict = dict()
        log_dict['update_time'] = datetime.now().strftime("%d/%m/%Y %H:%M")
        log_dict['newspaper_count'] = str(config_manager.get_newspaper_count())
        log_dict['database_count'] = str(data_manager.count_database())
        stream.write(jsonpickle.encode(log_dict))
        stream.close()

print("FINISH")

