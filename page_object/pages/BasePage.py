import os
import sys
import time

from selenium.webdriver.common.action_chains import ActionChains
import requests
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.webdriver import WebDriver
from selenium.webdriver.support.wait import WebDriverWait
from page_object.config.readconfig import ReadConfig
from page_object.dbconnect.DbSqlUtil import DBSqlUtil
from page_object.util.logger import log

class BasePage(object):

    getcon = ReadConfig()
    url = getcon.get('URL','URL')

    def __init__(self,driver):
        self.driver:WebDriver = driver
        self.driver.implicitly_wait(10)

    def target_page(self):
        return self.driver.current_url == self.url

    def _open(self,url):
        self.url = url
        self.driver.get(url)

    def open(self,url):
        self._open(url)

    def wait_elevisible(self,loc):
        try:
            start = time.time()
            WebDriverWait(self.driver, 20, 0.5).until(EC.visibility_of_element_located(loc))
            end = time.time()
            log.info("{0}出现,等待时间{1}s".format(loc,round(end - start, 2)))
        except:
            log.error("未能等待元素出现。")
        return self

    def find_element(self,*loc):
        return self.driver.find_element(*loc)

    def click(self,loc):          #点击操作
        self.wait_elevisible(loc)
        try:
            log.info("点击:{0}".format(loc))
            self.find_element(*loc).click()
        except:
            log.error("{0}点击失败".format(loc))
        return self

    def double_click(self,loc):     #双击操作
        self.wait_elevisible(loc)
        try:
            log.info("双击:{0}".format(loc))
            ActionChains(self.driver).double_click(self.find_element(*loc)).perform()
        except:
            log.error("{0}双击失败".format(loc))
        return self

    def context_click(self,loc):        #右键操作
        self.wait_elevisible(loc)
        try:
            log.info("右击:{0}".format(loc))
            ActionChains(self.driver).context_click(self.find_element(*loc))
        except:
            log.error("{0}右击失败".format(loc))
        return self

    def send_keys(self,loc,text):       #输入操作
        self.wait_elevisible(loc)
        try:
            log.info("在:{0}中输入:{1}".format(loc,text))
            self.find_element(*loc).clear()
            self.find_element(*loc).send_keys(text)
        except:
            log.error("输入操作失败")
        return self

    def hover_element(self,loc):        #鼠标悬浮
        self.wait_elevisible(loc)
        try:
            log.info("鼠标悬停在:{0}之上".format(loc))
            ActionChains(self.driver).move_to_element(self.find_element(*loc)).perform()
        except:
            log.error("鼠标悬停操作失败")
        return self

    def get_text(self,loc):     #获取元素文本
        self.wait_elevisible(loc)
        try:
            log.info("获取元素:{0}的文本内容".format(loc))
            text = self.find_element(*loc).text
        except:
            log.error("获取元素:{0}的文本内容失败".format(loc))
        return text

    def window_handles(self):   #切换窗口
        try:
            log.info("切换窗口")
            windows = self.driver.window_handles
            self.driver.switch_to.window(windows[-1])
        except:
            log.error("切换窗口失败")
        return self

    def swipe_button(self,loc):   #滑动到元素
        try:
            log.info("滑动到元素{0}".format(loc))
            target = self.driver.find_element(*loc)
            self.driver.execute_script("arguments[0].scrollIntoView();", target)
            time.sleep(2)
        except:
            log.error("滑动到元素{0}失败".format(loc))
        return self

    def switch_iframe(self,value,type="id"):
        try:
            log.info("切换iframe:{0}".format(value))
            if type == "id":
                self.driver.switch_to_frame(value)
            elif type == "name":
                self.driver.switch_to_frame(value)
            elif type == "xpath":
                self.driver.switch_to_frame(self.driver.find_element_by_xpath(value))
        except:
            log.info("切换iframe:{0}失败".format(value))
        return self

    def isElementPresent(self,loc):   #判断元素是否存在
        try:
            element = self.driver.find_element(*loc)
        except:
            log.error("元素{0}不存在".format(loc))
            return False
        else:
            log.info("元素{0}存在".format(loc))
            return True

    def callApi(self,url):     #调用第三方http接口
        geturl = url
        response = requests.get(geturl)
        responsebody = response.text
        return responsebody