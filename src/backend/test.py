from lib.browser_crawler import BrowserCrawler
from lib.config import ConfigManager
from lib.utils import get_independent_os_path
import os

# Test 1: Test firefox, geckodrive and selenium are installed ok
print("Test 1: check if Firefox, Geckodrive and Selenium are installed ok")
web_crawler = BrowserCrawler()
print("Try to load Dantri")
web_crawler.load_page("https://dantri.com.vn")
title = web_crawler.get_title()
print("title: %s" % title)

if title is not None: 
    print("Result: OK")
else:
    print("Result: FAIL")

print()
web_crawler.quit()

# Test 2: Check if config file is existed and can be parsed

print("Test 2: check if config file can be parsed")
base_dir = os.environ['DOCBAO_BASE_DIR']
config_file = get_independent_os_path([base_dir, "src", "backend", "input", "config.yaml"])

config_manager = ConfigManager(config_file)
config_manager.load_data()

if len(config_manager.get_newspaper_list()) >= 0:
    print("Result: OK")
else:
    print("Result: FAIL")
print()

