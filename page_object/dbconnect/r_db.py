import json
import os
from os.path import abspath


class ReadDbConfig():

    def readdb(self,dbtype):

        BASE_DIR = os.path.dirname(os.path.dirname(__file__))
        dir = os.path.join(BASE_DIR, "dbconnect\\dbconfig.json")

        config_dir = (dir)

        with open(config_dir, 'r') as load_str:
            db = json.load(load_str)

        db_m_all = []
        for i in db:
            if dbtype == i:
                for j in db[i]:
                    if dbtype == 'mysql':
                        db_m = db[i][j]
                        db_m_all.append(db_m['HOST'])
                        db_m_all.append(db_m['USER'])
                        db_m_all.append(db_m['PASS'])
                        db_m_all.append(db_m['DB_NAME'])
                        #print("db_m_all:",db_m_all)
                        return db_m_all

                    else:
                        db_m = db[i][j]
                        db_m_all.append(db_m['HOST'])
                        db_m_all.append(db_m['USER'])
                        db_m_all.append(db_m['PASS'])
                        db_m_all.append(db_m['SERVICE_NAME'])
                        #print("db_m_all:", db_m_all)
                        return db_m_all

if __name__ == '__main__':
    read = ReadDbConfig()
    print(read.readdb('mysql'))
