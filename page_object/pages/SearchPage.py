#-- coding:utf-8 --
import time

from selenium.webdriver import ActionChains
from selenium.webdriver.common.by import By
from page_object.pages.BasePage import BasePage

class SearchPage(BasePage):

    def search(self,text):
        kw = (By.ID,"kw")
        su = (By.ID,"su")

        self.send_keys(kw,text)
        self.click(su)
        time.sleep(3)
        return self

    def hover_p(self):
        tj_settingicon = (By.XPATH,"//*[@id='u']//*[@name='tj_settingicon']")

        self.hover_element(tj_settingicon)
        time.sleep(2)
        self.context_click(tj_settingicon)
        return self

    def login(self):
        userNameInput = (By.ID,"userNameInput")
        passwordInput = (By.ID,"passwordInput")
        submitButton = (By.ID,"submitButton")

        self.send_keys(userNameInput,"0010437")
        self.send_keys(passwordInput,"wxj@2016")
        self.click(submitButton)
        time.sleep(5)

        text = self.driver.page_source
        cookie = self.driver.get_cookies()
        print("cookiecookie:",cookie)
        return self