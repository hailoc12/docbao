#####################################################################################################################
#Program: Doc bao theo tu khoa (keyword-based online journalism reader)
#Author: hailoc12
#Version: 1.1.0
#Date: 09/01/2018
#Repository: http://github.com/hailoc12/docbao
#File: crawl.py
#Function: crawl data from newspaper and push to mysql database. It also supports multiprocessed crawling
#####################################################################################################################

from lib import *
if not is_another_session_running():
    new_session()
    try:
        crawler = Docbao_Crawler(
                crawl_newspaper=True,
                crawl_kols=False,
                crawl_kols_by_smcc=False,
                export_to_json=True,
                export_to_queue=True,
                export_to_elasticsearch=True,
                export_to_wordpress=False
                )
        crawler.load_data_from_file()
        crawler.multiprocess_crawl()
        crawler.save_data_to_redis()
        crawler.save_data_to_file()
    except:
        print_exception()
    finish_session()
else:
    print("Another session is running. Exit")

