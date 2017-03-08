import os
import ConfigParser

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
config = ConfigParser.ConfigParser()
path = os.path.join(BASE_DIR, 'SaltRuler/config.ini')
# print path
config.read(path)

def glob_config(option,key):
    value = config.get(option,key)
    return value