
#coding:utf-8

from django.shortcuts import render
from EmpAuth.decorators import login_required
from saltstack.saltapi import SaltAPI
from saltstack.models import SaltServer,State
from django.http import JsonResponse
import json
from SaltRuler import settings
from SaltRuler.glob_config import glob_config
# Create your views here.


saltmaster = glob_config('salt_api','master')



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
            return render(request, 'saltstack/command.html',{'apiinfo':u'请先添加API'})
    sapi = SaltAPI(url=salt_server.url, username=salt_server.username, password=salt_server.password)
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
    return render(request, 'saltstack/key_list.html', {'minions': minions, 'minion_down': minion_down,'salt_server':salt_server,'server_list':server_list,'url':'key_list'})


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
            return render(request, 'saltstack/command.html',{'apiinfo':u'请先添加API'})
    sapi = SaltAPI(url=salt_server.url, username=salt_server.username, password=salt_server.password)
    minions = sapi.key_list('key.list_all')['return'][0]['data']['return']['minions']
    tgt = info = cmd_args = cmd_exec_result = ''
    exec_module = "cmd.run"
    if request.method == 'POST':
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
    return render(request, 'saltstack/command.html', {'cmd_exec_result': cmd_exec_result,'minion_list':minions,'info':info,'arg':cmd_args,'tgt':tgt,'salt_server':salt_server,'server_list':server_list,'url':'cmd_exec'})

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
            return render(request, 'saltstack/command.html',{'apiinfo':u'请先添加API'})
    sapi = SaltAPI(url=salt_server.url, username=salt_server.username, password=salt_server.password)
    envs = sapi.SaltRun(client='runner', fun='fileserver.envs')['return'][0]
    minions = sapi.key_list('key.list_all')['return'][0]['data']['return']['minions']
    env = envs[0]
    if request.POST.get('tgt'):
        minion = request.POST.get('tgt')
    else:
        minion=minions[0]
    if request.POST.get('env'):
        env = request.POST.get('env')
        state = request.POST.get('state')
        if minion and state:
            ret=sapi.SaltCmd(minion,fun='state.sls',client='local',arg=state)['return'][0]
    roots = sapi.SaltRun(client='wheel', fun='file_roots.list_roots')['return'][0]['data']['return']

    dirs = roots[env][0]

    states = []
    for root, dirs in dirs.items():  # root="/srv/salt/prod/"  dirs={"init":{"epel.sls":"f",}}
        for dir, files in dirs.items():  # dir='init' or 'top.sls'    files={"epel.sls":"f",}
            if dir == '.svn':
                pass
            elif files == "f" and dir.endswith('.sls'):
                states.append(dir[0:-4])
            elif isinstance(files, dict):
                for sls, f in files.items():
                    if f == 'f' and sls.endswith('.sls'):
                        states.append('%s.%s' % (dir, sls[0:-4]))
    result = sorted(states)
    if result and not state:
        state=result[0]
    return render(request, 'saltstack/state.html', {'minion_list': minions,'minion':minion, 'ret': ret,'envs':envs,'env':env,'states':result,'state':state,'salt_server':salt_server,'server_list':server_list,'url':'state_exec'})

def state_fun(request,server_id):
    if request.is_ajax() and request.method == 'GET':
        tgt=request.GET.get('tgt','')
        env=request.GET.get('env','')
        state=request.GET.get('state','')
        states=[]
        try:
            salt_server = SaltServer.objects.get(id=server_id)
            sapi = SaltAPI(url=salt_server.url,username=salt_server.username,password=salt_server.password)
            if env:
                if state and tgt:
                    arg=state.rstrip(',')
                    result=sapi.SaltCmd(client='local',tgt=tgt,fun='state.sls',arg=arg,arg1='saltenv=%s'%env,expr_form='list')['return'][0]
                    Res=State(client='local',minions=tgt,fun='state.sls',arg=arg,tgt_type='list',server=salt_server,user=request.user.username,result=json.dumps(result))
                    Res.save()
                else:
                    roots=sapi.SaltRun(client='wheel',fun='file_roots.list_roots')['return'][0]['data']['return']
                    dirs=roots[env][0]                #dirs={"/srv/salt/prod/":{}}
                    for root,dirs in dirs.items():   #root="/srv/salt/prod/"  dirs={"init":{"epel.sls":"f",}}
                        for dir,files in dirs.items():         #dir='init' or 'top.sls'    files={"epel.sls":"f",}
                            if  dir == '.svn' :pass
                            elif files == "f" and dir.endswith('.sls'):
                                states.append(dir[0:-4])
                            elif isinstance(files,dict):
                                for sls,f in files.items():
                                    if f=='f' and sls.endswith('.sls'):
                                        states.append('%s.%s'%(dir,sls[0:-4]))
                    result=sorted(states)
        except Exception as e:
            result = str(e)
        return JsonResponse(result,safe=False)




