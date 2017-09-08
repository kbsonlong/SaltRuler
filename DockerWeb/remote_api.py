#!/usr/bin/env python
#coding:utf-8

__author__ = 'Luodi'

import docker


'''
Docker 容器API公共模块，可进行容器及镜像管理
'''

class Dockerapi(object):
    def __init__(self, host, port):
        ##由于导入的docker版本不同，所以调用接口函数不一致，据了解docker 2.5.1版本使用的是APIClient，1.10.6使用的是Client
        try:
            self.dockerConnect = docker.APIClient(base_url='tcp://%s:%s' % (host, port), timeout=60)
        except:
            self.dockerConnect = docker.Client(base_url='tcp://%s:%s' % (host, port), timeout=60)

    def GetallContainers(self):
        Containers = self.dockerConnect.containers(all=1)
        return Containers

    def SearchContainers(self, Searchparameter):
        SearchContainer = self.dockerConnect.containers(all=1,filters={'name':[Searchparameter]})
        return SearchContainer

    def ContainerStatus(self, Status):
        StatusContainer = self.dockerConnect.containers(all=1,filters={'status':[Status]})
        return StatusContainer

    def InspectContainer(self,name):
        inspect = self.dockerConnect.inspect_container(container=name)
        return inspect


    def Dockerversion(self):
        Version = self.dockerConnect.version()
        return Version

    def StartContainer(self, name):
        StartContainer = self.dockerConnect.start(container=name)
        return StartContainer

    def StopContainer(self, name):
        StopContainer = self.dockerConnect.stop(container=name)
        return StopContainer

    def DelayedstopContainer(self, name, timeout):
        delayedstop = self.dockerConnect.stop(container=name, timeout=timeout)
        return delayedstop

    def Dockerinfo(self):
        dockerinfo = self.dockerConnect.info()
        return dockerinfo

    def RestartContainer(self, name):
        restart = self.dockerConnect.restart(container=name)
        return restart

    def DelayedRestart(self, name, timeout):
        delayedrestart = self.dockerConnect.restart(container=name, timeout=timeout)
        return delayedrestart

    def RenameDocker(self, name, newname):
        rename = self.dockerConnect.rename(container=name, name=newname)
        return rename

    def TopContainer(self, name):
        topinfo = self.dockerConnect.top(container=name, ps_args=aux)
        return topinfo

    def killContainer(self, name):
        kill = self.dockerConnect.kill(container=name)
        return kill

    def PauseContainer(self, name):
        pause = self.dockerConnect.pause(container=name)
        return pause

    def UnpauseContainer(self, name):
        unpause = self.dockerConnect.unpause(container=name)
        return unpause

    def removeContainer(self, name, v=False, link=False, force=False):
        remove = self.dockerConnect.remove_container(container=name, v=v, link=link, force=force)
        return remove

    def LogContainer(self,name,timestamps=False,tail=all):

        logs = self.dockerConnect.logs(container=name,stdout=True,stderr=True,timestamps=timestamps,tail=tail)

        return logs


    def AllImages(self):
        images=self.dockerConnect.images(all=1)
        return images

    def SearchImage(self,name):
        image = self.dockerConnect.images(name)
        return image

    def DeleteImages(self,imagename):

        data=self.dockerConnect.remove_image(image=imagename,force=False)

        return u"删除镜像成功!!"

    def InitSwarm(self,host,port):
        swarm_info  = self.dockerConnect.init_swarm(advertise_addr='%s:%s' % (host,port))
        return swarm_info

    def JoinSwarm(self,host,port,join_token):
        join_info = self.dockerConnect.join_swarm(remote_addrs=["%s:%s" % (host,port)],join_token=join_token,listen_addr='0.0.0.0:%s' % port,advertise_addr='%s:%s' %(host,port))
        return join_info

    def ShowNodes(self,node_name=None):
        if node_name:
            nodes_info=self.dockerConnect.nodes(filters=node_name)
        else:
            nodes_info = self.dockerConnect.nodes()
        return nodes_info

    def join_token(self,role='Worker'):
        info = self.dockerConnect.inspect_swarm()
        if role == 'Worker':
            return info['JoinTokens']['Worker']
        elif role == 'Manager':
            return info['JoinTokens']['Manager']



if __name__ == '__main__':
    test=Dockerapi('192.168.52.200','2375')
    # print test.GetallContainers()
    # print test.AllImages()[0].keys()
    # for Image in test.AllImages():
    #     print Image
    # print type(test.AllImages())
    #
    # print test.SearchImage('mysql')
    # print test.InitSwarm('192.168.52.200',2377)
    ##获取swarm集群token
    work_token = test.join_token('Worker')
    manager_token = test.join_token('Manager')
    print work_token,manager_token
    # print Dockerapi('192.168.52.201', '2375').JoinSwarm(join_token=work_token,host='192.168.52.201',port='2377')
    # print test.JoinSwarm('192.168.52.200:2377',test.test()['JoinTokens']['Worker'])
    # print test.ShowNodes()[0]['ID'], test.ShowNodes()[0]['Description']['Hostname'], test.ShowNodes()[0]['Status']['Addr'], test.ShowNodes()[0]['Status']['State'], test.ShowNodes()[0]['Spec']['Availability']
