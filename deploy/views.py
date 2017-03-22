from django.shortcuts import render
from EmpAuth.decorators import login_required
from SaltRuler.glob_config import glob_config
from saltstack.saltapi import *
from saltstack.models import SaltServer,State
from django import forms
# Create your views here.


@login_required
def app_deploy_html(request):
    return render(request, 'deploy/app_deploy.html')

@login_required
def app_deploy(request):
    ip_list = request.GET['ip_list']
    exec_module = "state.sls"
    state_args = request.GET['app']
    app_deploy_result = api_exec('%s' %(ip_list), '%s' %(exec_module) , arg='%s' %(state_args), arg_num=1)['return'][0]
    return render(request, 'deploy/app_deploy.html', {'app_deploy_result': app_deploy_result})

@login_required
def compute_deploy_html(request):
    return render(request, 'deploy/compute_deploy.html')

@login_required
def compute_deploy(request):
    ip_list = request.GET['ip_list']
    exec_module = "state.sls"
    script_args = request.GET['compute']
    compute_deploy_result = api_exec('%s' %(ip_list), '%s' %(exec_module) , arg='%s' %(script_args), arg_num=1)['return'][0]
    return render(request, 'deploy/compute_deploy.html', {'compute_deploy_result': compute_deploy_result})


class UserForm(forms.Form):
    username = forms.CharField()
    headImg = forms.FileField()


@login_required
def file_upload(request,server_id):
    server_list = SaltServer.objects.all()
    try:
        salt_server = SaltServer.objects.get(id=server_id)
    except:  # id不存在时返回第一个
        salt_server = SaltServer.objects.all()
        if salt_server:
            salt_server=salt_server[0]
        else:
            return render(request, 'deploy/fileupload.html',{'apiinfo':u'请先添加API'})
    sapi = SaltAPI(url=salt_server.url, username=salt_server.username, password=salt_server.password)
    minions = sapi.key_list('key.list_all')['return'][0]['data']['return']['minions']
    tgt = info = cmd_args = cmd_exec_result = ''
    exec_module = "cp.get_url"
    if request.method == 'POST':
        ip_list = request.POST.get('minion')
        ip_lists = request.POST.get('minions')
        path=''
        dest = request.POST.get('dest')
        if ip_list is None and not ip_lists:
            info = '目标主机不能为空'
        elif not dest:
            info = '请输入目标主机存放完整路径，目录必须存在！'
        elif ip_list:
            tgt=ip_list
            upload_result = sapi.SaltCmd(tgt=tgt, fun="cp.get_url", arg=path,arg1=dest)
        elif ip_lists:
            tgt = ip_lists
            upload_result = sapi.SaltCmd(tgt=tgt, fun="cp.get_url", arg=path,arg1=dest)
    return render(request, 'deploy/fileupload.html', {'upload_result': upload_result,'minion_list':minions,'info':info,'arg':cmd_args,'tgt':tgt,'salt_server':salt_server,'server_list':server_list,'url':'cmd_exec'})

