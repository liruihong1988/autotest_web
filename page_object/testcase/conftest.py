import re
import time

import pytest

from page_object.config.readconfig import ReadConfig
from page_object.util.getversion import getVersion
from page_object.dbconnect.DbSqlUtil import DBSqlUtil

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

def pytest_sessionfinish(session):  #在测试执行完毕尚未返回exit code的时候进行剩余操作

    passed_amount = sum(1 for result in session.results.values() if result.passed)
    failed_amount = sum(1 for result in session.results.values() if result.failed)

    import time

    timetemp = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
    timeArray = time.strptime(timetemp, "%Y-%m-%d %H:%M:%S")
    detailedid = int(time.mktime(timeArray))

    util = DBSqlUtil('mysql')

    getcon = ReadConfig()

    project = getcon.get('DEFAULT',"PROJECTNAME")
    testtype = getcon.get('DEFAULT',"TESTTYPE")

    ver = getVersion()
    version = ver.getNowVersion(testtype, project)

    testTitle_list = []
    result_list = []
    global result_color_list
    result_color_list = []

    for i in session.markers:
        markers_list = str(session.markers[i])
        testTitle = re.findall(r"args=\('(.+?)',\)", markers_list)
        list2 = "".join(testTitle)
        testTitle_list.append(list2)

    # 插入测试结果表
    testTitle_list = []
    pytestname_list = []
    result_list = []
    featurename_list =[]

    for i in session.markers:
        markers_list = str(session.markers[i])
        testTitle = re.findall(r"args=\('(.+?)',\)", markers_list)
        testTitle_list.append(testTitle)

    for i in session.results:
        results_list = str(session.results[i])
        featurename = re.findall(r"TestReport '(.+?).py::", results_list)
        pytestname = re.findall(r"::.*::(.+?)' when", results_list)
        testresult = re.findall(r"outcome='(.+?)'>", results_list)
        testresult1 = str(testresult)

        if testresult1 == "['passed']":
            result = "1"
        else:
            result = "0"
        result_list.append(result)
        pytestname_list.append(pytestname)
        featurename_list.append(featurename)

    test_result_zip = zip(testTitle_list, pytestname_list, result_list,featurename_list)
    test_result_list = list(test_result_zip)

    for i in test_result_list:
        list_i = str(i)
        testTitle = re.findall(r"\(\['(.+?)'\], ", list_i)
        pytestname = re.findall(r"\], \['(.+?)'\], '", list_i)
        testresult = re.findall(r"\], '(.+?)', \[", list_i)
        featurename = re.findall(r"\', \['(.+?)'\]\)", list_i)

        util.mysql_execute_sql(
            "INSERT INTO pytest_ui_result(test_type,project,version,feature_name,testTitle,testTitlename,result,runtime,exceptionmessage,detailed_id)VALUE(%s,%s,%s,%s,%s,%s,%s,null,null,%s)",
            (testtype,project,version,featurename,testTitle, pytestname, testresult, detailedid))

        # 更新子表运行时间
        for n in session.runtime:
            listn = (n, session.runtime[n])
            listnn = str(listn)

            testTitlen = re.findall(r"Function (.+?)>", listnn)
            testresultn = re.findall(r", (.+?)\)", listnn)

            util.mysql_execute_sql(
                "UPDATE pytest_ui_result SET runtime = %s WHERE testTitlename = %s AND VERSION = %s and feature_name = %s and detailed_id =%s",
                (testresultn,testTitlen,version,featurename,detailedid))

        # 更新错误信息
        for j in session.exception:
            listj = (str(j), str(session.exception[j]))
            listjj = str(listj)
            print("listjjlistjjlistjjlistjj:", listjj)
            testTitlej = re.findall(r"Function (.+?)>", listjj)
            testresultj = re.findall(r" '.*", listjj)

            if testresultj == [" 'Null')"]:
                testresultj = 'null'
                util.mysql_execute_sql(
                    "UPDATE pytest_ui_result SET exceptionmessage = %s WHERE testTitlename = %s AND VERSION = %s and feature_name = %s and detailed_id =%s",
                    (testresultj, testTitlej, version,featurename,detailedid))
            else:
                util.mysql_execute_sql(
                    "UPDATE pytest_ui_result SET exceptionmessage = %s WHERE testTitlename = %s AND VERSION = %s and feature_name = %s and detailed_id =%s",
                    (testresultj, testTitlej, version, featurename,detailedid))

    #更新用例结果颜色
    for i in session.results:
        results_list = str(session.results[i])
        featurename = re.findall(r"TestReport '(.+?).py::", results_list)
        testresult = re.findall(r"outcome='(.+?)'>", results_list)
        testresult1 = str(testresult)
        testTitle_color = re.findall(r"::.*::(.+?)' when", results_list)

        if testresult1 == "['passed']":
            result = '通过'
            result_color = 'style=background-color:Lime'

        else:
            result = '不通过'
            result_color = 'style=background-color:red'

        util.mysql_execute_sql(
            "UPDATE pytest_ui_result SET result_name = %s WHERE testTitlename = %s AND VERSION = %s and feature_name = %s and detailed_id =%s",
            (result, testTitle_color, version,featurename,detailedid))
        util.mysql_execute_sql(
            "UPDATE pytest_ui_result SET result_color = %s WHERE testTitlename = %s AND VERSION = %s and feature_name = %s and detailed_id =%s",
            (result_color, testTitle_color, version,featurename,detailedid))
