# IMPORT LIB
import xlsxwriter
from lib import *
import jsonpickle

# GLOBAL OBJECT
config_manager = ConfigManager(get_independent_os_path(['input', 'config.txt'])) #config object
data_manager = ArticleManager(config_manager, get_independent_os_path(["data", "article.dat"]),get_independent_os_path(["data","blacklist.dat"]) ) #article database object
keyword_manager = KeywordManager(data_manager, config_manager, get_independent_os_path(["data", "keyword.dat"]), get_independent_os_path(["input", "collocation.txt"]), get_independent_os_path(["input", "keywords_to_remove.txt"]))    #keyword analyzer object

class NewKeywordDetector:
    def __init__(self, keyword_manager, config_manager, filename):
        self._keyword_manager = keyword_manager
        self._config_manager = config_manager
        self._filename = filename
        self._new_keyword =list() 
    def detect_new_keyword(self):
        print("DETECT NEW KEYWORDS")
        #keyword first appear in three iterator will be considered new keyword
        keyword_list = self._keyword_manager._optimized_keyword_list
        new_keyword = self._new_keyword 
        current_iterator = self._keyword_manager._series_iterator
        count = 0
        print("Current iterator: " + str(current_iterator))
        min_freq = self._config_manager.get_minimum_freq_for_new_keyword()
        loop_interval = self._config_manager.get_loop_interval_for_new_keyword_accepted()
        for item in keyword_list:
            print("Processing keyword: " + item.get_keyword())
            if item.get_len_of_freq_series() >= 1 and current_iterator - item.get_first_iterator() <= loop_interval and item.get_freq_series() >= min_freq and item.get_keyword_length() > 2:
                new_keyword.append({"keyword":item.get_keyword(),"count": item.get_freq_series()})
                count+=1
                print("Found " + str(count) + " new keywords: " + item.get_keyword())

    def write_new_keyword_to_json_file(self):
        with open_utf8_file_to_write(self._filename) as stream:
            stream.write(jsonpickle.encode(self._new_keyword))
            stream.close()
            
class FastGrowingKeywordDetector:
     def __init__(self, keyword_manager, config_manager, filename):
        self._keyword_manager = keyword_manager
        self._config_manager = config_manager
        self._filename = filename
        self._fast_growing_list = list() 
     def detect_fast_growing_keyword(self):
        print("DETECT FAST GROWING KEYWORDS")
        keyword_list = self._keyword_manager._optimized_keyword_list
        result = self._fast_growing_list
        iterator = self._keyword_manager._series_iterator
        count = 0
        print("Current iterator: " + str(iterator))
        # a fast growing keyword is a keyword being updated frequently and have growth rate less than 5 min / article  
        min_freq_series = self._config_manager.get_minimum_freq_series_for_fast_growing_keyword()
        min_freq = self._config_manager.get_minimum_freq_for_fast_growing_keyword()
        crawl_interval = self._config_manager.get_crawling_interval()
        publish_speed = self._config_manager.get_minimum_publish_speed()
        for item in keyword_list:
            length = item.get_len_of_freq_series()
            last_iterator= item.get_last_iterator()
            print("Processing keyword: " + item.get_keyword())
            if length >= min_freq_series and item.get_keyword_length() > 2:
                first_iterator = item.get_first_iterator()
                duration = (iterator - first_iterator) * crawl_interval
                speed = duration / item.get_freq_series() 
                if speed < publish_speed:
                    count+=1
                    print("Found " + str(count) + " fast growing keywords: " + item.get_keyword())
                    print("Duration: " + str(duration))
                    print("Articles: " + str(item.get_freq_series()))
                    print("Speed: " + str(speed) + " min/article")
                    result.append({"keyword":item.get_keyword(),"count": item.get_freq_series()})

     def write_fast_growing_keyword_to_json_file(self):
        with open_utf8_file_to_write(self._filename) as stream:
            stream.write(jsonpickle.encode(self._fast_growing_list))
            stream.close()
   
#MAIN PROGRAM
print("DETECT SPECIAL KEYWORDS")
#load data
config_manager.load_data()
keyword_manager.load_data()

#special keywords detecting
new_keyword_detector = NewKeywordDetector(keyword_manager,config_manager, get_independent_os_path(["export", "new_keyword.json"]))
new_keyword_detector.detect_new_keyword()
new_keyword_detector.write_new_keyword_to_json_file()

fast_growing_detector = FastGrowingKeywordDetector(keyword_manager, config_manager, get_independent_os_path(["export", "fast_growing_keyword.json"]))
fast_growing_detector.detect_fast_growing_keyword()
fast_growing_detector.write_fast_growing_keyword_to_json_file()

print("FINISH")
