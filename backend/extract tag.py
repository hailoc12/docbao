# -*- coding: utf-8 -*-
from pyvi.pyvi import ViTokenizer
import codecs

def open_utf8_file_to_read(filename):
    try:
        return codecs.open(filename, "r", "utf-8")
    except:
        return None
class TagExtractor():
    def __init__(self, text = None):
        self.text = text
        self.__set_stopwords()

    def __set_stopwords(self):
        with open_utf8_file_to_read('keywords_to_remove.txt') as f:
            stopwords = set([w.strip().replace(' ', '_') for w in f.readlines()])
        self.stopwords = stopwords

    def segmentation(self):
        return ViTokenizer.tokenize(self.text)

    def split_words(self):
        text = self.segmentation()
        SPECIAL_CHARACTER = '0123456789%@$.,=+-!;/()*"&^:#|\n\t\''
        try:
            return [x.strip(SPECIAL_CHARACTER).lower() for x in text.split()]
        except TypeError:
            return []

    def get_topic_tag_list(self):
        split_words = self.split_words()
        return [word.replace('_', ' ') for word in split_words if word not in self.stopwords]

