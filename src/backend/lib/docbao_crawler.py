
# IMPORT LIB:
import copy
from src.backend.lib.data import Article, ArticleManager
from src.backend.lib.config import ConfigManager
from src.backend.lib.keyword import KeywordManager
from src.backend.lib.elasticsearch_data import ElasticSearch_Client
from src.backend.lib.rabbitmq_client import RabbitMQ_Client
from src.backend.lib.wordpress import Wordpress
from src.backend.lib.browser_crawler import BrowserWrapper, BrowserCrawler
from src.backend.lib.utils import get_independent_os_path, get_utc_now_date
from src.backend.lib.utils import print_exception, get_max_crawler_can_be_run
from src.backend.lib.utils import open_utf8_file_to_write, get_date_string

#from backend.lib import *
import multiprocessing
import os
import time
import epdb
import jsonpickle


def _print_crawl_queue(queue):
    """Print crawl_queue for debug"""
    temp = []
    print("Print crawl_queue for debugging")
    while not queue.empty():
        config = queue.get()
        temp.append(config)
        print(config.get_crawl_url())
    for config in temp:
        queue.put(config)


class Docbao_Crawler():

    _crawl_newspaper=True
    _crawl_kols = False

    def __init__(self, crawl_newspaper=True, crawl_kols=False, crawl_kols_by_smcc = False, max_kols=100,
                 export_to_json=True, export_to_queue=False, export_to_elasticsearch=False, export_to_wordpress=False):
        '''
        input
        -----
        max_kols: max random-get kols will be crawl  in this turn
        '''
        self._crawl_kols = crawl_kols
        self._crawl_newspaper = crawl_newspaper
        self._crawl_kols_by_smcc = crawl_kols_by_smcc
        self._export_to_json = export_to_json
        self._export_to_queue = export_to_queue
        self._export_to_elasticsearch = export_to_elasticsearch
        self._export_to_wordpress = export_to_wordpress

        base_dir = os.environ['DOCBAO_BASE_DIR']

        # Create shared object
        self._config_manager = ConfigManager(get_independent_os_path([base_dir, 'src', 'backend', 'input', 'config.yaml']),
                                            get_independent_os_path([base_dir, 'src', 'backend', 'input', 'kols_list.txt']),
                                            get_independent_os_path([base_dir, 'src', 'backend', 'input', 'fb_list.txt'])) #config object

        self._data_manager = ArticleManager(self._config_manager, get_independent_os_path([base_dir, 'src', 'backend', 'data', 'article.dat']),get_independent_os_path([base_dir, 'src', 'backend', "data","blacklist.dat"]) ) #article database object
        self._keyword_manager = KeywordManager(self._data_manager, self._config_manager, get_independent_os_path([base_dir, 'src', 'backend', "data", "keyword.dat"]), get_independent_os_path([base_dir, 'src', 'backend', "input", "collocation.txt"]), get_independent_os_path(["input", "keywords_to_remove.txt"]))    #keyword analyzer object

    def load_data_from_file(self):
        # Load data from file
        self._config_manager.load_data(crawl_newspaper=self._crawl_newspaper, crawl_kols=self._crawl_kols, crawl_kols_by_smcc=self._crawl_kols_by_smcc)
        self._data_manager.load_data()
        self._keyword_manager.load_data()

        self._data_manager.compress_database(self._keyword_manager)
        self._data_manager.compress_blacklist()

    def save_data_to_file(self):
        print("Save data to file")
        self._data_manager.save_data()
        self._keyword_manager.save_data()
        self._config_manager.save_data(self._crawl_newspaper, self._crawl_kols)

    def crawler_process(self, process_name, lock, timeout_flag, browser_list, crawl_queue, data_manager, crawled_articles, new_blacklists, export_to_queue):
        # Function: work as an worker in multiprocessed crawling
        # Input:
        #   timeout_flag: shared variable to check if timeout happen
        #   lock: to acquire and release shared data
        #   browser_list: a shared queue of browser to release when timeout
        #   crawl_queue: a shared queue of "crawl task"
        #   data_manager: an object that support method to crawl. Important: this object can't be shared by multiprocessing lib, so output data must be shared in another queue. But input data have cleared _data articles but initial _blacklists link
        #   blacklists: Queue that contain blacklist links
        #   crawled_articles: Queue that contain new crawled articles
        #   push_to_queue: push new crawled articles to rabbit queue
        # Output:
        #   blacklists will contain new and old blacklisted links
        #   crawled_aritlces: contain new crawled articles

        print("Crawler %s has been started" % process_name)

        browser = BrowserWrapper()
        lock.acquire()
        browser_list.put(browser)
        lock.release()

        non_job_list = []
        job_list = []
        finish = False
        a = True
        browser_profile = None
        try:
            while True:
                print("Crawler %s is running" % process_name)
                # get a web config from crawl_queue
                webconfig = None

                # get current profile of current browser
                # process browser can only crawl task that have the same profile
                if browser.get_browser() is not None:
                    browser_profile = browser.get_profile()
                lock.acquire()

                # epdb.set_trace()
                # this browser have more job (in job_list) or global queue have more job not timeout
                if (not crawl_queue.empty() or job_list) and not finish and (timeout_flag.value == 0):

                    if len(job_list) > 0: # has job
                        webconfig = job_list.pop()

                    else: # first job or ready to get more "default profile" job
                        if browser_profile is None:       # first job. Use next webconfig to create browser
                            # _print_crawl_queue(crawl_queue)
                            webconfig = crawl_queue.get()
                            browser_profile = webconfig.get_browser_profile()

                            if browser_profile != '': # not default profile
                                while (not crawl_queue.empty()):  # get all job for this browser profile
                                    temp_webconfig = crawl_queue.get()
                                    if temp_webconfig.get_browser_profile() == browser_profile:
                                        job_list.append(temp_webconfig)
                                    else:
                                        non_job_list.append(temp_webconfig)

                                while len(non_job_list) > 0: # push back non-job to queue
                                    crawl_queue.put(non_job_list.pop())
                                # _print_crawl_queue(crawl_queue)

                            else:
                                pass # any other default browser can get job
                            # use webconfig as first job to crawl

                        elif browser_profile == '': # get more "default profile" job
                            webconfig = crawl_queue.get()
                            browser_profile = webconfig.get_browser_profile()

                            if browser_profile != '': # not default profile
                                non_job_list.append(webconfig)
                                found = False
                                #epdb.set_trace()
                                while (not crawl_queue.empty()):  # get all job for this browser profile
                                    temp_webconfig = crawl_queue.get()
                                    if temp_webconfig.get_browser_profile() == '':
                                        job_list.append(temp_webconfig) # get one job only
                                        found = True
                                        break
                                    else:
                                        non_job_list.append(temp_webconfig)

                                while len(non_job_list) > 0: # push back non-job to queue
                                    crawl_queue.put(non_job_list.pop())

                                if not found:
                                    finish = True # no more default profile job
                                    lock.release()
                                    continue # kill browser in the next while

                            else:
                                pass # use webconfig to crawl

                        else: # all job for this browser profile are done
                            # push back data
                            finish = True
                            lock.release()
                            continue # kill browser in the next while

                    # webconfig is first job or next job in job_list to crawl
                    lock.release()

                    # crawl data
                    # epdb.set_trace()
                    crawl_type = webconfig.get_crawl_type()
                    if crawl_type == "newspaper":
                        print("Crawler %s is crawling newspaper %s" % (process_name, webconfig.get_webname()))
                        data_manager.add_articles_from_newspaper(process_name, webconfig, browser)
                    elif 'facebook' in crawl_type: # facebook user, facebook fanpage/groups
                        print("Crawler %s is crawling FB %s" % (process_name, webconfig.get_webname()))
                        data_manager.add_articles_from_facebook(process_name, webconfig, browser)
                    elif 'kols smcc' in crawl_type: # facebook user, facebook fanpage/groups
                        print("Crawler %s is crawling Kols post by using smcc service" % process_name)
                        data_manager.add_articles_from_facebook_by_smcc(process_name, webconfig)

                    time.sleep(10)

                else: # timeout or no more job left
                    if timeout_flag.value != 0:
                        print("Crawler %s: timeout is detected. Finish" % process_name)
                    elif crawl_queue.empty() and (not job_list):
                        print("Crawler %s: no more job for this crawler. Finish" % process_name)

                    lock.release()

                    if browser is not None:
                        print("Quit browser in Crawler %s" % process_name)
                        browser.quit()
                    # output data to shared data
                        # push crawled articles to Queue
                    print("Crawler %s is putting crawled data to main queues" % process_name)
                    lock.acquire()
                    print("Number of articles: %s" % str(len(data_manager._data)))

                    new_articles = []
                    for article_id, article in data_manager._new_article.items():
                        crawled_articles.put(article)
                        new_articles.append(article)
                        # push newly added blacklist to Queue

                    # push data
                    print("Crawler %s: Push new crawled articles to database " % process_name)
                    if export_to_queue:
                        try:
                            # push to RabbitMQ # for Bangtin project only
                            rb = RabbitMQ_Client()
                            rb.connect()
                            rb.push_to_queue(new_articles) # put new newspaper article to RabbitMQ
                            rb.disconnect()
                        except:
                            print_exception()

                    for href, count in data_manager._new_blacklist.items():
                        new_blacklists.put((href, count))
                    lock.release()
                    print("Crawler %s has finished" % process_name)
                    return None
        except:
            print_exception()
            print("There are some error in crawler %s" % process_name)
            if browser is not None:
                print("Quit browser in Crawler %s" % process_name)
                browser.quit()

    def multiprocess_crawl(self):
        # Create Manager Proxy to host shared data for multiprocessed crawled
        with multiprocessing.Manager() as manager:

            data_manager = self._data_manager
            config_manager = self._config_manager
            keyword_manager = self._keyword_manager

            time.sleep(1)
            print("Create Manager Proxy")
            time.sleep(1)
            print("Create shared object")
            crawl_queue = manager.Queue()
            crawled_articles = manager.Queue()
            new_blacklists = manager.Queue()
            browser_list = manager.Queue() # keep all firefox browser to release when timeout
            lock = manager.Lock()
            timeout_flag = manager.Value('i', 0) # shared variable to inform processes if timeout happends

            # Init crawl queue
            time.sleep(1)
            print("Init crawl queue")
            config_list = config_manager.get_newspaper_list()
            number_of_job = 0

            for webconfig in config_list:
                # check delay time between crawl
                last_run = webconfig.get_last_run()
                min_duration = webconfig.get_minimum_duration_between_crawls()
                time_pass =  int((get_utc_now_date() - last_run).total_seconds() / 60)

                if time_pass > min_duration:
                    # print("Print crawl_queue:")
                    # print(webconfig.get_crawl_url()) # for debug
                    crawl_queue.put(webconfig)
                    number_of_job+=1
                    webconfig.set_last_run() # set last_run to now
                else:
                    web_name = webconfig.get_webname()
                    print("Ignore crawling %s. Need more %d minutes more to crawl" % (web_name, min_duration - time_pass))

            # Start crawl process
            max_crawler = config_manager.get_max_crawler()
            time.sleep(1)
            print("%s crawlers are set to be run in parallel" % str(max_crawler))
            supported_max_crawler = get_max_crawler_can_be_run()
            if supported_max_crawler == 0:
                supported_max_crawler = 1
            if max_crawler > supported_max_crawler:
                time.sleep(1)
                print("Current system can support only %s crawlers to be run in parallel" % str(supported_max_crawler))
                time.sleep(1)
                print("You should reduce max_crawler in config.yaml")
                time.sleep(1)
                print("max_crawler will be set to %s in this run" % str(supported_max_crawler))
                max_crawler = supported_max_crawler
            elif max_crawler < supported_max_crawler:
                time.sleep(1)
                print("Current system can support up to %s crawlers to be run in parallel" % str(supported_max_crawler))
                time.sleep(1)
                print("You should increase max_crawler in config.yaml")
            if max_crawler > int(number_of_job/2):
                time.sleep(1)
                print("There are only %s newspaper to crawl" % str(number_of_job))
                time.sleep(1)
                print("max_crawler will be set to %s for efficience" % str(int(number_of_job / 2)+1))
                max_crawler = int(number_of_job / 2) + 1

            crawler_processes = []
            time.sleep(1)

            print("Can run max to %s crawlers" % str(max_crawler))

            timeout = config_manager.get_timeout()
            start = time.time()

            alive_crawler = 0

            running = True
            start_timeout = 0
            is_timeout = False
            terminate_time = 120 # 2 min
            crawler_iterator = 0

            while running:
                # count alive crawler
                running_crawler = ''
                alive_crawler = 0
                running = False
                for process in crawler_processes:
                    if process.is_alive():
                        alive_crawler +=1
                        running_crawler = running_crawler + " %s " % str(alive_crawler)
                        running = True
                if running:
                    print("Running crawler:")
                    print(running_crawler)
                else: # not running process
                    lock.acquire()
                    if crawl_queue.empty():
                        lock.release()
                        break
                    running = True
                    lock.release()


                # create new crawler if needed
                lock.acquire()
                if alive_crawler < max_crawler and not crawl_queue.empty() and not is_timeout: # have more jobs that current browser can't crawl. Maybe need another browser_profiles
                    #epdb.set_trace()
                    lock.release()
                    print("Can create more crawler")
                    crawler_iterator +=1
                    crawler = multiprocessing.Process(target=self.crawler_process, args=(str(crawler_iterator), lock, timeout_flag, browser_list, crawl_queue, data_manager, crawled_articles, new_blacklists, self._export_to_queue))
                    crawler_processes.append(crawler)
                    crawler.start()
                    time.sleep(1)
                    print("Start crawler number %s (pid: %s)" % (str(crawler_iterator), crawler.pid))
                else:
                    lock.release()

                # kill all process after timeout
                if not is_timeout:
                    print("Remaining seconds to timeout %s" % str(int(timeout - time.time() + start)))
                else:
                    print("Remaining seconds to terminate %s" % str(int(terminate_time - time.time() + start_timeout)))
                if (time.time() - start > timeout) and (not is_timeout):
                    start_timeout = time.time()

                    print("Timeout")
                    print("Inform all processes about timeout. Terminate all after 2 min")
                    lock.acquire()
                    timeout_flag.value = 1
                    lock.release()
                    is_timeout = True

                if (timeout_flag.value == 1) and (time.time() - start_timeout >= terminate_time):
                    print("Kill unquited browser")
                    while not browser_list.empty():
                        lock.acquire()
                        browser = browser_list.get()
                        print("Found a running browser")
                        print(browser)
                        print("Close browser")
                        browser.quit()
                        lock.release()
                    print("Kill all processes")
                    for crawler in crawler_processes:
                        crawler.terminate()
                        # some processes may be not terminate. Don't know why
                        #crawler.join()
                    running = False

                time.sleep(10)

            # join process to wait for all crawler to finish
            #for crawler in crawler_processes:
            #    crawler.join()

            time.sleep(1)
            print("Finish crawling")
            time.sleep(1)

            # Save all new crawled articles and push to ElasticSearch + RabbitMQ
            print("New crawled articles")
            rb = RabbitMQ_Client()
            rb_articles = []

            while not crawled_articles.empty():
                article = crawled_articles.get()
                if article.get_id() not in data_manager._data:
                    data_manager._data[article.get_id()] = article # merge new articles to data
                    rb_articles.append(article)
                    print("%s: %s" % (article.get_newspaper(), article.get_topic()))

            while not new_blacklists.empty():
                href, count = new_blacklists.get()
                data_manager._blacklist[href] = count

            # analyze keyword
            print("Analyze keywords")
            keyword_manager.build_keyword_list()

            print("Export data to json files")


            # export data
            trending_keywords = keyword_manager.write_trending_keyword_by_growing_speed_to_json_file()

            if self._export_to_json:
                data_manager.export_to_json()
                keyword_manager.write_fast_growing_keyword_to_json_file()
                keyword_manager.write_uncategorized_keyword_to_text_file()
                keyword_manager.write_trending_article_to_json_file()
                keyword_manager.write_hot_growing_article_to_json_file()
                keyword_manager.write_keyword_dicts_to_json_file()
                keyword_manager.write_keyword_freq_series_to_json_file()
                keyword_manager.write_new_keyword_to_json_file()

            trends=[]

            for topic in trending_keywords[:min(40, len(trending_keywords))]:
                print('trending topic: %s' % topic)

                articles = data_manager.get_latest_article_contain_keyword(topic, number=6)
                first_article = articles[0]
                posts=[]

                print('relate article: ')
                for article in articles:
                    posts.append(str(article.get_id()))
                    print(article.get_topic())

                print(posts)
                #trends.append({'topic': topic, 'posts': posts})
                trends.append({'topic': first_article.get_topic(), 'posts': posts})

            # push data
            print("Push data to database and other services")
            if self._export_to_queue:
                try:
                    # push to RabbitMQ # for Bangtin project only
                    rb.connect()
                    rb.push_trends_to_queue(trends)
                    rb.disconnect()
                except:
                    print_exception()

            if self._export_to_wordpress:
                try:
                    # push to wordpress
                    wp = Wordpress()
                    for article in rb_articles:
                        if article.get_post_type() == 0: # newspaper post
                            topic = article.get_topic().lower()
                            # trending = False
                            # if trending_keywords:
                            #     for keyword in trending_keywords:
                            #         if keyword in topic:
                            #             trending = True
                            #             break

                            post_id = wp.add_new_article(article, [])
                            if post_id:
                                article.set_wordpress_id(post_id)
                            #sleep(15) # avoid being banned by wordpress host
                except:
                    print_exception()


            if self._export_to_elasticsearch:
                try:
                    # push to Elasticsearch
                    es = ElasticSearch_Client()
                    for article in rb_articles:
                        es.push_article(article) # put new article to ElasticSearch

                except:
                    print_exception()

            # write log data
            try:
                with open_utf8_file_to_write(get_independent_os_path(["export", "log_data.json"])) as stream:
                    log_dict = dict()
                    update_time = get_date_string(get_utc_now_date(), date_format="%d/%m/%Y %H:%M", timezone=config_manager.get_display_timezone())
                    log_dict['update_time'] = update_time
                    log_dict['newspaper_count'] = str(config_manager.get_newspaper_count())
                    log_dict['database_count'] = str(data_manager.count_database())
                    log_dict['hub_title'] = config_manager.get_hub_title()
                    log_dict['hub_href'] = config_manager.get_hub_href()
                    stream.write(jsonpickle.encode(log_dict))
                    stream.close()
            except:
                print_exception()

        print("FINISH")
