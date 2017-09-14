#coding:utf-8

from django.shortcuts import render_to_response,render,HttpResponse
from django.http import HttpResponseRedirect
from django import forms
from .models import *
from cmdb.models import Assetmanage
import hashlib,json
from .decorators import login_required
from saltstack.saltmaster import saltinfo
from saltstack.saltapi import SaltAPI
from SaltRuler.glob_config import glob_config

# url = glob_config('salt_api','url')
# username = glob_config('salt_api','username')
# password = glob_config('salt_api','password')
# device0 = glob_config('server','dervice0')
# salt_master = glob_config('salt_api','master')
# sapi = SaltAPI(url,username,password)

# Create your views here.
class UserForm(forms.Form):
    username = forms.CharField(max_length=100)
    password = forms.CharField(widget=forms.PasswordInput())




def login(request):
    form = UserForm()
    info=''
    try:
        if request.method == 'POST':
            form = UserForm(request.POST)
            if form.is_valid():
                username = form.cleaned_data['username']
                password = form.cleaned_data['password']
                passwdhash = hashlib.sha1(password + username + 'kbson').hexdigest()
                user = Users.objects.filter(username__exact=username, password__exact=passwdhash)
                if user:
                    request.session['username'] = username
                    return HttpResponseRedirect('/EmpAuth')
                else:
                    info = 'Please check username and password!!'
    except Exception as info:
        pass
    return render_to_response('EmpAuth/login.html', {'form':form, 'info':info})

@login_required
def index(request):
    username = request.session.get('username')
    print username
    if username:
        LocalData={}
        return render_to_response('EmpAuth/home.html', LocalData)
    else:
        return HttpResponseRedirect('EmpAuth/login')

def logout(request):
    try:
        del request.session['username']
    except KeyError:
        pass
    return HttpResponseRedirect('/EmpAuth/login/')

@login_required
def userinfo(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        user_list = Users.objects.filter(username)
    else:
        user_list = Users.objects.all()
    return render(request, 'EmpAuth/show_user.html', {'user_list':user_list})

@login_required
def change(request,id):
    if int(id) == 0:
        username = request.session.get('username')
    else:
        username = Users.objects.get(id=id)
    try:
        info=''
        if request.method == 'POST':
            username = request.POST.get('username')
            oldpass  = request.POST.get('id_old_password')
            password = hashlib.sha1(oldpass + username + 'kbson').hexdigest()
            newpass  = request.POST.get('password01')
            confpass = request.POST.get('password02')
            if confpass == newpass:
                user=Users.objects.filter(username=username,password=password)
                if user:
                    newpasshs = hashlib.sha1(newpass + username + 'kbson').hexdigest()
                    print newpass,newpasshs
                    # user.password=newpasshs
                    Users.objects.filter(username=username,password=password).update(password=newpasshs)
                    info = u"密码修改成功"
                else:
                    info = u'当前密码不正确'
            else:
                info = u'输入的两次新密码不一致！'
    except Exception as e:
        info = e
    contexts={'info':info,'username':username,'id':id}
    return render(request, 'EmpAuth/change.html', contexts)





@login_required
def useradd(request):
    username = request.session.get('username')
    if username == 'kbson'or username == 'admin':
        deps = department.objects.all()
        info=''
        if request.method == 'POST':
            newuser=request.POST.get('username')
            name=request.POST.get('name')
            password1=request.POST.get('password1')
            email=request.POST.get('email')
            dep=request.POST.get('dep')
            user = Users.objects.filter(username=newuser)
            depid=department.objects.filter(department_name=dep).values('id')[0]['id']
            if user:
                info ="Users %s is Exist!!" % newuser
            else:
                user=Users()
                user.username=newuser
                user.name=name
                user.password=password1
                user.email=email
                user.department_id=depid
                user.save()
                info = 'Users %s Add Success!!' % newuser
        return render_to_response( 'EmpAuth/useradd.html', {'info':info,'deps':deps})
    else:
        return HttpResponseRedirect('/EmpAuth/useradd')

@login_required
def userdel(request,id):
    username = request.session.get('username')
    if username == 'kbson'or username == 'admin':
        if request.method == 'GET':
            username = request.GET.get('username')
            Users.objects.filter(id=id).delete()
            return HttpResponseRedirect('/EmpAuth/userinfo')
    else:
        return HttpResponseRedirect('/EmpAuth/usinfo')



@login_required
def gateone(request):
    host_ip = request.GET.get('host',None)
    host_user = request.GET.get('user','root')
    host_port = request.GET.get('port',22)

    if host_port =="":
        host_port=22
        print host_port
    if not host_ip :
        return render_to_response('EmpAuth/404.html',locals(),request)
    else:
        return render_to_response('EmpAuth/gateone.html',locals(),request)

def create_signature(secret, *parts):
    import hmac, hashlib
    hash = hmac.new(secret, digestmod=hashlib.sha1)
    for part in parts:
        hash.update(str(part))
    return hash.hexdigest()

@login_required
def get_auth_obj(request):
    import time, hmac, hashlib, json
    user = request.user.username
    # 安装gateone的服务器以及端口.
    gateone_server = 'https://39.108.6.88/'
    # 之前生成的api_key 和secret
    secret  = "YjJhNDUzZDA4NmU5NGY5MGEwMTdkMDM5NzhkNGY3NGExM"
    api_key = "YTgyYjAxMmViMTYyNDBhMmFhMjFjZTI2NTgwMGJiMjI0O"

    authobj = {
        'api_key': api_key,
        'upn': "gateone",
        'timestamp': str(int(time.time() * 1000)),
        'signature_method': 'HMAC-SHA1',
        'api_version': '1.0'
    }
    my_hash = hmac.new(secret, digestmod=hashlib.sha1)
    my_hash.update(authobj['api_key'] + authobj['upn'] + authobj['timestamp'])

    authobj['signature'] = my_hash.hexdigest()
    auth_info_and_server = {"url": gateone_server, "auth": authobj}
    valid_json_auth_info = json.dumps(auth_info_and_server)
    print valid_json_auth_info
    #   print valid_json_auth_info
    return HttpResponse(valid_json_auth_info)