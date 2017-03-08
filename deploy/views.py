from django.shortcuts import render
from EmpAuth.decorators import login_required

# Create your views here.
from saltstack.saltapi import *

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
