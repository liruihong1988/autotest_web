import datetime
import re
from page_object.dbconnect.DbSqlUtil import DBSqlUtil

class getVersion(object):

    util = DBSqlUtil('mysql')

    def getNewVersion(self,type,project):


        data = self.util.mysql_select_one("SELECT version FROM proj_verion_config WHERE type = %s AND project= %s",(type,project))

        currentversion = data

        y = re.findall(r"v(.+?)\.", currentversion)
        m = re.findall(r"\.(.+?)\.", currentversion)
        c = currentversion[-4:]
        year = y[0]
        month = m[0]
        count = c

        nowyear = datetime.datetime.now().year
        d = datetime.date.today()
        nowmonth = '%02d' % d.month
        nowday = datetime.datetime.now().day
        if int(nowday) <= 9:
            nowday = "0" + str(nowday)
        monthday = str(nowmonth) + str(nowday)

        if year == str(nowyear):
            if month == monthday:
                count = int(count) + 1
                newversion = 'v' + str(year) + '.' + month + '.' + str('%04d' % count)
                print(newversion)

            elif month != monthday:
                month = monthday
                count = '0001'
                newversion = 'v' + str(year) + '.' + month + '.' + count
                print(newversion)

        elif year != str(nowyear):
            year = str(nowyear)
            if month == monthday:
                count = int(count) + 1
                newversion = 'v' + str(year) + '.' + month + '.' + str('%04d' % count)
                print(newversion)

            elif month != monthday:
                month = monthday
                count = '0001'
                newversion = 'v' + str(year) + '.' + month + '.' + count

        self.util.mysql_execute_sql("UPDATE proj_verion_config SET version = %s WHERE type = %s AND project= %s ",(newversion,type,project))
        return newversion

    def getNowVersion(self, type, project):
        nowversion = self.util.mysql_select_one("SELECT VERSION FROM proj_verion_config WHERE  TYPE=%s AND project = %s",(type,project))
        return nowversion

if __name__ == '__main__':
    version = getVersion()
    version.getNewVersion("WEB","Datacenter")