#-- coding:utf-8 --
import re
import shutil
from multiprocessing import Process, Pool, Queue, Manager
from os.path import abspath

import pytest
from airtest.core.api import *

from page_object.config.readconfig import ReadConfig

BASE_DIR = os.path.dirname(os.path.dirname(os.path.dirname(__file__)))
import sys
sys.path.extend([BASE_DIR])
from page_object.util.getversion import getVersion

from page_object.dbconnect.DbSqlUtil import DBSqlUtil
from page_object.util.httpreport import htmlreport
import configparser

def get_all_testfiles(dir):
    files_ = []
    list_ = os.listdir(dir)
    for i in range(0, len(list_)):
        path = os.path.join(dir, list_[i])
        if os.path.isdir(path):
            files_.extend(get_all_testfiles(path))
        if os.path.isfile(path):
            files_.append(path)

    file_list = []
    for i in files_:
        if os.path.basename(i)[0:5] == 'test_' and os.path.basename(i)[-3:] == '.py':
            file_list.append(i)
    return file_list

def get_pyfile():
    cmd = "pytest --collect-only -qq > all_testcase.txt"
    os.system(cmd)
    testcase_list = []
    f = open('all_testcase.txt', 'r')
    for lines in f:
        ls = lines.strip('\n').replace(' ', '').split('\n')
        for i in ls:
            print(str(i))
            if len(i) == 0:
                break
            i_py_a = i[0:i.rfind(":")]
            print(i_py_a)
            testcase_list.append(str(os.getcwd()) + '\\' + str(i_py_a))
    f.close()
    return testcase_list

def get_testcase():
    cmd = "pytest --collect-only -q > all_testcase.txt"
    os.system(cmd)
    testcase_list = []
    f = open('all_testcase.txt', 'r')
    for lines in f:
        ls = lines.strip('\n').replace(' ', '').split('\n')
        for i in ls:
            if len(i) == 0 or 'no' in i:
                break
            testcase_list.append(str(os.getcwd()) + '\\' + str(i))
    f.close()
    return testcase_list

def executiveTest(que):

    while 1==1:   #死循环，执行队列任务，队列为空时退出循环
        if que.qsize() != 0:
            case_path = que.get()
            print("case_pathcase_path",case_path)
            REPORTS_DIR = os.path.dirname(os.path.dirname(__file__))
            reports_dir = os.path.join(REPORTS_DIR, "reports")
            pytest.main(["-s", case_path,"--alluredir",reports_dir])
        else:
            break

if __name__ == '__main__':

    getcon = ReadConfig()
    project = getcon.get('DEFAULT', "PROJECTNAME")
    testtype = getcon.get('DEFAULT', "TESTTYPE")
    runmode = getcon.get('OPRATIONMODE', "RUNMODE")
    ver = getVersion()
    version = ver.getNewVersion(testtype, project)
    start_time = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())

    #获取所有的待测试文件
    if runmode == 'PYFILE':
        testcase_list = get_pyfile()
    else:
        testcase_list = get_testcase()
    testcsae_num = len(testcase_list)

    #把待测试文件放入que
    que = Manager().Queue(testcsae_num +1)  # 可用
    for i in testcase_list:
        que.put(i)

    #启动多进程执行任务
    num = testcsae_num
    i = 0
    pool = Pool(processes=num)
    while i < num:

        pool.apply_async(executiveTest, (que,))
        i = i + 1

    pool.close()
    pool.join()

    end_time = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())

    util = DBSqlUtil('mysql')

    #获取测试结果数据，生成html-report
    testcase_number = util.mysql_select_one("SELECT COUNT(*) FROM pytest_ui_result WHERE VERSION = %s",(version))
    passed_amount = util.mysql_select_one("SELECT COUNT(*) FROM pytest_ui_result WHERE VERSION = %s and result = '1'",(version))
    failed_amount = util.mysql_select_one("SELECT COUNT(*) FROM pytest_ui_result WHERE VERSION = %s and result = '0'",(version))

    html = htmlreport()
    html.report(start_time, end_time, testcase_number, passed_amount, failed_amount, version)

    ALLURE_DIR = os.path.dirname(os.path.dirname(__file__))
    allure_dir = os.path.join(ALLURE_DIR, "allure-report")
    reports_dir = os.path.join(ALLURE_DIR, "reports")

    # 生成allure-report
    cmd = "allure generate" + " " + reports_dir + " " + "-o" + " " + allure_dir + " " + "--clean"
    os.system(cmd)