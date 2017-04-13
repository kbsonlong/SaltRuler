#coding:utf-8

from django.test import TestCase

# Create your tests here.
try:
    from docker import Client
except:
    from docker import APIClient as Client

c = Client(base_url='tcp://192.168.62.200:2375',version='1.14',timeout=10)

##查看所有镜像
print c.images()[0].keys()

# curl 'http://127.0.0.1:2375/images/json?all=0' | python -m json.tool

##创建容器
# c.create_container(image='nginx')

# ##启动、停止、重启容器
# c.start(container='a610e5b536c4547a01017c4dbe2d755bc336d2f939294b1e77f3613b85f70b57')
# c.stop(container='a610e5b536c4547a01017c4dbe2d755bc336d2f939294b1e77f3613b85f70b57')
# c.restart(container='a610e5b536c4547a01017c4dbe2d755bc336d2f939294b1e77f3613b85f70b57')
