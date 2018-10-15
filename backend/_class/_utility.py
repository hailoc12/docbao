import urllib
from bs4 import BeautifulSoup
import re
import codecs
from datetime import datetime
import os
import urllib.request
from fake_useragent import UserAgent
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


def read_url_source_as_soup(url):  # return page as soup of BeautifulSoup
    f_hdr = {
        'User-Agent': UserAgent().chrome,
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
        'Accept-Charset': 'ISO-8859-1,utf-8;q=0.7,*;q=0.3',
        'Accept-Encoding': 'none',
        'Accept-Language': 'en-US,en;q=0.8',
        'Connection': 'keep-alive'}

    hdr = {
        'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.11 (KHTML, like Gecko) Chrome/23.0.1271.64 Safari/537.11',
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
        'Accept-Charset': 'ISO-8859-1,utf-8;q=0.7,*;q=0.3',
        'Accept-Encoding': 'none',
        'Accept-Language': 'en-US,en;q=0.8',
        'Connection': 'keep-alive'}
    #a=True
    #while a:
    try:
        print(url)
        req = urllib.request.Request(
            url,
            data=None,
            headers=hdr)
        f = urllib.request.urlopen(req)
        return BeautifulSoup(f.read().decode('utf-8'),features="html.parser")
        #a = False
    except:
        print("Khong the mo trang: " + url)
        return None

def is_not_outdated(date, ngay_toi_da):
    dateobj = get_date(date)
    return (datetime.now() - dateobj).days <= ngay_toi_da

def get_fullurl(weburl, articleurl):
    if re.compile("(http|https)://").search(articleurl):
        return articleurl
    else:
        return weburl + articleurl
