import os
import sys

import cx_Oracle
import pymysql
import logging
from page_object.dbconnect.r_db import ReadDbConfig
from page_object.util.logger import log

class DBSqlUtil(object):

    def __init__(self,dbtype):
        read = ReadDbConfig()
        db_m = read.readdb(dbtype)

        self.dbtype = dbtype
        # self.dbname = dbname
        self.host = db_m[0]
        self.username = db_m[1]
        self.password = db_m[2]
        self.database = db_m[3]

    def connect_db(self):
        if self.dbtype == 'mysql':
            try:
                self.db = pymysql.connect(self.host, self.username, self.password, self.database)
            except:
                log.error("connectDatabase failed")

        elif self.dbtype == 'oracle':
            try:
                self.db = cx_Oracle.connect(self.username, self.password, self.host + "/CBSS",
                                                encoding="UTF-8")
            except:
                log.error("connectDatabase failed")
        else:
            print("出错了")

    def get_cursor(self):
        self.cursor = self.db.cursor()
        return self.cursor

    def close_db(self):
        self.cursor.close()
        self.db.close()

    def mysql_select_one(self,sql,*value):
        self.connect_db()
        try:
            cursor = self.get_cursor()
            cursor.execute(sql,*value)
            result = cursor.fetchone()[0]
        except:
            log.error("select failed:" + sql)
            log.error("param:" + str(*value))
        self.db.commit()
        self.close_db()
        log.info("操作成功，执行语句为" + sql + " " +"参数值为:" + str(*value))
        log.info("查询成功，结果为:" + str(result))
        return result

    def mysql_select_list(self,sql,*value):
        self.connect_db()
        try:
            cursor = self.get_cursor()
            cursor.execute(sql, *value)
            result = cursor.fetchall()
        except:
            log.error("select failed:" + sql)
            log.error("param:" + str(*value))
        self.db.commit()
        self.close_db()
        log.info("操作成功，执行语句为" + sql + " " +"参数值为:" + str(*value))
        log.info("查询成功，结果为:" + str(result))
        return result

    def mysql_execute_sql(self,sql,*value):
        self.connect_db()
        try:
            n = self.get_cursor().execute(sql, *value)
        except:
            log.error("execute failed:" + sql)
            log.error("param:" + str(*value))
        self.db.commit()
        self.close_db()
        log.info("操作成功，执行语句为" + sql + str(*value))
        return n

    def oracle_select_one(self,sql,params={}):
        self.connect_db()
        try:
            cursor = self.get_cursor()
            cursor.execute(sql,params)
            result = cursor.fetchone()
        except:
            log.error("select failed:" + sql)
            log.error("param:" + str(params))
        self.db.commit()
        self.close_db()
        log.info("操作成功，执行语句为" + sql + " " +"参数值为:" + str(params))
        log.info("查询成功，结果为:" + str(result))
        return result

    def oracle_select_list(self,sql,params={}):
        self.connect_db()
        try:
            cursor = self.get_cursor()
            cursor.execute(sql, params)
            result = cursor.fetchall()
        except:
            log.error("select failed:" + sql)
            log.error("param:" + str(params))
        self.db.commit()
        self.close_db()
        log.info("操作成功，执行语句为" + sql + " " +"参数值为:" + str(params))
        log.info("查询成功，结果为:" + str(result))
        return result

    def oracle_execute_sql(self,sql,params={}):
        self.connect_db()
        try:
            n = self.get_cursor().execute(sql, params)
        except:
            log.error("execute failed:" + sql)
            log.error("param:" + str(params))
        self.db.commit()
        self.close_db()
        log.info("操作成功，执行语句为" + sql + str(params))
        return n

if __name__ == '__main__':
    pass