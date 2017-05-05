#coding:utf-8
from celery import task
from saltstack.models import SaltServer
from cmdb.models import Servers
from saltstack.saltapi import SaltAPI

@task
def add(x, y):
    return x + y

@task
def server_collects(tgt='*',server_id=0):
    server_list = SaltServer.objects.all()
    contexts = {'server_list': server_list, 'server_id': server_id}
    try:
        try:
            salt_server = SaltServer.objects.get(id=server_id)
        except Exception as e:  # id不存在时返回第一个
            salt_server = SaltServer.objects.all()[0]
    except Exception as e:
        contexts.update({'error': e})
    try:
        sapi = SaltAPI(url=salt_server.url, username=salt_server.username, password=salt_server.password)
        print salt_server.url
        grains = sapi.SaltCmd(tgt=tgt, fun='grains.items', client='local')['return'][0]
        minions = sapi.key_list('manage.status', client='runner')['return'][0]
        if salt_server and grains:
            for i in grains.keys():
                try:
                    server = Servers.objects.get(local_ip=i)
                except:
                    server = Servers()
                if i in minions['up']:
                    minions_status = '0'
                else:
                    minions_status = '1'
                server.hostname = grains[i]['host']
                server.local_ip = grains[i]['id']
                server.OS = "%s %s" % (grains[i]['os'], grains[i]['osrelease'])
                server.Mem = grains[i]['mem_total']
                server.Cpus = grains[i]['num_cpus']
                server.Cpu_type = grains[i]['cpu_model']
                server.minion_id = grains[i]['id']
                server.app = grains[i]['virtual']
                server.server_status = minions_status
                server.save()
                contexts.update({'success': u'%s 收集成功' % tgt, 'server_id': salt_server.id})
        if not grains:
            contexts.update({'error': u'%s 主机不存在或者离线' % tgt})
    except Exception as e:
        contexts.update({'error': '%s %s' % (tgt, e)})
    return contexts