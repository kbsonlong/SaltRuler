#coding:utf-8

import os
from django.shortcuts import render,HttpResponseRedirect
from EmpAuth.decorators import login_required
from SaltRuler.glob_config import glob_config
from saltstack.saltapi import *
from .models import Assetmanage, Servers
from deploy.models import Upload
from django import forms
from cmdb.models import Servers
from saltstack.models import SaltServer
from saltstack.tasks import *

class UpForm(forms.Form):
    headImg = forms.FileField(label='')

url = glob_config('salt_api','url')
username = glob_config('salt_api','username')
password = glob_config('salt_api','password')
device0 = glob_config('server','dervice0')
sapi=SaltAPI(url,username,password)

@login_required
def asset_table(request):
    uf = UpForm()
    a=[]
    info = ''

    ###批量导入主机
    if request.method == "POST":
        uf = UpForm(request.POST, request.FILES)
        if uf.is_valid():
            # 获取表单信息
            headImg = uf.cleaned_data['headImg']
            upload = Upload()
            upload.headImg = headImg
            upload.save()
            try:

                f = open(u'./upload/%s' % str(headImg))
                List = []
                for line in f:
                    values = line.split(',')
                    List.append(Assetmanage(asset_num=values[0].strip(' '), type=values[1].strip(' '),
                                            server_ip=values[2].strip(' '), remote_ip=values[3].strip(' '),
                                            data_center=values[4].strip(' '), room_num=values[5].strip(' '),
                                            rack_num=values[6].strip(' '), system_type=values[7].strip(' '),
                                            cputype_num=values[8].strip(' '), disksize_num=values[9].strip(' '),
                                            memsize_num=values[10].strip(' '), disk_raid=values[11].strip(' '),
                                            card_type_num=values[12].strip(' '), power_num=values[13].strip(' '),
                                            service_num=values[14].strip(' '), buy_time=values[15].strip(' '),
                                            expiration_time=values[16].strip(' '), note=values[17].strip(' ')))
                f.close()
                Assetmanage.objects.bulk_create(List)
                info = 'Success!'
            except Exception as error:
                info = error
            finally:
                os.remove(u'./upload/%s' % str(headImg))  ###不管导入是否成功，删除上传的文件，避免修改数据后上传同名文件还是调用旧数据
    asset_list = Assetmanage.objects.all()
    for asset in asset_list:
        asset_dict = {'asset_num': '%s' % (asset.asset_num),'type': '%s' % (asset.type),
                'server_ip': '%s' % (asset.server_ip),'remote_ip': '%s' % (asset.remote_ip),
                'data_center': '%s' % (asset.data_center),
                'room_num': '%s' % (asset.room_num),'rack_num': '%s' % (asset.rack_num),
                'system_type': '%s' % (asset.system_type),'cputype_num': '%s' % (asset.cputype_num),
                'disksize_num': '%s' % (asset.disksize_num),'memsize_num': '%s' % (asset.memsize_num),
                'disk_raid': '%s' % (asset.disk_raid),'card_type_num': '%s' % (asset.card_type_num),
                'power_num': '%s' % (asset.power_num),'service_num': '%s' % (asset.service_num),
                'buy_time': '%s' % (asset.buy_time),'expiration_time': '%s' % (asset.expiration_time),
                'note': '%s' % (asset.note),'assetget_url': asset}
        a.append(asset_dict)
    return render(request, 'cmdb/asset_table.html', {'a' : a,'uf':uf,'info':info})

@login_required
def asset_add(request):
    if request.GET.get('asset_num') is None or request.GET.get('server_ip') is None or request.GET.get('service_num') is None:
        info={}
        info['info'] = '(带*号必填项！)'
        return render(request, 'cmdb/asset_add.html',info)
    else:
        asset_num = request.GET.get('asset_num')
        type = request.GET.get('type')
        server_ip = request.GET.get('server_ip')
        remote_ip = request.GET.get('remote_ip')
        data_center = request.GET.get('data_center')
        room_num = request.GET.get('room_num')
        rack_num = request.GET.get('rack_num')
        system_type = request.GET.get('system_type')
        cputype_num = request.GET.get('cputype_num')
        disksize_num = request.GET.get('disksize_num')
        memsize_num = request.GET.get('memsize_num')
        disk_raid = request.GET.get('disk_raid')
        card_type_num = request.GET.get('card_type_num')
        power_num = request.GET.get('power_num')
        service_num = request.GET.get('service_num')
        buy_time = request.GET.get('buy_time')
        expiration_time = request.GET.get('expiration_time')
        note = request.GET.get('note')
        Assetmanage.objects.create(asset_num="%s" % (asset_num),type="%s" % (type),
                               server_ip="%s" % (server_ip),remote_ip="%s" % (remote_ip),
                               data_center="%s" % (data_center),room_num="%s" % (room_num),
                               rack_num="%s" % (rack_num),system_type="%s" % (system_type),
                               cputype_num="%s" % (cputype_num),disksize_num="%s" % (disksize_num),
                               memsize_num="%s" % (memsize_num),disk_raid="%s" % (disk_raid),
                               card_type_num="%s" % (card_type_num),power_num="%s" % (power_num),
                               service_num="%s" % (service_num),buy_time="%s" % (buy_time),
                               expiration_time="%s" % (expiration_time),note="%s" % (note))
        asset = Assetmanage.objects.get(asset_num="%s" % (asset_num))
        asset_add = {'asset_num': '%s' % (asset.asset_num),'type': '%s' % (asset.type),
                 'server_ip': '%s' % (asset.server_ip),'remote_ip': '%s' % (asset.remote_ip),
                 'data_center': '%s' % (asset.data_center),
                 'room_num': '%s' % (asset.room_num),'rack_num': '%s' % (asset.rack_num),
                 'system_type': '%s' % (asset.system_type),'cputype_num': '%s' % (asset.cputype_num),
                 'disksize_num': '%s' % (asset.disksize_num),'memsize_num': '%s' % (asset.memsize_num),
                 'disk_raid': '%s' % (asset.disk_raid),'card_type_num': '%s' % (asset.card_type_num),
                 'power_num': '%s' % (asset.power_num),'service_num': '%s' % (asset.service_num),
                 'buy_time': '%s' % (asset.buy_time),'expiration_time': '%s' % (asset.expiration_time),
                 'note': '%s' % (asset.note)}
        return render(request, 'cmdb/asset_add.html',{'asset_add':asset_add,'info':'添加成功!'})


@login_required
def asset_update(request):
    asset_update = asset_num = info = ''
    if request.GET.get('asset_num'):
        asset_num = request.GET.get('asset_num')
    if request.method == 'POST':
        asset_num = request.POST.get('asset_num')
        type = request.POST.get('type')
        server_ip = request.POST.get('server_ip')
        remote_ip = request.POST.get('remote_ip')
        data_center = request.POST.get('data_center')
        room_num = request.POST.get('room_num')
        rack_num = request.POST.get('rack_num')
        system_type = request.POST.get('system_type')
        cputype_num = request.POST.get('cputype_num')
        disksize_num = request.POST.get('disksize_num')
        memsize_num = request.POST.get('memsize_num')
        disk_raid = request.POST.get('disk_raid')
        card_type_num = request.POST.get('card_type_num')
        power_num = request.POST.get('power_num')
        service_num = request.POST.get('service_num')
        buy_time = request.POST.get('buy_time')
        expiration_time = request.POST.get('expiration_time')
        note = request.POST.get('note')
        asset_update=''
        if asset_num:
            update = Assetmanage.objects.get(asset_num="%s" % (asset_num))
        if type != '':
            update.type = "%s" % (type)
            update.save()
        if server_ip != '':
            update.server_ip = "%s" % (server_ip)
            update.save()
        if remote_ip != '':
            update.remote_ip = "%s" % (remote_ip)
            update.save()
        if data_center != '':
            update.data_center = "%s" % (data_center)
            update.save()
        if room_num != '':
            update.room_num = "%s" % (room_num)
            update.save()
        if rack_num != '':
            update.rack_num = "%s" % (rack_num)
            update.save()
        if system_type != '':
            update.system_type = "%s" % (system_type)
            update.save()
        if cputype_num != '':
            update.cputype_num = "%s" % (cputype_num)
            update.save()
        if disksize_num != '':
            update.disksize_num = "%s" % (disksize_num)
            update.save()
        if memsize_num != '':
            update.memsize_num = "%s" % (memsize_num)
            update.save()
        if disk_raid != '':
            update.disk_raid = "%s" % (disk_raid)
            update.save()
        if card_type_num != '':
            update.card_type_num = "%s" % (card_type_num)
            update.save()
        if power_num != '':
            update.power_num = "%s" % (power_num)
            update.save()
        if service_num != '':
            update.service_num = "%s" % (service_num)
            update.save()
        if buy_time != '':
            update.buy_time = "%s" % (buy_time)
            update.save()
        if expiration_time != '':
            update.expiration_time = "%s" % (expiration_time)
            update.save()
        if note != '':
            update.note = "%s" % (note)
            update.save()
        info = '更新成功！'
    if asset_num:
        asset = Assetmanage.objects.get(asset_num="%s" % (asset_num))
        asset_update = {'asset_num': '%s' % (asset.asset_num),'type': '%s' % (asset.type),
                     'server_ip': '%s' % (asset.server_ip),'remote_ip': '%s' % (asset.remote_ip),
                     'data_center': '%s' % (asset.data_center),
                     'room_num': '%s' % (asset.room_num),'rack_num': '%s' % (asset.rack_num),
                     'system_type': '%s' % (asset.system_type),'cputype_num': '%s' % (asset.cputype_num),
                     'disksize_num': '%s' % (asset.disksize_num),'memsize_num': '%s' % (asset.memsize_num),
                     'disk_raid': '%s' % (asset.disk_raid),'card_type_num': '%s' % (asset.card_type_num),
                     'power_num': '%s' % (asset.power_num),'service_num': '%s' % (asset.service_num),
                     'buy_time': '%s' % (asset.buy_time),'expiration_time': '%s' % (asset.expiration_time),
                     'note': '%s' % (asset.note)}
    return render(request, 'cmdb/asset_update.html', {'asset_update':asset_update,'asset_num':asset_num,'info':info})



@login_required
def asset_del(request):
    asset_num = request.GET.get('asset_num')
    asset = Assetmanage.objects.get(asset_num="%s" % (asset_num))
    Assetmanage.objects.get(asset_num="%s" % (asset_num)).delete()
    a = []
    asset_list = Assetmanage.objects.all()
    for asset in asset_list:
        asset_dict = {'asset_num': '%s' % (asset.asset_num), 'type': '%s' % (asset.type),
                      'server_ip': '%s' % (asset.server_ip), 'remote_ip': '%s' % (asset.remote_ip),
                      'data_center': '%s' % (asset.data_center),
                      'room_num': '%s' % (asset.room_num), 'rack_num': '%s' % (asset.rack_num),
                      'system_type': '%s' % (asset.system_type), 'cputype_num': '%s' % (asset.cputype_num),
                      'disksize_num': '%s' % (asset.disksize_num), 'memsize_num': '%s' % (asset.memsize_num),
                      'disk_raid': '%s' % (asset.disk_raid), 'card_type_num': '%s' % (asset.card_type_num),
                      'power_num': '%s' % (asset.power_num), 'service_num': '%s' % (asset.service_num),
                      'buy_time': '%s' % (asset.buy_time), 'expiration_time': '%s' % (asset.expiration_time),
                      'note': '%s' % (asset.note), 'assetget_url': asset}
        a.append(asset_dict)
    return render(request, 'cmdb/asset_table.html', {'a' : a})


@login_required
def host_add_html(request):
    info = host_dict = server_ip = ''
    if request.GET.get('server_ip'):
        server_ip = request.GET.get('server_ip')
    if request.method == 'POST':
        ser_ip = request.POST.get('host_ip')
        local_ip = request.POST.get('local_ip')
        if ser_ip == "" or local_ip == "":
            info = '主机IP、宿主IP不允许为空！'
        else:
            host_id = Assetmanage.objects.get(server_ip=ser_ip)
            if not Servers.objects.filter(local_ip=local_ip):
                Servers.objects.create(host_ip=host_id, local_ip=local_ip)
            else:
                host = Servers.objects.get(local_ip=local_ip)
                print host
                host.host_ip_id = host_id
                host.save()
            # servers = Servers.objects.get(local_ip=local_ip)
            # host_dict = {'host_ip': '%s' % (servers.local_ip), 'local_ip': '%s' % (servers.local_ip), 'status': status,
            #              'host_name': '%s' % (servers.hostname),
            #              'system_version': '%s' % (servers.OS),
            #              'cpu_num': '%s' % (servers.Cpus),
            #              'mem_size': '%s' % (servers.Mem), 'host_note': '%s' % (servers.Cpu_type)}
            info = '添加成功!'
    return render(request, 'cmdb/host_add.html',{'host_add':host_dict,'info':info,'server_ip':server_ip})

@login_required
def host_table(request):
    servers_list = Servers.objects.all()
    contexts = {}
    b = []
    for servers in servers_list:
        if servers.server_status == 0:
            status = 'up'
        else:
            status = 'down'
        host_dict = {'host_ip': '%s' % (servers.local_ip), 'local_ip': '%s' % (servers.local_ip), 'status': status,
                     'host_name': '%s' % (servers.hostname),
                     'system_version': '%s' % (servers.OS),
                     'cpu_num': '%s' % (servers.Cpus),
                     'mem_size': '%s' % (servers.Mem), 'host_note': '%s' % (servers.Cpu_type)}
        b.append(host_dict)
    contexts.update({'b': b})
    return render(request, 'cmdb/host_table.html', contexts)


@login_required
def host_update_html(request):
    host_update=''
    info=''
    if request.method == 'POST':
        server_ip = request.POST.get('host_ip')
        local_ip = request.POST.get('local_ip')
        app = request.POST.get('app')
        host_note = request.POST.get('host_note')
        if server_ip != '':
            host_ip = Assetmanage.objects.get(server_ip=server_ip)
        else:
            host_ip = ''
        update = Servers.objects.get(local_ip="%s" % (local_ip))
        if host_ip != '':
            update.host_ip = host_ip
            update.save()
        if app != '':
            update.app = "%s" % (app)
            update.save()
        if host_note != '':
            update.host_note = "%s" % (host_note)
            update.save()
        host = Servers.objects.get(local_ip="%s" % (local_ip))
        host_update = {'host_ip': '%s' % (host.host_ip.server_ip), 'local_ip': '%s' % (host.local_ip),
                       'app':app,'note':host_note
                       }
        info ='更新成功！！'
    return render(request, 'cmdb/host_update.html',{'host_update':host_update,'info':info})



@login_required
def host_del_html(request):
    host_del=local_ip=info=''
    if request.method == 'POST':
        local_ip = request.POST.get('local_ip')
        Servers.objects.get(local_ip="%s" % (local_ip)).delete()
        info = u'删除成功！！'
    if request.GET.get('local_ip'):
        local_ip = request.GET.get('local_ip')
        Servers.objects.get(local_ip="%s" % (local_ip)).delete()
        info = u'%s 删除成功！！' % local_ip
        return render(request, 'cmdb/host_table.html',{'host_del':host_del,'success':info})
    return render(request, 'cmdb/host_del.html', {'host_del': host_del, 'success': info})

@login_required
def host_list(request, server_ip):
    host_ip_ids = Assetmanage.objects.filter(server_ip=server_ip)
    asset_id = host_ip_ids.values('id')[0]['id']
    servers_list = Servers.objects.filter(host_ip_id=asset_id)
    host_ip = Assetmanage.objects.filter(id=asset_id).values('server_ip')[0]['server_ip']
    contexts = {'server_ip':host_ip}
    b = []
    for servers in servers_list:
        if servers.server_status == 0:
            status = 'up'
        else:
            status = 'down'
        host_dict = {'host_ip': '%s' % (servers.local_ip), 'local_ip': '%s' % (servers.local_ip), 'status': status,
                     'host_name': '%s' % (servers.hostname),
                     'system_version': '%s' % (servers.OS),
                     'cpu_num': '%s' % (servers.Cpus),
                     'mem_size': '%s' % (servers.Mem), 'host_note': '%s' % (servers.Cpu_type)}
        b.append(host_dict)
    contexts.update({'b': b})
    return render(request, 'cmdb/host_table.html', contexts)



@login_required
def server_collect(request,server_id):
    server_list = SaltServer.objects.all()
    tgt = request.GET.get('ip')
    servers_list = Servers.objects.all()
    contexts = {'server_list': server_list, 'server_id': server_id}
    b=[]
    for servers in servers_list:
        if servers.server_status == 0:
            status = 'up'
        else:
            status = 'down'
        host_dict = {'host_ip': '%s' % (servers.local_ip), 'local_ip': '%s' % (servers.local_ip), 'status': status,
                     'host_name': '%s' % (servers.hostname),
                     'system_version': '%s' % (servers.OS),
                     'cpu_num': '%s' % (servers.Cpus),
                     'mem_size': '%s' % (servers.Mem), 'host_note': '%s' % (servers.Cpu_type)}
        b.append(host_dict)

    contexts.update({'b':b})
    result = server_collects.delay(tgt=tgt,server_id=server_id)
    print result.ready()


    return render(request, 'cmdb/host_table.html', contexts)
    # return HttpResponseRedirect("/cmdb/host_table/")

