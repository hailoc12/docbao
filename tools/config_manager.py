header = '''
###############################################################################
# program : config manager 
# function: help create, edit web configs easily for crawling 
# author  : hailoc12
# created : 2019-06-14
###############################################################################
'''
import copy
from os import system
import os
from src.backend.lib.config import ConfigManager, WebConfig
from src.backend.lib.utils import get_independent_os_path
from src.backend.lib.data import Article, ArticleManager
from src.backend.lib.browser_crawler import BrowserWrapper, BrowserCrawler

HELP_STRING = 'Type "help" for help, "quit" or "exit" to quit app'
MAX_DISPLAY = 10

mem_list = None # memorized list use for chaining commands 

# UTILITY

def display_multiple_input(message, answer_message="Input: "):
    answer = None
    print(message)
    count=0
    result = []
    while answer != '':
        count+=1
        answer = input(str(count) + '. ' + answer_message)
        if answer !='':
            result.append(answer)
    return result 

def display_choice_dialog(message, choices, answer_message="Your Answer: "):
    '''
    output
    ======
    None if cancel
    0..len(choices) if choice
    '''
    print(message)
    for i in range(0, len(choices)):
        print("%s. %s" % (str(i+1), choices[i]))
    choice = 'a'
    while not choice.isdigit():
        try:
            print()
            choice = input(answer_message)
            if choice.strip().isdigit():
                choice = int(choice)
                if choice <= 0 or choice > len(choices):
                    print("You must input a number between 1..%s" % str(len(choices)))
                    choice = 'a'
                return choice-1
            else:
                if choice.strip() == '':
                    return None
                else:
                    print("You must input a number between 1..%s" % str(len(choices)))
                    choice = 'a'
        except:
            print("You must input a number between 1..%s" % str(len(choices)))
            choice = 'a'

def extract_args(args):
    '''
    extract index or keyword from arguments

    arg:
    - args: list of arguments of command
    
    output: index (int) or keyword (str) or None if fail
    ''' 
    arg = " ".join(args).strip()
    try:
        index = int(arg) - 1 #index start from 0
        if mem_list is not None:
            if index >=0 and index < len(mem_list):
                return index
            else:
                print("Must provide an index between 1..%s" % str(len(mem_list)))
        else:
            print('There are no list to use index. Use command "show" to create list')
    except:
        keyword = arg 
        return keyword
    return None
     
def display_menu_dialog(menu_message,input_message, menu=[]):
    '''
    function
    --------
    display menu and get user choice 
    
    input
    -----
    menu: list of menu 

    output
    ------
    return user choice in number (0..len(menu)-1)
    '''
    print(menu_message)
    choice = display_choice_dialog(input_message, menu)
    return choice 

def clear_screen():
    system('clear')

def process_edit_config(webconfig):
    if webconfig is None:
        input("There isn't any web config yet. Create a new one or load from resources")
        return None

    print_config_header = '''
###########################################
#            PRINT WEB CONFIG             #
###########################################
'''
    while True: 
        clear_screen()
        print(print_config_header)
        config_list = webconfig.print_config()
        number_of_config = len(config_list) 
        choice = input("Press ENTER to return, LINE NUMBER <=%s to edit, -LINENUMBER <=%s to remove, or >%s to add new config: " % (number_of_config, number_of_config, number_of_config))

        is_digit = False
        try:
            line = int(choice)
            is_digit = True
        except:
            pass
        if is_digit:
            if line <= number_of_config: # edit config
                if line > 0: # edit old config
                    if line != 1:
                        key, value = webconfig.get_config_by_index(line-2)
                    else:
                        key = 'Webname'
                        value = webconfig.get_webname()
                    print()
                    print("Editing key: %s" % key)
                    print("Old value: %s" % str(value))

                    validated = False
                    while not validated:
                        try:
                            new_value = eval(input("New Value: ")) # note: eval is important here to get right data type
                            validated = True
                        except:
                            print("Input value in wrong format. Remember to input like Python code (eg. 'money' not money. [a, b, c] not '[a, b, c]'")

                    if line != 1:
                        webconfig.set_config(key, new_value)
                    else:
                        webconfig.set_webname(new_value)
                    input("Change OK. Press ENTER to continue")
                elif line < 0: # delete config
                    if line == -1: # delete webname
                        input("Sorry, you can't delete site name")
                    else:
                        key, value = webconfig.get_config_by_index(-line-2)
                        webconfig.delete_config(key)
                        input("Succesfully remove %s from site config" % key)
            else: # add new config
                key = input("Enter new config key: ")
                validated = False
                while not validated:
                    try:
                        value = eval(input("Enter config value: "))
                        validated = True
                    except:
                        print("Input value in wrong format. Remember to input like Python code (eg. 'money' not money. [a, b, c] not '[a, b, c]'")

                webconfig.set_config(key, value)
                input("Sucessfully add %s to config" % key)
        else:
            break
    return webconfig


def display_yes_no_dialog(message):
    choice = input(message)
    if 'y' == choice.lower().strip():
        return True
    elif 'n' == choice.lower().strip():
        return False
    else:
        return None

def process_create_blank_newspaper():
    webconfig = WebConfig()
    webconfig.load_default_config('newspaper')
    print()
    # basic config
    newspaper_name = input("Please enter newspaper name: ")
    newspaper_url  = input("Please enter newspaper base url: ")
    choice = display_yes_no_dialog("Is crawl url the same as base url (y/n) ?")
    if not choice:
        crawl_url = input("Please enter crawl url: ")
    else:
        crawl_url = newspaper_url
    
    use_browser = display_yes_no_dialog("Do you want to crawl using browser or not (y/n) ?")
    if use_browser:
        webconfig.set_config("use_browser", True)
    else:
        webconfig.set_config("use_browser", False)

    #date_xpath = input("Please enter xpath to get publish date in detail page: ")

    menu = ['Auto Find', 
            'Class name',
            'Xpath']

    date_extract_type = display_choice_dialog('Please choose one way to extract publish date in detail page: ', menu)

    if date_extract_type == 1: # CSS selection  
        css = input("Please enter class name of html tag that contain publish date: ")
        date_xpath = '//node()[@class="' + css + '"]'
    elif date_extract_type == 2:
        date_xpath = input("Please enter single xpath that extract html tag containing publish date: ")
    else: # Autofind. Not implement yet
        date_xpath = ''

    xpath_count = len(webconfig.get_topics_xpath())

    remove_date_tag_html = display_yes_no_dialog('Does it need to remove html tag to extract publish date (y/n)?: ')
    webconfig.set_config('remove_date_tag_html', remove_date_tag_html)

    ignore_topic_menu_choice = ['Topic is invalid', 'Use current time as publish date']
    choice = display_choice_dialog("How to treat topic that can't find its publish date ?", ignore_topic_menu_choice)
    if choice == 0: 
        ignore_topic_not_have_publish_date = True
    else: 
        ignore_topic_not_have_publish_date = False
    webconfig.set_config('ignore_topic_not_have_publish_date', ignore_topic_not_have_publish_date)

    crawl_detail_choice = display_yes_no_dialog('Do you want to crawl detail content (sapo, content, img) ?: ')

    if crawl_detail_choice:
        sapo_xpath = input("Please enter xpath to extract sapo text: ")
        
        content_xpath    = input("Please enter xpath to extract main content: ")

        remove_content_html = True

        remove_content_html_xpaths = []
        answer = None
        count = 1
        while answer != '':
            print("Please input xpaths to remove tags (ENTER=Finish): ")
            answer = input("Xpath %s: " % str(count))
            if answer != '':
                remove_content_html_xpaths.append(answer)
            count+=1
        
        feature_image_xpath = input("Please enter xpath to extract feature images url: ")

        text_xpath = display_multiple_input("Please input xpaths to get text element: ")
        image_box_xpath = display_multiple_input("Please input xpaths to get image box element: ")

        image_title_xpath = display_multiple_input("Please input xpaths to get title element from image box (ENTER=finish): ")
        video_box_xpath = display_multiple_input("Please input xpaths to get video box element (ENTER=Finish)")
        video_title_xpath = display_multiple_input("Please input xpaths to get title element from video box (ENTER=finish): ")
        audio_box_xpath = display_multiple_input("Please input xpaths to get audio box element (ENTER=Finish)")
        audio_title_xpath = display_multiple_input("Please input xpaths to get title element from audio box (ENTER=finish): ")

        avatar_choice_menu = ['Provide logo link', 'Xpath to get logo url']
        avatar_choice = display_choice_dialog("How do you want to extract logo url ?", avatar_choice_menu)
        avatar_url = ''
        avatar_xpath = ''

        if avatar_choice == 0: # provide linke
            avatar_type = 'url'
            avatar_url = input("Please enter logo absolute url: ")
        else:
            avatar_xpath = input("Please enter xpath to extract avatar/logo url: ")
            avatar_type = 'xpath'

        sapo_xpath_list = []
        content_xpath_list = []
        feature_image_xpath_list = []

        for i in range(0, xpath_count):
            sapo_xpath_list.append(sapo_xpath)
            content_xpath_list.append(content_xpath)
            feature_image_xpath_list.append(feature_image_xpath)

        webconfig.set_config('sapo_xpath', sapo_xpath_list)
        webconfig.set_config('content_xpath', content_xpath_list)
        webconfig.set_config('text_xpath', text_xpath)
        webconfig.set_config('feature_image_xpath', feature_image_xpath_list)
        webconfig.set_config('get_detail_content', crawl_detail_choice)
        webconfig.set_config('remove_content_html', remove_content_html)
        webconfig.set_config('remove_content_html_xpaths', remove_content_html_xpaths)

        webconfig.set_config('image_box_xpath', image_box_xpath)
        webconfig.set_config('image_title_xpath', image_title_xpath)

        webconfig.set_config('video_box_xpath', video_box_xpath)
        webconfig.set_config('video_title_xpath', video_title_xpath)

        webconfig.set_config('audio_box_xpath', audio_box_xpath)
        webconfig.set_config('audio_title_xpath', audio_title_xpath)

        webconfig.set_config('avatar_type', avatar_type)
        webconfig.set_config('avatar_xpath', avatar_xpath)
        webconfig.set_config('avatar_url', avatar_url)

    tags = display_multiple_input("Please input metadata to label article crawled from this config (ENTER=finish): ")
    domain_re = newspaper_url
    webconfig.set_webname(newspaper_name)
    webconfig.set_config('web_url', newspaper_url)
    webconfig.set_config('crawl_url', crawl_url)
    webconfig.set_config('url_pattern_re', domain_re)
    webconfig.set_tags(tags)
    date_xpath_list = []

    # use the same date_xpath for every topic_xpath
    for i in range(0, xpath_count):
        if date_xpath:
            date_xpath_list.append(date_xpath)
    webconfig.set_config('date_xpath', date_xpath_list) 
    # topic type
    choice = display_yes_no_dialog("Do you want to run test with default config (y/n) ?")
    if choice:
        webconfig = process_test_crawl_web_config(webconfig)
        is_ok = True
    input("Successfully createn %s site config" % webconfig.get_webname())
    return webconfig

def process_create_blank_web_config():
    clear_screen() 

    header = '''
##############################################
CREATE BLANK WEB CONFIG
##############################################
    '''

    print(header) 

    menu = ['Newspaper',
            'Wordpress Blog',
            'Facebook Account',
            'Facebook Page', 
            'Facebook Group',
            'Other']
    
    # choose template  
    user_choice = display_menu_dialog('What type of site: ', 'Choice: ', menu)
    webconfig = WebConfig()

    if user_choice == 0: # newspaper
        webconfig = process_create_blank_newspaper()
               
    elif user_choice == 1: # wordpress 
        webconfig.load_default_config('wordpress')
    elif user_choice == 2: # facebook user
        webconfig.load_default_config('facebook user')
        fb_name = input("Please input FB Account name: ")
        fb_username = input("Please input FB username (or ENTER to leave it): ")
        fb_userid   = input("Please input FB user ID (or ENTER to leave it): ")
        if fb_username.strip() != '':
            url = "https://www.facebook.com/" + fb_username.strip()
        else:
            url = "https://www.facebook.com/profile.php?id=" + fb_userid.strip()
        webconfig.set_webname(fb_name)
        webconfig.set_config('web_url', url) 
        webconfig.set_config('crawl_url',url)
        webconfig.set_config('url_pattern_re', url)

    elif user_choice == 3: # facebook fanpage
        webconfig.load_default_config('facebook fanpage')
        fb_name = input("Please input Fanpage name: ")
        fb_id = input("Please input Fanpage id: ")
        url = "https://www.facebook.com/pg/" + fb_id.strip() + "/posts/?ref=page_internal"
        webconfig.set_webname(fb_name)
        webconfig.set_config('web_url', url) 
        webconfig.set_config('crawl_url',url)
        webconfig.set_config('url_pattern_re', url)
    elif user_choice == 4: # facebook group
        webconfig.load_default_config('facebook fanpage')
        fb_name = input("Please input FB Group name (eg Page Hải Phòng): ")
        fb_id = input("Please input Group id (eg page.haiphong): ")
        url = "https://www.facebook.com/groups/" + fb_id.strip() + "/"
        webconfig.set_webname(fb_name)
        webconfig.set_config('web_url', url) 
        webconfig.set_config('crawl_url',url)
        webconfig.set_config('url_pattern_re', url)
    else: 
        webconfig.load_default_config()

    # what to do next  
    menu = ['Edit created config',
            'Test crawling this config',
            'Save config',
            "Return"]
    user_choice = -1  

    while user_choice != 3: # finish
        clear_screen()
        print(header)
        user_choice = display_menu_dialog('What do you want to do next ? ', 'Choice: ', menu)
        if user_choice == 0: # edit config  
            process_edit_config(webconfig)
        elif user_choice == 1: # test crawl  
            webconfig = process_test_crawl_web_config(webconfig)

        elif user_choice == 2: # save config 
            process_save_webconfig(webconfig)
    return webconfig
       
def process_test_crawl_web_config(webconfig):
    '''
    function
    --------
    try to crawl with webconfig only  

    return
    ------
    modified webconfig
    '''
    test_crawl_header = '''
###########################################
#        TEST CRAWLING SITE CONFIG        #
###########################################
    '''
    has_change_dir = False
    try:
        os.chdir("backend")
        has_change_dir = True
    except:
        pass

    continue_test = True
    while continue_test:
        clear_screen()
        print(test_crawl_header)

        # prepare webconfig for test  
        minimum_duration_old_value = webconfig.get_minimum_duration_between_crawls()
        webconfig.set_minimum_duration_between_crawls(-5) # mean always crawl this config
        maximum_url_old_value = webconfig.get_config('maximum_url', 10)
        webconfig.set_config('maximum_url',50) 

        # ask for edit 
        choice = display_yes_no_dialog("Is there anything to edit before test crawling (y/n) ?")
        if choice:
            webconfig = process_edit_config(webconfig)
            maximum_url_old_value = webconfig.get_maximum_url()

        # test
        config_manager = ConfigManager(get_independent_os_path(['src', 'backend','input', 'test.yaml']), get_independent_os_path(['input', 'kols_list.txt']), get_independent_os_path(['input', 'fb_list.txt']))
        config_manager.load_data()
        config_manager.replace_crawl_list([webconfig]) 
        data_filename = get_independent_os_path(['src', 'backend', 'data','test_article.dat'])
        blacklist_filename = get_independent_os_path(['src', 'backend','data','test_blacklist.dat'])

        data_manager = ArticleManager(config_manager, data_filename, blacklist_filename)
        data_manager.reset_data()

        # test crawl 
        my_pid = 1
        browser = BrowserWrapper()
        if webconfig.get_crawl_type() == 'newspaper':
            data_manager.add_articles_from_newspaper(my_pid, webconfig, browser)
        elif 'facebook' in webconfig.get_crawl_type():
            data_manager.add_articles_from_facebook(my_pid, webconfig, browser)

        # report 
        #

        continue_test = display_yes_no_dialog('Do you want to test again (y/n) ?: ')

        # return back
        webconfig.set_config('maximum_url', maximum_url_old_value)
        webconfig.set_minimum_duration_between_crawls(minimum_duration_old_value)

    if has_change_dir:
        os.chdir("..")

    return webconfig

def process_create_web_config_from_existing_one():
    '''
    return
    ------
    webconfig object that contain config load from file
    ''' 

    load_config_header = '''
###########################################
#            PRINT WEB CONFIG             #
###########################################
    '''

    load_config_menu = ['Load from local config files',
            'Load from online config database',
            'Return to main menu'
           ]

    choice = -1
    webconfig = None
    while choice != 2:
        clear_screen()
        print(load_config_header)
        choice = display_menu_dialog('What do you want to do ?', "Choice (ENTER=cancel): ", load_config_menu)
        if choice == 0: 
            # display config file list
            file_base_path = get_independent_os_path(['resources','configs', 'newspaper'])
            filepath = display_choose_file_dialog(file_base_path)
            if filepath is not None:
                webconfig = WebConfig()
                webconfig.load_config_from_file(filepath)
                input("Successfully load site config from %s" % filepath)
                
        elif choice == 1:
            pass
    return webconfig

def process_manage_other_config(config_manager): 
    '''
    return
    ------
    None
    ''' 

    manage_other_config_header = '''
###########################################
#  MANAGE PROPERTIES IN CONFIG.YAML FILE  #
###########################################
    '''
    while True:
        clear_screen()
        print(manage_other_config_header)
        config_list = config_manager.print_config()
        choice = input("Press ENTER to return or LINE NUMBER to edit: ")
        if choice.isdigit():
            index = int(choice) - 1
            key, value = config_list[index]
            print()
            print("Editing key: %s" % key)
            print("Old value: %s" % str(value))
            new_value = eval(input("New Value: "))
            config_manager.set_config(key, new_value)
            input("Change OK. Press ENTER to continue")
        else:
            break
    config_manager.save_data()
            

def display_choose_file_dialog(file_base_path):
    header = '''
###########################################
#           LOAD SITE CONFIG              #
###########################################
    '''
    ok = False
    while not ok:
        clear_screen()
        print(header)
        search = input("Enter keyword to find config file or ENTER to display all: ") 
        file_list = []
        for root,directory,files in os.walk(file_base_path):
            for item in files:
                if search in item: 
                    file_list.append(item)

        # choose file 
        config_file_index = display_menu_dialog('Which config do you want to load ?', 'Choice (ENTER=Cancel): ', file_list)
        if config_file_index is None: #cancel
            return None
        config_file_name = file_list[int(config_file_index)]
        # make filepath to load
        filepath = get_independent_os_path([file_base_path, config_file_name])
        answer = input("Are you sure to load site config from %s ? (ENTER=ok, anything=repeat)" % config_file_name)
        if answer.strip() == '':
            ok = True
    return filepath

def process_manage_crawl_list(config_manager):
    '''
    output
    ======
        - config_manager with modified data 
        - None or webconfig loaded from current crawl list 
    '''
    manage_crawl_list_header = '''
###########################################
#           MANAGE CRAWL LIST             #
###########################################
    '''
   
     # what to do next  
    menu = ['Add site config file to list',
            'Remove newspaper from list',
            'Edit site config in list',
            'Load site config in list to working config',
            'Edit config of all site in list',
            'Add working site config to list',
            'Load working site config from list',
            'Return', 
            ]
    user_choice = -1  
    webconfig = None

    while user_choice != len(menu)-1: # finish
        clear_screen()
        print(manage_crawl_list_header)
        newspaper_list = config_manager.print_crawl_list() # newspaper_list contain all crawl config. All edits will be made on newspaper_list then merge back into config_manager
        print() 
        user_choice = display_menu_dialog('What do you want to do next ? ', 'Choice: ', menu)
        if user_choice == 0: # add config file to list 
            filepath = display_choose_file_dialog(get_independent_os_path(['resources', 'configs', 'newspaper']))
            if filepath is not None:
                new_webconfig = WebConfig()
                new_webconfig.load_config_from_file(filepath)
                newspaper_list.append(new_webconfig)
                input("Successfully add %s to crawl list" % new_webconfig.get_webname())
                config_manager.replace_crawl_list(newspaper_list) #save all changes to config_manager
                config_manager.save_data()

        elif user_choice == 1: # remove newspaper from list
            choice = input("Please input LINE NUMBER to remove or ENTER to cancel: ")
            if choice.strip() != '' and choice.isdigit():
                remove_webconfig = newspaper_list.pop(int(choice) -1)
                input("Successfuly remove %s from crawl list" % remove_webconfig.get_webname())
                config_manager.replace_crawl_list(newspaper_list) #save all changes to config_manager
                config_manager.save_data()

        elif user_choice == 2: # edit site config in list
            choice = input("Please input LINE NUMBER to edit or ENTER to cancel: ")
            if choice.strip() != '' and choice.isdigit():
                choose_webconfig = newspaper_list[int(choice) -1]
                choose_webconfig = process_edit_config(choose_webconfig) 
                config_manager.add_newspaper(choose_webconfig) # update config 
                config_manager.save_data()

        elif user_choice == 3: # load site config to working config
            choice = input("Please input LINE NUMBER to load or ENTER to cancel: ")
            if choice.strip() != '' and choice.isdigit():
                choose_webconfig = newspaper_list[int(choice) -1]
                webconfig = choose_webconfig
                input("Successfuly load %s config to working config" % choose_webconfig.get_webname())

        elif user_choice == 4: # edit single config of all sites in list
                print()
                newspaper_list = config_manager.get_newspaper_list()
                if len(newspaper_list) > 0:
                    print("Sample of a site config:")
                    sample_site = newspaper_list[0]
                    sample_site.print_config()
                    print()

                    key = input('Enter config property to edit: (ENTER=cancel, -config_name=remove)').strip()
                    key = key.strip()
                    if key != '':
                        if key[0] == '-': # remove config
                            key = key[1:]
                            count = 0 
                            for newspaper in config_manager.get_newspaper_list():
                                count+=1
                                newspaper.delete_config(key)
                            input("Successfully remove %s of %s site" % (key, str(count)))
                            config_manager.save_data()

                        else: # edit all
                            new_value = eval(input('Enter new value of %s: ' % key))
                            count = 0
                            for newspaper in config_manager.get_newspaper_list():
                                count+=1
                                newspaper.set_config(key, new_value)
                            input("Successfully change %s of %s site to new value" % (key, str(count)))
                            config_manager.save_data()
                else:
                    print("There haven't been any site config in crawling list")
                
        elif user_choice == 5: # add working site config to list
            if webconfig is not None:
                config_manager.add_newspaper(webconfig)
                input("Succesfully add %s to crawl list" % webconfig.get_webname())
                config_manager.save_data()
            else:
                input("No working site config. Please go to site config manager to create/load one")

        elif user_choice == 6: # load newspaper to current webconfig 
            choice = input("Please input LINE NUMBER to load or ENTER to cancel: ")
            if choice.strip() != '' and choice.isdigit():
                webconfig = copy.copy(newspaper_list[int(choice) -1])
                input("Successfuly load %s from crawl list" % webconfig.get_webname())
    return webconfig
 

def process_manage_config(webconfig=None, config_manager=None): 
    '''
    return
    ------
    None or webconfig loaded from crawling list 
    ''' 

    manage_config_header = '''
###########################################
#         MANAGE CONFIG.YAML FILE         #
###########################################
    '''

    manage_config_menu = [
                          'Edit crawl list',
            'Edit program settings',
            'Go to site config manager',
            'Return to main menu'
           ]

    choice = -1
    while choice != len(manage_config_menu) -1:
        clear_screen()
        print(manage_config_header)
        choice = display_menu_dialog('What do you want to do ?', "Choice: ", manage_config_menu)
        if choice == 0: # manage crawl list
           load_web_config = process_manage_crawl_list(config_manager)
           if load_web_config is not None:
               webconfig = load_web_config
        elif choice == 1: # manage other config  
            process_manage_other_config(config_manager)
        elif choice == 2: # go to site config manager
            process_webconfig_manager(webconfig, config_manager)

    return webconfig
 
def process_save_webconfig(webconfig):
    menu = ['Save in a new file',
            'Update an existing file']
    choice = display_choice_dialog('How do you want to save: ', menu)

    file_base_path = get_independent_os_path(['resources','configs','newspaper'])

    if choice == 0:
        print("Working config will be saved in ./resource/config/newspaper/")
        filename = input("Filename: ")
        filepath = get_independent_os_path([file_base_path, filename]) 
    elif choice == 1: #update existing file
        filepath = display_choose_file_dialog(file_base_path)

    webconfig.export(filepath)
    print("File is save OK") 

def process_webconfig_manager(webconfig=None, config_manager=None):
    '''
    return
    ------
    None
    ''' 

    webconfig_header = '''
###########################################
#           SITE CONFIG MANAGER           #
###########################################
    '''

    manage_webconfig_menu = ['Create new blank config',
                          'Load config from file',
            'Edit working site config',
            'Save working site config to file',
            'Test crawling working site config',
            'Add/Update working site config to crawl list',
            'Move to program setting',
            'Return to main menu'
           ]

    choice = -1
    while choice != len(manage_webconfig_menu) -1 :
        clear_screen()
        print(webconfig_header)
        choice = display_menu_dialog('What do you want to do ?', "Choice: ", manage_webconfig_menu)
        if choice == 0: # add current webconfig to crawl list
            webconfig = process_create_blank_web_config()
        if choice == 1: # create webconfig from existing one
            webconfig = process_create_web_config_from_existing_one()
        elif choice == 2: # editing working webconfig 
            webconfig = process_edit_config(webconfig)  
        elif choice == 3: # save working site config to file
            process_save_webconfig(webconfig) 
        elif choice == 4: # test crawling 
            process_test_crawl_web_config(webconfig)
        elif choice == 5: # add/update working site config to crawl list
            config_manager.add_newspaper(webconfig)
            config_manager.save_data() 
            print("Successfully add/update %s to crawl list" % webconfig.get_webname())
            
        elif choice == 6: # move to program setting
            process_manage_config(webconfig, config_manager)
    return webconfig

# MAIN PROGRAM
config_manager = ConfigManager(get_independent_os_path(['src', 'backend', 'input', 'config.yaml']),
                              get_independent_os_path(['src, ','backend', 'input', 'kols_list.txt']), 
                              get_independent_os_path(['src', 'backend', 'input', 'fb_list.txt'])) #config object
config_manager.load_data(True, False, False, 30, '.')

main_menu_choice = -1 
while main_menu_choice != 2:
    clear_screen()
    print(header)

    main_menu = ['Manage site config', 
                 'Manage program settings',
                 'Quit']

    main_menu_choice = display_menu_dialog('WELCOME TO CONFIG MANAGER', 'Your choice: ', main_menu)
    webconfig = None
    if main_menu_choice == 0: # crawl new site
        webconfig  = process_webconfig_manager(webconfig, config_manager)
    elif main_menu_choice == 1: # manage config.yaml
        webconfig = process_manage_config(webconfig, config_manager)

print("Goodbye")  
