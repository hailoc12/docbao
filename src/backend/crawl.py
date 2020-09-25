#####################################################################################################################
#Program: Doc bao theo tu khoa (keyword-based online journalism reader)
#Author: hailoc12
#Version: 1.1.0
#Date: 09/01/2018
#Repository: http://github.com/hailoc12/docbao
#File: crawl.py
#####################################################################################################################

from src.backend.lib.utils import new_session, is_another_session_running, print_exception, finish_session
from src.backend.lib.utils import get_independent_os_path
from src.backend.lib.docbao_crawler import Docbao_Crawler
import os

if not is_another_session_running():
    new_session()
    try:
        crawler = Docbao_Crawler(
                crawl_newspaper=True,
                crawl_kols=False,
                crawl_kols_by_smcc=False,
                export_to_json=True,
                export_to_queue=os.environ['DOCBAO_EXPORT_TO_RABBITMQ']=='true',
                export_to_elasticsearch=os.environ['DOCBAO_EXPORT_TO_ELASTICSEARCH']=='true',
                export_to_wordpress=os.environ['DOCBAO_EXPORT_TO_WORDPRESS']=='true'
                )
        crawler.load_data_from_file()
        crawler.multiprocess_crawl()
        crawler.save_data_to_file()
    except:
        print_exception()
    finish_session()
else:
    print("Another session is running. Exit")

