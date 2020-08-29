from .utils import *

# class reprents a single category that keyword belongs to
class Category:
    def __init__(self, name, filename):
        self._name = name
        self._filename = filename
        self._category_set = None
    def get_name(self):
        return self._name

    def get_filename(self):
        return self._filename

    def get_category_set(self):
        if self._category_set is None:
            with open_utf8_file_to_read(self._filename) as stream:
                self._category_set = set([keyword.strip().lower() for keyword in stream.readlines()])        
                stream.close()
        return self._category_set

