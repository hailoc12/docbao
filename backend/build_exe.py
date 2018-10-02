from distutils.core import setup
import py2exe
import urllib
from bs4 import BeautifulSoup
import yaml
import re
import xlsxwriter
import codecs
from datetime import datetime
import urllib.request

setup(console=['docbao.py'])
