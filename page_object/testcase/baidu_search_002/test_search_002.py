#-- coding:utf-8 --

import allure
from selenium.webdriver.common.by import By

from page_object.pages.BasePage import BasePage
from page_object.pages.MainPage import MainPage

@allure.feature('Test_Search_002')
class Test_Search_002(object):

    @allure.story('test_searchcase_002_001')
    def test_searchcase_002_001(self,driver):
        self.driver = driver
        self.main = MainPage(self.driver)
        self.main.open_baidu().search("pytest")

        assert_text = BasePage(self.driver)
        text = (By.XPATH,"//*[contains(text(),'Web开发服务应用软件')]")
        assert assert_text.isElementPresent(text) == True

    @allure.story('test_searchcase_002_002')
    def test_searchcase_002_002(self, driver):
        self.driver = driver
        self.main = MainPage(self.driver)
        self.main.open_baidu().search("自动化测试")

        assert_text = BasePage(self.driver)
        text = (By.XPATH, "//*[contains(text(),'自动化测试需要学什么')]")
        assert assert_text.isElementPresent(text) == True

    def teardown(self):
        self.driver.close()
        self.driver.quit()