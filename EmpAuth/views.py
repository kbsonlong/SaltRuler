#coding:utf-8

from django.shortcuts import render_to_response,render
from django.http import HttpResponseRedirect
from django import forms
from .models import Users
from cmdb.models import Assetmanage
import hashlib,json
from .decorators import login_required
from saltstack.saltmaster import saltinfo
from saltstack.saltapi import SaltAPI
from SaltRuler.glob_config import glob_config

url = glob_config('salt_api','url')
username = glob_config('salt_api','username')
password = glob_config('salt_api','password')
device0 = glob_config('server','dervice0')
salt_master = glob_config('salt_api','master')


# Create your views here.
class UserForm(forms.Form):
    username = forms.CharField(max_length=100)
    password = forms.CharField(widget=forms.PasswordInput())


sapi = SaltAPI(url,username,password)

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
    if username:
        ##saltmaster主机信息
        print salt_master
        LocalData = saltinfo(salt_master)

        ##统计数据中心主机
        LocalData['gz'] = len(Assetmanage.objects.filter(data_center='广州市').values())
        LocalData['sz'] = len(Assetmanage.objects.filter(data_center='深圳市').values())
        LocalData['bj'] = len(Assetmanage.objects.filter(data_center='北京市').values())
        LocalData['qt'] = len(Assetmanage.objects.all().values()) - LocalData['gz'] - LocalData['sz'] - LocalData['bj']

        ##SaltStack状态
        minions = sapi.key_list('manage.status', client='runner')['return'][0]
        minion_down = minions['down']
        minion_online = len(minions['up'])
        if len(minion_down) > 0:
            minion_down = minion_down
        else:
            minion_down = []
        key_status, totle = sapi.minions_key_status()
        saltdata = {'minion_online': minion_online, 'minion_offline': len(minion_down),'minion_down': minion_down}
        # print saltdata
        LocalData['username'] = username
        LocalData['minions_totle'] = totle
        LocalData.update(saltdata)
        LocalData.update(key_status)
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
    return render(request, 'EmpAuth/show_user.html', {'a':user_list})

@login_required
def change(request):
    try:
        info=''

        if request.method == 'POST':
            username = request.POST.get('username')
        elif request.method == 'GET':
            username = request.GET.get('username')
            if username is None:
                username = request.session.get('username')
        oldpass  = request.POST.get('oldpass')
        password = hashlib.sha1(oldpass + username + 'kbson').hexdigest()
        newpass  = request.POST.get('newpass')
        confpass = request.POST.get('confpass')
        if confpass == newpass:
            user=Users.objects.filter(username=username,password=password)
            if user:
                newpasshs = hashlib.sha1(newpass + username + 'kbson').hexdigest()
                Users.objects.update(password=newpasshs).filter(username=username)
        else:
            info = '输入的两次新密码不一致！'
    except Exception as e:
        pass
    # print info
    return render(request, 'EmpAuth/change.html', {'info':info})

@login_required
def useradd(request):
    username = request.session.get('username')
    if username == 'kbson'or username == 'admin':
        info=''
        if request.method == 'POST':
            newuser=request.POST.get('username')
            password1=request.POST.get('password1')
            password2=request.POST.get('password2')
            if password1 == password2:
                user = Users.objects.filter(username=newuser)
                if user:
                    info ="Users %s is Exist!!" % newuser
                else:
                    user=Users()
                    user.username=newuser
                    user.password=password1
                    user.save()
                    info = 'Users %s Add Success!!' % newuser
            else:
                info = '输入的两次密码不一致！'
        return render(request, 'EmpAuth/useradd.html', {'info':info})
    else:
        return HttpResponseRedirect('/EmpAuth')

@login_required
def userdel(request):
    username = request.session.get('username')
    if username == 'kbson'or username == 'admin':
        info=''
        # if request.method == 'POST':
        #     username=request.POST.get('username')
        #     user = Users.objects.filter(username=username)
        #     if  user:
        #         Users.objects.filter(username=username).delete()
        #         info = 'Users %s Delete Success!!' % username
        #     else:
        #         info = "Users %s not Exist!!" % username
        #     return render(request, 'EmpAuth/userdel.html',{'info':info})
        if request.method == 'GET':
            username = request.GET.get('username')
            Users.objects.filter(username=username).delete()
            return HttpResponseRedirect('/EmpAuth/userinfo')
    else:
        return HttpResponseRedirect('/EmpAuth')

