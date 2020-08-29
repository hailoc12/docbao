from lib import *

if __name__ == "__main__":
    config_manager = ConfigManager(get_independent_os_path(['input', 'config.yaml']),
                                            get_independent_os_path(['input', 'kols_list.txt']),
                                            get_independent_os_path(['input', 'fb_list.txt'])) #config object
    data_manager = ArticleManager(config_manager, get_independent_os_path(["data", "article.dat"]),get_independent_os_path(["data","blacklist.dat"]) ) #article database object
    data_manager.load_data()
 
    count = 0
    for href in data_manager._data:
        count+=1
        if count == 14:
            article = data_manager._data[href]
            print(article.get_topic())
            wp = Wordpress()
            post_id = wp.add_new_article(article)
            print("Successfully add wordpress post with id: %s" % str(post_id))
            print("Update its sentimentality to neutral")
            sleep(10)

            if wp.update_post_sentimentality(post_id, "neutral"):
                print("Successfully update post %s sentimentality to neutral" % post_id)
            else:
                print("Update error")

            break


