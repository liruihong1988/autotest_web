import configparser
import os

class ReadConfig(object):

    def get(self,title,key):
        BASE_DIR = os.path.dirname(__file__)
        sysconfig_dir = os.path.join(BASE_DIR,"sysconfig.ini")
        config = configparser.ConfigParser()
        config.read(sysconfig_dir)
        config_value = config[title][key]
        return config_value

if __name__ == "__main__":
    getcon = ReadConfig()
    print(getcon.get('WEBDRIVER','driver'))