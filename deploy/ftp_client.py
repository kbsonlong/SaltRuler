#coding=utf-8
import requests
url = 'http://localhost:8080'
path = u'E:\ThunDownload\setuptools-12.0.3.tar.gz'
print path
files = {'file': open(path, 'rb')}
r = requests.post(url, files=files)
print r.url,r.text