import urllib
from bs4 import BeautifulSoup
import re
import codecs
from datetime import datetime
import os
import urllib.request
from  lib.crawl import *
import time

_firefox_browser = None

# UTILITY FUNCTION
def is_another_session_running():
    return os.path.exists("docbao.lock")

def finish_session():
    os.remove("docbao.lock")

def new_session():
    with open_utf8_file_to_write("docbao.lock") as stream:
        stream.write("locked")
        stream.close()

def get_independent_os_path(path_list):
    path = ""
    for item in path_list:
        path = os.path.join(path, item)
    return path

def open_utf8_file_to_read(filename):
    try:
        return codecs.open(filename, "r", "utf-8")
    except:
        return None


def open_utf8_file_to_write(filename):
    try:
        return codecs.open(filename, "w+", "utf-8")
    except:
        return None


def open_binary_file_to_write(filename):
    try:
        return open(filename, "wb+")
    except:
        return None


def open_binary_file_to_read(filename):
    try:
        return open(filename, "rb")
    except:
        return None


def read_url_source_as_soup(url, use_browser=False, _firefox_browser=None, timeout=5):  # return page as soup of BeautifulSoup

    #f_hdr = {
    #    'User-Agent': UserAgent().chrome,
    #    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
    #    'Accept-Charset': 'ISO-8859-1,utf-8;q=0.7,*;q=0.3',
    #    'Accept-Encoding': 'none',
    #    'Accept-Language': 'en-US,en;q=0.8',
    #    'Connection': 'keep-alive'}

    hdr = {
        'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.11 (KHTML, like Gecko) Chrome/23.0.1271.64 Safari/537.11',
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
        'Accept-Charset': 'ISO-8859-1,utf-8;q=0.7,*;q=0.3',
        'Accept-Encoding': 'none',
        'Accept-Language': 'en-US,en;q=0.8',
        'Connection': 'keep-alive'}
    a=True
    result = False
    browser = None
    #while a:
    try:
        print(url)
        html_source = None
        if use_browser == False:
            req = urllib.request.Request(
                url,
                data=None,
                headers=hdr)
            f=None
            try:
                f = urllib.request.urlopen(req)
            except:
                f=None
            if f is None:
                result = False
            else:
                result = True
                html_source = f.read().decode('utf-8')
        else:
            print("Use Browser to open %s" % url)
            if _firefox_browser is not None:
                browser = _firefox_browser
            else:
                print("Create new instance of Firefox browser")
                browser = BrowserCrawler()
                _firefox_browser = browser
            print("Load page: %s" % url)
            result = browser.load_page(url, timeout, 5)
            print("Result %s" % str(result))
            if result == True:
                try:
                    time.sleep(3) # There must be little delay between browser.load_page and get_page_html
                    html_source = _firefox_browser.get_page_html() #Somehow this command occasionally have errors
                except:
                    result = False
        a = False
        if result == True:
            return BeautifulSoup(html_source,features="html.parser")
        else:
            return None
    except:
        print("Khong the mo trang: " + url)
        return None
def quit_browser():
    global _firefox_browser

    if _firefox_browser is not None:
        print("Found an running instance of Firefox. Close it")
        print(_firefox_browser)
        _firefox_browser.quit()

def is_not_outdated(date, ngay_toi_da):
    dateobj = get_date(date)
    return (datetime.now() - dateobj).days <= ngay_toi_da

def get_fullurl(weburl, articleurl):
    if re.compile("(http|https)://").search(articleurl):
        return articleurl
    else:
        return weburl + articleurl
