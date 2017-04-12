# -*- coding: utf8 -*-


# vim /etc/systemd/system/multi-user.target.wants/docker.service
# ExecStart=/usr/bin/dockerd --registry-mirror=https://so9gt83b.mirror.aliyuncs.com -H tcp://0.0.0.0:2375 -H unix:///var/run/docker.sock

import docker
import os.path, json, requests
# c = docker.Client(base_url='tcp://192.168.99.101:2375',version='1.14',timeout=10)

url = 'http://192.168.62.200:5000/'

urls =  url.strip("/") + "/v2/"

req = requests.head(urls)


q=""

ReqUrl = url.strip("/") + "/v2/_catalog"

Images = requests.get(ReqUrl,  params={"q": q}).json()

print Images["repositories"]