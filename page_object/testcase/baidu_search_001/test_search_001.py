#-- coding:utf-8 --

import allure
from selenium.webdriver.common.by import By

from page_object.pages.BasePage import BasePage
from page_object.pages.MainPage import MainPage

@allure.feature('Test_Search_001')
class Test_Search_001(object):

    @allure.story('test_searchcase_001_001')
    def test_searchcase_001_001(self,driver):
        self.driver = driver
        self.main = MainPage(self.driver)
        self.main.open_baidu().search("selenium").hover_p()

        assert_text = BasePage(self.driver)
        text = (By.XPATH,"//*[contains(text(),'MeterSphere - 开源自动化测试平台')]")
        assert assert_text.isElementPresent(text) == True

    @allure.story('test_searchcase_001_002')
    def test_searchcase_001_002(self, driver):
        self.driver = driver
        self.main = MainPage(self.driver)
        self.main.open_baidu().search("python")

        assert_text = BasePage(self.driver)
        text = (By.XPATH, "//*[contains(text(),'PyCharm开发工具')]")
        assert assert_text.isElementPresent(text) == True

    @allure.story('test_searchcase_001_003')
    def test_searchcase_001_003(self, driver):
        self.driver = driver
        self.main = MainPage(self.driver)
        token = self.main.open_baidu().login()
        print("tokentoken:",token)
    #
    # def teardown(self):
    #     self.driver.close()
    #     self.driver.quit()