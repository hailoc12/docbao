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
    a = True
    while a:
    #try:
        while True:
            print("Crawler %s is running" % process_name)
            # get a web config from crawl_queue
            webconfig = None
            lock.acquire()
            if not crawl_queue.empty():
                webconfig = crawl_queue.get()
                lock.release()
                # crawl data
                print("Crawler %s is crawling newspaper %s" % (process_name, webconfig.get_webname()))
                data_manager.add_articles_from_newspaper(process_name, webconfig, browser)
            else:
                lock.release()
                print("Browser is")
                print(browser)

                if browser is not None:
                    print("Quit browser in Crawler %s" % process_name)
                    browser.quit()
                # output data to shared data
                    # push crawled articles to Queue
                print("Crawler %s is putting crawled data to main queues" % process_name)
                lock.acquire()
                for href, article in data_manager._data.items():
                    crawled_articles.put(article)
                    # push newly added blacklist to Queue
                for href, count in data_manager._new_blacklist.items():
                    new_blacklists.put((href, count))
                lock.release()
                print("Crawler %s has finished" % process_name)
                return None
        a= False
    #except:
    #    print("There are some error in crawler %s" % process_name)
    #    if browser is not None:
    #        print("Quit browser in Crawler %s" % process_name)
    #        browser.quit()

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
    config_list = config_manager.get_newspaper_list()
    number_of_job = len(config_list)
    for webconfig in config_list:
        crawl_queue.put(webconfig)

    # Start crawl process
    max_crawler = config_manager.get_max_crawler()
    time.sleep(1)
    print("%s crawlers are set to be run in parallel" % str(max_crawler))
    supported_max_crawler = get_max_crawler_can_be_run()
    if max_crawler > supported_max_crawler:
        time.sleep(1)
        print("Current system can support only %s crawlers to be run in parallel" % str(supported_max_crawler))
        time.sleep(1)
        print("You should reduce max_crawler in config.txt")
        time.sleep(1)
        print("max_crawler will be set to %s in this run" % str(supported_max_crawler))
        max_crawler = supported_max_crawler
    elif max_crawler < supported_max_crawler:
        time.sleep(1)
        print("Current system can support up to %s crawlers to be run in parallel" % str(supported_max_crawler))
        time.sleep(1)
        print("You should increase max_crawler in config.txt")
    if max_crawler > number_of_job:
        time.sleep(1)
        print("There are only %s newspaper to crawl" % str(number_of_job))
        time.sleep(1)
        print("max_crawler will be set to %s for efficience" % str(int(number_of_job / 2)))
        max_crawler = int(number_of_job / 2)

    crawler_processes = []
    time.sleep(1)
    print("Init %s crawlers" % str(max_crawler))

    timeout = config_manager.get_timeout()
    start = time.time()

    for i in range(max_crawler):
        crawler = multiprocessing.Process(target=crawler_process, args=(str(i+1), lock, crawl_queue, data_manager, crawled_articles, new_blacklists))
        crawler_processes.append(crawler)
        crawler.start()
        time.sleep(1)
        print("Start crawler number %s (pid: %s)" % (str(i+1), crawler.pid))

    # kill all process after timeout
    while time.time() - start <= timeout:
        print("Remaining seconds to timeout %s" % str(int(timeout - time.time() + start)))
        running = False
        running_crawler = ""
        count = 0
        for crawler in crawler_processes:
            count += 1
            if crawler.is_alive():
                running_crawler = running_crawler + " %s " % str(count)
                running = True
        if running:    
            print("Running crawler:")
            print(running_crawler)
            time.sleep(5)
        else:
            break
    else:
        print("Timeout, kill all processes")
        for crawler in crawler_processes:
            crawler.terminate()
            crawler.join()

    # join process to wait for all crawler to finish
    #for crawler in crawler_processes:
    #    crawler.join()
        
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

