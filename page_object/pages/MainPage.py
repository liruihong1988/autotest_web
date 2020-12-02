import time

from selenium.webdriver.common.by import By

from page_object.pages.BasePage import BasePage
from page_object.pages.SearchPage import SearchPage


class MainPage(BasePage):

    def open_baidu(self):
        self.open(self.url)
        return SearchPage(self.driver)

