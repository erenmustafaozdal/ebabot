from selenium import webdriver
from selenium.common.exceptions import NoSuchElementException
from selenium.common.exceptions import TimeoutException
from selenium.common.exceptions import StaleElementReferenceException
from selenium.webdriver.support.ui import WebDriverWait
import classes.log as log
import settings

chromedriver_path = settings.driver_path
web_headless = settings.web_headless
web_profile = settings.web_profile
web_implicitly_wait = settings.web_implicitly_wait
web_size = settings.web_size

class Browser(object):
    """docstring for Browser"""
    def __init__(self, user):
        super(Browser, self).__init__()
        self.options = webdriver.ChromeOptions()
        self.options.add_experimental_option("excludeSwitches", ["enable-logging"])
        self.options.headless = web_headless
        self.options.add_argument("user-data-dir={}\\{}".format(web_profile,user['name']))        
        self.__web = webdriver.Chrome(chromedriver_path, options=self.options)
        self.__web.implicitly_wait(web_implicitly_wait)

        if web_size == "max":
            self.__web.maximize_window()
        else:
            self.__web.set_window_size(web_size[0], web_size[1])

        log.write("Tarayıcı varsayılan ayarlarda açıldı.", "header")
        log.write("<blue>Gizli mi?:</> {}".format("Evet" if web_headless else "Hayır"))

    def get(self):
        return self.__web

    def wait(self, ec, seconds = 300, isNot = False):
        try:
            ignored_exceptions=(NoSuchElementException,StaleElementReferenceException,)
            wait = WebDriverWait(self.__web, seconds,ignored_exceptions=ignored_exceptions)
            if isNot:
                return wait.until_not(ec)
            return wait.until(ec)
        except TimeoutException:
            return False

    def element(self, xpath, multiple = False):
        try:
            if multiple == True:
                element = self.__web.find_elements_by_xpath(xpath)
            else:
                element = self.__web.find_element_by_xpath(xpath)
        except NoSuchElementException:
            return False
        return element

    def switchTab(self, tab):
        self.__web.switch_to.window(self.__web.window_handles[tab])



