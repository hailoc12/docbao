from lib.crawl import *
from lib.config import * 
from lib.utils import *

web_crawler = BrowserCrawler()

# Test 1: Test firefox, geckodrive and selenium are installed ok
print("Test 1: check if Firefox, Geckodrive and Selenium are installed ok")

web_crawler.load_page("http://dantri.com.vn", 2, 0.5)
title = web_crawler.get_title()

if "Dân trí" in title:
    print("Result: OK")
else:
    print("Result: FAIL")

print()
web_crawler.quit()

# Test 2: Check if config file is existed and can be parsed

print("Test 2: check if config file can be parsed")

config_file = get_independent_os_path(["input", "config.txt"])

config_manager = ConfigManager(config_file)
config_manager.load_data()

if len(config_manager.get_newspaper_list()) > 0:
    print("Result: OK")
else:
    print("Result: FAIL")
print()

