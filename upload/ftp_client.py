#coding=utf-8
import requests
import sys

def get_down(url,path):
    files = {'file':open(path,'rb')}
    r = requests.post(url,files=files)
    return r.status_code

if __name__ == '__main__':
    url = sys.argv[1]
    path = sys.argv[2]
    http_code = get_down(url,path)
    print http_code