###############################################################################
# Program: Docbao Search                                                      #
# Function: Search specific keywords in Docbao database                       #
# Author: hailoc12                                                            #
# Created: 2019-08-15                                                         #
###############################################################################


from lib import ConfigManager, ArticleManager, get_independent_os_path, get_date_string

if __name__ == '__main__':
    # load database
    config_manager = ConfigManager(get_independent_os_path(['input', 'config.yaml']),
                                   get_independent_os_path(['input', 'kols_list.txt']),
                                   get_independent_os_path(['input', 'fb_list.txt'])) #config object

    data_manager = ArticleManager(config_manager, get_independent_os_path(["data", "article.dat"]),get_independent_os_path(["data","blacklist.dat"]) ) #article database object
    config_manager.load_data(crawl_newspaper=False, crawl_kols=False, crawl_kols_by_smcc=False)
    data_manager.load_data()
    
    
    answer = 'y'
    while answer in ['y', 'Y']:
        print('Please input search string in format "a, b, c; x, y, z" to find all articles that contain ("a" or "b" or "c") and ("x" or "y" or "z") keywords: ')
        search_string = input("Search: ")
        article_list = data_manager.search_in_database(search_string, search_content=True)
        if article_list:
            print("There are %s results: " % len(article_list))
            for count, article in enumerate(sorted(article_list, key=lambda x: x.get_date()), 1):
                print(count, ". ", article.get_topic())
                print(article.get_href())
                print(get_date_string(article.get_date()))
                print()
        else:
            print("There are no result")
        answer = input("Do you want to search again (y/n) ?: ")
