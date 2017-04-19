#coding:utf-8
from django.shortcuts import render
from EmpAuth.decorators import login_required
from saltstack.saltapi import SaltAPI
from saltstack.models import SaltServer
import time
from deploy.models import files_history
from SaltRuler.glob_config import glob_config
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

    minions = sapi.key_list('key.list_all')['return'][0]['data']['return']
    minion_down = sapi.key_list('manage.status',client='runner')['return'][0]['down']
    if len(minion_down) > 0:
        minion_down = minion_down
    else:
        minion_down = []
    context.update({'minions': minions, 'minion_down': minion_down})
    return render(request, 'saltstack/key_list.html',context )


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
    minions = sapi.key_list('key.list_all')['return'][0]['data']['return']['minions']
    tgt = info = cmd_args = cmd_exec_result = ''
    context = {'salt_server':salt_server,'server_list':server_list,'minion_list':minions,'url':'cmd_exec'}
    exec_module = "cmd.run"
    if request.method == 'POST':
        try:
            ip_list = request.POST.get('minion')
            ip_lists = request.POST.get('minions')
            cmd_args = request.POST.get('arg')
            if ip_list is None and not ip_lists:
                info = '主机不能为空'
            elif not cmd_args:
                info = '请输入执行命令！'
            elif ip_list:
                tgt=ip_list
                cmd_exec_result=sapi.SaltCmd(tgt,exec_module,client='local',arg=cmd_args,expr_form='list')['return'][0]
            elif ip_lists:
                tgt = ip_lists
                cmd_exec_result = sapi.SaltCmd(tgt, exec_module, client='local', arg=cmd_args, expr_form='list')['return'][0]
            context.update({'cmd_exec_result': cmd_exec_result,'info':info,'arg':cmd_args,'tgt':tgt})
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
    context = {'minion_list': minions,  'ret': ret, 'envs': envs, 'env': env,'state': state, 'salt_server': salt_server, 'server_list': server_list, 'url': 'state_exec'}
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
    context = {'minion_list': minions, 'ret': ret, 'envs': envs, 'state': state, 'salt_server': salt_server,
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