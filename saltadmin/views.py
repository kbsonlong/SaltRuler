#coding:utf-8
from django.shortcuts import render,HttpResponse,render_to_response
from EmpAuth.decorators import login_required
from saltadmin.saltapi import SaltAPI
from saltadmin.models import SaltServer
import time,json
from deploy.models import files_history
from SaltRuler.glob_config import glob_config
from saltadmin.models import *
# Create your views here.


saltmaster = glob_config('salt_api','master')
fh = files_history()


@login_required
def key_list(request,server_id):

    server_list = SaltServer.objects.all()
    try:
        salt_server = SaltServer.objects.get(id=server_id)
    except:  # id不存在时返回第一个
        salt_server = SaltServer.objects.all()
        if salt_server:
            salt_server = salt_server[0]
        else:
            return render(request, 'saltstack/command.html',{'apiinfo':u'请先添加SaltServer API'})
    sapi = SaltAPI(url=salt_server.url, username=salt_server.username, password=salt_server.password)
    context = {'salt_server':salt_server,'server_list':server_list,'url':'key_list'}
    if request.method == 'POST':
        if request.POST.get('accept'):
            accept_minion = request.POST.get('accept')
            sapi.key_list(fun='key.accept',match=accept_minion)
        else:
            delete_minion = request.POST.get('delete')
            sapi.key_list(fun='key.delete',match=delete_minion)

    key_status = sapi.key_list('key.list_all')['return']
    minions_accept = key_status[0]['data']['return']['minions']
    minions_denied = key_status[0]['data']['return']['minions_denied']
    minions_rejected = key_status[0]['data']['return']['minions_rejected']
    minions_pre = key_status[0]['data']['return']['minions_pre']
    # minion_down = sapi.key_list('manage.status', client='runner')['return']
    minions = minions_accept+minions_denied+minions_rejected+minions_pre
    insert = []
    for minion in minions_accept:
        try:
            m = Minions.objects.get(minion=minion)
            m.status="Accepted"
            m.save()
        except:
            insert.append(Minions(minion=minion,saltserver=salt_server,status="Accepted"))
    for minion in minions_rejected:
        try:
            m = Minions.objects.get(minion=minion)
            m.status="Rejected"
            m.save()
        except:
            insert.append(Minions(minion=minion,saltserver=salt_server,status="Rejected"))

    for minion in minions_pre:
        try:
            m = Minions.objects.get(minion=minion)
            m.status="Unaccepted"
            m.save()
        except:
            insert.append(Minions(minion=minion,saltserver=salt_server,status="Unaccepted"))
    Minions.objects.bulk_create(insert)


    # if len(minion_down[0]['down']) > 0:
    #     minion_down = minion_down[0]['down']
    # else:
    #     minion_down = []
    context.update({'minions': minions, 'minion_down': "",'minions_pre':minions_pre})
    return render(request, 'saltstack/key_list.html',context )


##获取minion组的minion
@login_required
def get_minion(request,server_id):
    server_list = SaltServer.objects.all()
    try:
        salt_server = SaltServer.objects.get(id=server_id)
    except:  # id不存在时返回第一个
        salt_server = SaltServer.objects.all()
        if salt_server:
            salt_server = salt_server[0]
        else:
            return render(request, 'saltstack/command.html', {'apiinfo': u'请先添加SaltServer API'})
    contexts = {}
    group = request.GET.get("group")
    is_state = request.GET.get("state")
    minions =MinionGroup.objects.get(groupname=group).minions.all()
    minion_group = MinionGroup.objects.all()
    contexts.update({"minions":minions, 'salt_server': salt_server,'server_list':server_list,'minion_group':minion_group,'group':group})
    print is_state
    if is_state:
        return render(request, 'saltstack/state.html', contexts)
    return render(request,'saltstack/command.html',contexts)

@login_required
def cmd_exec(request,server_id):
    server_list = SaltServer.objects.all()
    try:
        salt_server = SaltServer.objects.get(id=server_id)
    except:  # id不存在时返回第一个
        salt_server = SaltServer.objects.all()
        if salt_server:
            salt_server=salt_server[0]
        else:
            return render(request, 'saltstack/command.html',{'apiinfo':u'请先添加SaltServer API'})
    sapi = SaltAPI(url=salt_server.url, username=salt_server.username, password=salt_server.password)
    minion_group = MinionGroup.objects.all()
    minions = sapi.key_list('key.list_all')['return'][0]['data']['return']['minions']
    tgt = info  = cmd_exec_result =minion_list= ''

    context = {'salt_server':salt_server,'server_list':server_list,'minions':minions,'url':'cmd_exec'}
    exec_module = "cmd.run"
    if request.method == 'POST':
        try:
            ip_list = request.POST.get('minion')
            cmd_args = request.POST.get('arg')
            group = request.POST.get('group')
            minions = MinionGroup.objects.get(groupname=group).minions.all()

            if not cmd_args:
                info = '请输入执行命令！'
            elif ip_list:
                tgt=ip_list
                cmd_exec_result=sapi.SaltCmd(tgt,exec_module,client='local',arg=cmd_args,expr_form='list')['return'][0]
            else:
                for i in minions.values('minion'):
                    minion_list += i['minion'] + ','
                tgt=minion_list.strip(',')
                cmd_exec_result = sapi.SaltCmd(tgt, exec_module, client='local', arg=cmd_args, expr_form='list')['return'][0]
            context.update({'cmd_exec_result': cmd_exec_result,'info':info,'arg':cmd_args,'tgt':tgt,'group':group,'minions':minions})
        except Exception as e:
            if request.POST.get('minion'):
                tgt = request.POST.get('minion')
            if request.POST.get('minions'):
                tgt = request.POST.get('minions')
            cmd_exec_result = e
            context.update({'error':e})
        ##添加审计记录
        fh.username = request.session.get('username')
        fh.active = 'exec command'
        fh.active_time = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
        fh.remote_server = tgt
        fh.path = cmd_exec_result
        fh.save()
    context.update({'minion_group':minion_group})

    return render(request, 'saltstack/command.html', context)

@login_required
def state_exec(request,server_id):
    ret = state=''
    server_list = SaltServer.objects.all()
    try:
        salt_server = SaltServer.objects.get(id=server_id)
    except:  # id不存在时返回第一个
        salt_server = SaltServer.objects.all()
        if salt_server:
            salt_server = salt_server[0]
        else:
            return render(request, 'saltstack/state.html',{'apiinfo':u'请先添加SaltServer API'})
    sapi = SaltAPI(url=salt_server.url, username=salt_server.username, password=salt_server.password)
    envs = sapi.SaltRun(client='runner', fun='fileserver.envs')['return'][0]
    minions = sapi.key_list('key.list_all')['return'][0]['data']['return']['minions']
    env = envs[0]
    context = {'minions': minions,  'ret': ret, 'envs': envs, 'env': env,'state': state, 'salt_server': salt_server, 'server_list': server_list, 'url': 'state_exec'}
    if request.method == 'POST':
        try:
            if request.POST.get('tgt'):
                minion = request.POST.get('tgt')
            else:
                minion=minions[0]
            if request.POST.get('env'):
                env = request.POST.get('env')
                state = request.POST.get('state')
                if minion and state:
                    ret=sapi.SaltCmd(tgt=minion,fun='state.sls',client='local',arg=state,arg1='saltenv=%s'%env)['return'][0]
            roots = sapi.SaltRun(client='wheel', fun='file_roots.list_roots')['return'][0]['data']['return']
            dirs = roots[env][0]
            states = []
            for root, dirs in dirs.items():  # root="/srv/salt/prod/"  dirs={"init":{"epel.sls":"f",}}
                for dir, files in dirs.items():  # dir='init' or 'top.sls'    files={"epel.sls":"f",}
                    if dir == '.svn':
                        dir = '.svn'
                    elif files == "f" and dir.endswith('.sls'):
                        states.append(dir[0:-4])
                    elif isinstance(files, dict):
                        for sls, f in files.items():
                            if f == 'f' and sls.endswith('.sls'):
                                states.append('%s.%s' % (dir, sls[0:-4]))
            result = sorted(states)
            if result and not state:
                state=result[0]
            context.update({'minion': minion,'ret': ret, 'states': result,'env':env,'state':state})
        except Exception as e:
            context.update({'error':e})

        fh.username = request.session.get('username')
        fh.active = u'state 编排'
        fh.active_time = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
        fh.remote_server = ''
        fh.path = state
        fh.save()
    return render(request, 'saltstack/state.html', context)

##
@login_required
def state_fun(request,server_id):
    ret = state = ''
    server_list = SaltServer.objects.all()
    try:
        salt_server = SaltServer.objects.get(id=server_id)
    except:  # id不存在时返回第一个
        salt_server = SaltServer.objects.all()
        if salt_server:
            salt_server = salt_server[0]
        else:
            return render(request, 'saltstack/state.html', {'apiinfo': u'请先添加SaltServer API'})
    sapi = SaltAPI(url=salt_server.url, username=salt_server.username, password=salt_server.password)
    envs = sapi.SaltRun(client='runner', fun='fileserver.envs')['return'][0]
    minions = sapi.key_list('key.list_all')['return'][0]['data']['return']['minions']
    context = {'minions': minions, 'ret': ret, 'envs': envs, 'state': state, 'salt_server': salt_server,
               'server_list': server_list, 'url': 'state_exec'}
    if request.is_ajax() or request.method == 'GET':
        try:
            if request.GET.get('tgt'):
                minion = request.GET.get('tgt')
            else:
                minion = minions[0]
            if request.GET.get('env'):
                env = request.GET.get('env')
                state = request.GET.get('state')
                if minion and state:
                    ret = sapi.SaltCmd(minion, fun='state.sls', client='local', arg=state,arg1='saltenv=%s'%env)['return'][0]
            roots = sapi.SaltRun(client='wheel', fun='file_roots.list_roots')['return'][0]['data']['return']
            dirs = roots[env][0]
            states = []
            for root, dirs in dirs.items():  # root="/srv/salt/prod/"  dirs={"init":{"epel.sls":"f",}}
                for dir, files in dirs.items():  # dir='init' or 'top.sls'    files={"epel.sls":"f",}
                    if dir == '.svn':
                        dir = '.svn'
                    elif files == "f" and dir.endswith('.sls'):
                        states.append(dir[0:-4])
                    elif isinstance(files, dict):
                        for sls, f in files.items():
                            if f == 'f' and sls.endswith('.sls'):
                                states.append('%s.%s' % (dir, sls[0:-4]))
            result = sorted(states)
            if result and not state:
                state = result[0]

            context.update({'minion': minion,'ret': ret, 'states': result,'env':env,'state':state})
        except Exception as e:
            context.update({'error': e})
    return render(request,'saltstack/state.html',context)


