from selenium import webdriver
from selenium.webdriver.firefox.options import Options
from multiprocessing import Process
from pyvirtualdisplay import Display 
import random

class BrowserWrapper:
    # Wrap browser variable so it can be passed as reference variable
    _browser = None
    def set_browser(self, new_browser):
        self._browser = new_browser
    def get_browser(self):
        return self._browser
    def quit(self):
        if self._browser is not None:
            self._browser.quit()

class BrowserCrawler:
    # Function: this class use Firefox browser to fetch all rendered html of a page
    _driver = None
    _has_error = False
    _quited = False
    _diplay = None
    def __init__(self, timeout=30, display_browser=False, fast_load=True):
        # Create a headless Firefox browser to crawl
        options = Options()
        if display_browser==False:
            options.add_argument("--headless")

        profile=webdriver.FirefoxProfile()
        if fast_load==True:
            profile.set_preference('permissions.default.stylesheet', 2)
            # Disable images
            profile.set_preference('permissions.default.image', 2)
            # Disable notification
            profile.set_preference('permissions.default.desktop-notification', 2)
            # Disable Flash
            profile.set_preference('dom.ipc.plugins.enabled.libflashplayer.so', 'false')
            # Adblock Extension
            profile.exp = "input/adblock.xpi"
            profile.add_extension(extension=profile.exp)

        self._driver = webdriver.Firefox(firefox_options=options, firefox_profile=profile)

        # Create a virtual screen to with Raspberry too
        #self._display = Display(visible=0, size=(1024,768))
        #self._display.start()
        #self._driver = webdriver.Firefox()

        self._driver.set_page_load_timeout(timeout)
        self._quited = False

    def load_page(self, url, wait=5, entropy=3):
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
            a=False
            return True
        except:
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
