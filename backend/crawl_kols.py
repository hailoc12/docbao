######################################################################
# Program: Crawl Facebook KOLs API                                   #
# Function: Provide API to crawl post, image of a specific FB account#
# Created: 16/07/2019                                                #
######################################################################

from lib import *
from flask import Flask

KOLS_LIST_FILEPATH = get_independent_os_path(['input', 'kols_list.txt'])

config_manager = ConfigManager(get_independent_os_path(['backend', 'input', 'config.yaml'])) #config object
data_manager = ArticleManager(config_manager, get_independent_os_path(['backend', "data", "article.dat"]),get_independent_os_path(['backend', "data","blacklist.dat"]) ) #article database object

app=Flask(__name__)

@app.route('/')
def index():
    return "Hello World"

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
