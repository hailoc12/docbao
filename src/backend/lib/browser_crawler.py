from selenium import webdriver
from selenium.webdriver.firefox.options import Options
from multiprocessing import Process
from pyvirtualdisplay import Display 
import random
import os
from time import sleep
import traceback 
import sys

def print_exception():
    # Print error message in try..exception
    exec_info = sys.exc_info()
    traceback.print_exception(*exec_info)


def get_independent_os_path(path_list):
    path = ""
    for item in path_list:
        path = os.path.join(path, item)
    return path

# firefox functions

def get_firefox_profile(profile_name):
    '''
    function: return profile if exists, else create new
    input
    -----
    profile_name (str): profile in name
    '''
    profile_path = get_independent_os_path(['profiles',profile_name])
    
    if os.path.isdir(profile_path):
        return webdriver.FirefoxProfile(profile_path)
    else:
        print("profile %s doesn't exist yet") 
        print("you need to create %s profile with setup_browser.py")
        print("you default profile in this session") 
        os.mkdir(profile_path)
        return None

 
class BrowserWrapper:
    # Wrap browser variable so it can be passed as reference variable
    _browser = None
    _profile = ''
    def set_browser(self, new_browser, profile):
        self._browser = new_browser
        self._profile = profile
    def get_browser(self):
        return self._browser
    def get_profile(self):
        return self._profile
    def quit(self):
        if self._browser is not None:
            self._browser.quit()

class BrowserCrawler:
    # Function: this class use Firefox browser to fetch all rendered html of a page
    _driver = None
    _has_error = False
    _quited = False
    _diplay = None
    def __init__(self, timeout=60, display_browser=False, fast_load=True, profile_name=None):
        '''
        input
        -----
        
        timeout: timeout to load page  
        display_browser: not run browser in headless mode 
        fast_load: use ads block plugins, turn off css to load page faster 
        profile (str): provide a profile name. Need to set up profile first 
        '''
        # Create a headless Firefox browser to crawl
        
        options = Options()
        if display_browser==False:
            options.add_argument("--headless")

        if profile_name is None or profile_name=="": 
            profile= webdriver.FirefoxProfile()
        else:
            profile= get_firefox_profile(profile_name)
            print("Firefox profile: %s" % profile_name)

        if fast_load==True:
            profile.set_preference('permissions.default.stylesheet', 2)
            # Disable images
            profile.set_preference('permissions.default.image', 2)
            # Disable notification
            profile.set_preference('permissions.default.desktop-notification', 2)
            # Disable Flash
            profile.set_preference('dom.ipc.plugins.enabled.libflashplayer.so', 'false')
            # Adblock Extension
            base_dir = os.environ['DOCBAO_BASE_DIR']
            profile.exp = get_independent_os_path([base_dir, 'src', 'backend', 'input', "adblock.xpi"])
            profile.add_extension(extension=profile.exp)

        self._driver = webdriver.Firefox(firefox_options=options, firefox_profile=profile)

        if os.environ['DOCBAO_RUN_ON_RASPBERRY']=='true':
            # Create a virtual screen to with Raspberry too
            self._display = Display(visible=0, size=(1024,768))
            self._display.start()

        self._driver.set_page_load_timeout(timeout)
        self._quited = False

    def load_page(self, url, prevent_auto_redirect=False, wait=5, entropy=3):
        # Function: load page with url
        # Input:
        # - wait: time waiting for page to load
        # - entropy: small random add to waiting time

        wait = int(wait + random.random() * entropy)
        # self._driver.set_page_load_timeout(wait) # Set timeout frequently may raise errors
        # self._driver.implicitly_wait(wait)

        self._has_error = False
        a= True
        #while a:
        try: 
            self._driver.get(url)
            if prevent_auto_redirect:
                sleep(3)
                print('reload url to prevent auto redirect')
                self._driver.get(url)
            a=False
            return True
        except:
            print_exception()
            print("Timeout")
            self._has_error = True
            return False
        
    def get_title(self):
        # Function: return page title
        return self._driver.title

    def get_page_html(self):
        # Return all html of an web 
        return self._driver.page_source

    def has_error(self):
        return self._has_error

    def has_quited(self):
        return self._quited

    def quit(self):
        self._driver.quit()
        self._quited = True


class NewspaperCrawler():
    # Function: this class crawl a website based on a config 
    _browser_crawler = None
    _web_config = None
    _has_error = False
    _timeout = 0
    _page_loaded = False

    def __init__(self, web_config, wait=5):
        # Create new instance of Firefox to crawl
        self._browser_crawler = BrowserCrawler()
        self._web_config = web_config
        self._timeout = wait

    def load_page_async(self, url):
        # Open url in Firefox to extract information
        self._has_error = False
        self._browser_crawler.load_page(url,self._timeout)

        if self._browser_crawler.has_error():
            print("In NewspaperCrawler-->Init: Can't load page: %s" % url)
            self._has_error = True
            self._page_loaded = False
            return False
        self._page_loaded = True
        return True
       
    def load_page(self, url, run_async=True):
        # Load page async
        self._page_loaded = False
        if run_async:
            procs = Process(target=self.load_page_async, args=(url,))
            procs.start()
        else:
            self.load_page_async(url)
            return self.has_page_loaded()

    def has_page_loaded(self):
        return self._page_loaded

    def get_start_url(self):
        return self._web_config.get_crawl_url()

    def get_title(self):
        return self._browser_crawler.get_title()

    def has_error(self):
        return self._has_error
    
    def quit(self):
        self._browser_crawler.quit()

    def has_quited(self):
        return self._browser_crawler.has_quited()
