import pymysql

from page_object.config.readconfig import ReadConfig
from page_object.dbconnect.DbSqlUtil import DBSqlUtil
from page_object.dbconnect.r_db import ReadDbConfig


class InitDatabase(object):

    def initDb(self):
        read = ReadDbConfig()
        db_m = read.readdb("mysql")
        self.dbtype = "mysql"
        self.host = db_m[0]
        self.username = db_m[1]
        self.password = db_m[2]
        self.database = db_m[3]

        mydb = pymysql.connect(host=self.host,user=self.username,passwd=self.password)
        mycursor = mydb.cursor()
        c_db = "CREATE DATABASE /*!32312 IF NOT EXISTS*/`"+self.database+"`/*!40100 DEFAULT CHARACTER SET utf8 */;"
        mycursor.execute(c_db)
        mydb_table = pymysql.connect(host=self.host, user=self.username, passwd=self.password,database=self.database)
        mycursor_table = mydb_table.cursor()
        pytest_ui_result = """
            CREATE TABLE `pytest_ui_result` (
                  `id` int(10) NOT NULL AUTO_INCREMENT,
                  `test_type` varchar(20) DEFAULT NULL,
                  `project` varchar(20) DEFAULT NULL,
                  `version` varchar(50) DEFAULT NULL,
                  `feature_name` varchar(100) DEFAULT NULL,
                  `testTitle` varchar(100) DEFAULT NULL,
                  `testTitlename` varchar(100) DEFAULT NULL,
                  `result` varchar(20) DEFAULT NULL,
                  `runtime` varchar(20) DEFAULT NULL,
                  `exceptionmessage` mediumtext,
                  `detailed_id` varchar(50) DEFAULT NULL,
                  `result_name` varchar(50) DEFAULT NULL,
                  `result_color` varchar(50) DEFAULT NULL,
                  PRIMARY KEY (`id`)
                ) ENGINE=InnoDB AUTO_INCREMENT=1069 DEFAULT CHARSET=utf8;
        """
        proj_verion_config = """
            CREATE TABLE `proj_verion_config` (
                  `id` INT(10) NOT NULL AUTO_INCREMENT,
                  `type` VARCHAR(50) DEFAULT NULL,
                  `version` VARCHAR(50) DEFAULT NULL,
                  `project` VARCHAR(50) DEFAULT NULL,
                  `name` VARCHAR(50) DEFAULT NULL,
                  `createtime` DATE DEFAULT NULL,
                  KEY `id` (`id`)
                ) ENGINE=INNODB AUTO_INCREMENT=13 DEFAULT CHARSET=utf8;
        """
        getcon = ReadConfig()
        testtype = getcon.get('DEFAULT', 'TEST_TYPE')
        project = getcon.get('DEFAULT', 'PROJECT_NAME')
        in_version_config = "INSERT  INTO `proj_verion_config`(`type`,`version`,`project`,`name`,`createtime`) VALUES ('" + testtype + "','v2020.1028.0002','" + project + "',NULL,'2020-08-12')"
        mycursor_table.execute(pytest_ui_result)
        mycursor_table.execute(proj_verion_config)
        mycursor_table.execute(in_version_config)
        mydb_table.commit()
        mydb_table.close()

if __name__ == '__main__':
    db = InitDatabase()
    db.initDb()