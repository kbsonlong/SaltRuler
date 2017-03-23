#coding:utf-8
from django.shortcuts import render,HttpResponse
from EmpAuth.decorators import login_required
from SaltRuler.glob_config import glob_config
from saltstack.saltapi import *
from saltstack.models import SaltServer,State
from django import forms
import os
# Create your views here.

@login_required
def upload_file(request,server_id):
    server_list = SaltServer.objects.all()
    try:
        salt_server = SaltServer.objects.get(id=server_id)
    except:  # id不存在时返回第一个
        salt_server = SaltServer.objects.all()[0]
    contexts = {'server_list': server_list, 'salt_server': salt_server,'server_id':server_id}
    if not salt_server:
        return render(request,'deploy/file.html',contexts)
    if request.method == "POST":    # 请求方法为POST时，进行处理
        myFile =request.FILES.get("myfile", None)    # 获取上传的文件，如果没有文件，则默认为None
        server = request.POST.get("server",None)
        dest = request.POST.get('dest','/tmp/')
        if not myFile:
            contexts.update({'error':u'请选择上传文件!'})
            return render(request, 'deploy/file.html', contexts)
        if not server:
            contexts.update({'error': u'目标主机不能为空！！'})
            return render(request, 'deploy/file.html', contexts)

        ##将文件上传到平台所在服务器
        upload_dir = glob_config('nginx','upload_dir')
        destination = open(os.path.join(upload_dir,myFile.name),'wb+')    # 打开特定的文件进行二进制的写操作
        for chunk in myFile.chunks():      # 分块写入文件
            destination.write(chunk)
        destination.close()

        ##调用saltstack cp.get_url模块进行文件分发
        sapi = SaltAPI(url=salt_server.url, username=salt_server.username, password=salt_server.password)
        nginx_url = 'http://'+ glob_config('nginx','host') +':' + glob_config('nginx','port') + '/' + upload_dir + '/'
        ##文件上传后静态服务地址
        path = nginx_url + myFile.name
        ##目标存放绝对路径
        arg1=u'dest='+dest+myFile.name
        upload_results = sapi.SaltCmd(tgt=server, fun="cp.get_url",expr_form='list', arg=path, arg1=arg1)['return'][0]
        for upload_result in upload_results:
            contexts.update({'success': u'%s 上传成功!' % upload_result})
    return render(request,'deploy/file.html',contexts)