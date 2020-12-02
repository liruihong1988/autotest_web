import os
import time

import allure
import pytest
from airtest_selenium import WebChrome
from airtest_selenium.proxy import WebFirefox
from selenium import webdriver
from page_object.config.readconfig import ReadConfig

getcon = ReadConfig()
config_driver = getcon.get('WEBDRIVER',"driver")
config_remote = getcon.get('WEBDRIVER',"remote_url")

@pytest.fixture(scope='function')
def driver():
    global driver
    if config_driver == 'localchrome':
        driver = WebChrome()
    elif config_driver == 'localfirefox':
        driver = WebFirefox()
    elif config_driver == 'remotechrome':
        chrome_options = webdriver.ChromeOptions()
        driver = webdriver.Remote(command_executor=config_remote,desired_capabilities=chrome_options.to_capabilities())
    elif config_driver == 'remotefirefox':
        firefox_options = webdriver.FirefoxOptions()
        driver = webdriver.Remote(command_executor=config_remote,desired_capabilities=firefox_options.to_capabilities())
    driver.maximize_window()
    # yield (driver)
    return driver

def pytest_sessionstart(session):    #在测试session生成但尚未进入测试用例收集和执行的的时候记录一下测试套的开始时间
    global start_time
    start_time = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
    session.results = dict()         #dict()创建字典
    session.exception = dict()
    session.runtime = dict()
    session.markers = dict()

@pytest.hookimpl(tryfirst=True, hookwrapper=True)
def pytest_runtest_makereport(item, call):       #在测试执行时，每个测试用例（test_）执行，都会调用这个钩子方法

    outcome = yield
    result = outcome.get_result()

    if result.when == 'call':
        if result.longrepr != None:
            item.session.exception[item] = result.longrepr.reprcrash.message
        else:
            item.session.exception[item] = 'Null'
        item.session.results[item] = result                #把测试结果保存到session.results字典中
        item.session.runtime[item] = result.duration       #把测试执行时间保存到session.runtime字典中
        item.session.markers[item] = item.own_markers      #把测试用例的中文标题保存到session.markers字典中

    def adb_screen_shot(test_name):      #airtest截图方法
        timetemp = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
        timeArray = time.strptime(timetemp, "%Y-%m-%d %H:%M:%S")
        detailedid = int(time.mktime(timeArray))

        BASE_DIR = os.path.dirname(os.path.dirname(os.path.dirname(__file__)))
        dir = os.path.join(BASE_DIR, "screenshots\\")

        pic_path = dir + test_name  + "." + str(detailedid) + ".png"
        if config_driver == 'localchrome':
            driver.screenshot(pic_path)
        else:
            driver.get_screenshot_as_file(pic_path)
        return pic_path

    if result.when == 'call':  #判断测试用例执行失败时，调用截图方法进行截图，并把图片通过allure.attach.file方法与指定的测试用例进行关联
        if result.passed:   #True真则返回
            return
        if result.failed:   #False假则截图
            pic_path = adb_screen_shot(result.head_line)
            allure.attach.file(pic_path, "失败截图", attachment_type=allure.attachment_type.JPG)