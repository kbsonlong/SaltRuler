#coding:utf-8

from django.test import TestCase

# Create your tests here.
try:
    from docker import Client
except:
    from docker import APIClient as Client


from registry_api import BASE_REGISTRY_API
c = Client(base_url='tcp://192.168.62.200:2375',version='1.14',timeout=10)
# c = Client(base_url='unix://var/run/docker.sock',version='1.14',timeout=10)
# print c.images()
# import docker


#sssss

url = 'http://192.168.62.200:5000/'   ##私有仓库地址

b = BASE_REGISTRY_API()
print b.get_imageId_info(ImageId="sha256:9087edac75d18fbcaffbf6ed3f0fa34e726bd5e6abefe2d4cd0fdf4a493eb43b",url=url,version=2,tag="latest",ImageName="shipyard")['data']['history']
# client = docker.from_env()
# print client.containers.run("alpine", ["echo", "hello", "world"])

##查看所有镜像
# print c.images()[0].keys()

# curl 'http://127.0.0.1:2375/images/json?all=0' | python -m json.tool

##创建容器
# container_id =  c.create_container(image='nginx')['Id']

# ##启动、停止、重启、删除容器
# c.start(container=container_id)
# c.stop(container=container_id)
# c.restart(container=container_id)
# c.logs(container=container_id)
# c.remove_container(container=container_id,force=True)
# c.start(container='a610e5b536c4547a01017c4dbe2d755bc336d2f939294b1e77f3613b85f70b57')
# c.stop(container='a610e5b536c4547a01017c4dbe2d755bc336d2f939294b1e77f3613b85f70b57')
# c.restart(container='a610e5b536c4547a01017c4dbe2d755bc336d2f939294b1e77f3613b85f70b57')
# c.logs(container="4324fd63a0a5")
# c.inspect_container(container="4324fd63a0a5")
# c.remove_container(container='a610e5b536c4547a01017c4dbe2d755bc336d2f939294b1e77f3613b85f70b57')
# print c.containers(all)
# print c.tag(image='nginx',repository='registry')

