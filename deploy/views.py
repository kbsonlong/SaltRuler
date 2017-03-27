#coding:utf-8
from django.shortcuts import render,HttpResponse
from EmpAuth.decorators import login_required
from SaltRuler.glob_config import glob_config
from saltstack.saltapi import *
from saltstack.models import SaltServer,State
from deploy.models import files_history
import os,time,re
# Create your views here.


upload_dir = glob_config('nginx','upload_dir')
master = glob_config('salt_api','master')
@login_required
def upload_file(request,server_id):
    username = request.session.get('username')
    server_list = SaltServer.objects.all()
    contexts = {'server_list': server_list, 'server_id': server_id}
    try:
        salt_server = SaltServer.objects.get(id=server_id)
    except:  # id不存在时返回第一个
        salt_server = SaltServer.objects.all()[0]
        if not salt_server:
            return render(request, 'deploy/uploadfile.html', contexts)
    contexts.update({'salt_server': salt_server})
    try:
        if request.method == "POST":    # 请求方法为POST时，进行处理
            myFile =request.FILES.get("myfile", None)    # 获取上传的文件，如果没有文件，则默认为None
            server = request.POST.get("server",None)
            dest = request.POST.get('dest','/tmp/')
            print dest
            mdir = request.POST.get('mdir',None)
            mtime = request.POST.get('mtime',None)
            if not myFile:
                contexts.update({'error':u'请选择上传文件!'})
                return render(request, 'deploy/uploadfile.html', contexts)
            if not server:
                contexts.update({'error': u'目标主机不能为空！！'})
                return render(request, 'deploy/uploadfile.html', contexts)

            ##将文件上传到平台所在服务器

            destination = open(os.path.join(upload_dir,myFile.name),'wb+')    # 打开特定的文件进行二进制的写操作
            for chunk in myFile.chunks():      # 分块写入文件
                destination.write(chunk)
            destination.close()

            ##调用saltstack cp.get_url模块进行文件分发
            sapi = SaltAPI(url=salt_server.url, username=salt_server.username, password=salt_server.password)
            nginx_url = 'http://'+ glob_config('nginx','host') +':' + glob_config('nginx','port') + '/' + upload_dir + '/'
            ##文件上传后静态服务地址
            nginx_path = u'%s%s'% (nginx_url ,myFile.name)
            print nginx_path
            ##目标存放绝对路径
            if mtime:
                dest_path=u'dest=/%s/%s%s'% (dest.strip('/'),myFile.name,time.strftime("%Y%m%d%H%M%S", time.localtime()))
            else:
                dest_path = u'dest=/%s/%s' % (dest.strip('/'), myFile.name)

            if mdir:
                command = 'mkdir -p %s' % dest
                sapi.SaltCmd(tgt=server, fun="cmd.run", expr_form='list', arg=command)
            upload_results = sapi.SaltCmd(tgt=server, fun="cp.get_url",expr_form='list', arg=nginx_path, arg1=dest_path)['return'][0]
            #curl - k https: // 192.168.62.200:8000 - H "Accept: application/x-yaml" - H "X-Auth-Token: 69ce7566d2f6680f420cf673ab0d3dc8639ce7aa" - d client = 'local' - d tgt = '192.168.62.200,192.168.62.201' - d fun = 'cp.get_url' - d arg = 'http://192.168.62.1/upload/along_logo.png' - d arg = '/tmp/along_logo.png'
            # upload_results = {'return': [{'192.168.62.200': '/tmp/along_logo.png', '192.168.62.201': '/tmp/along_logo.png'}]}['return'][0]
            # print server.split(',')
            contexts.update({'success': u'%s 上传成功!' % upload_results})

            fh=files_history()
            fh.username=username
            fh.active='upload'
            fh.path=dest_path.strip('dest=')
            fh.remote_server = server
            fh.active_time=time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
            fh.url = nginx_path
            fh.save()
    except Exception as e:
        contexts.update({'error':e})
    return render(request, 'deploy/uploadfile.html', contexts)

@login_required
def download_file(request,server_id):
    username = request.session.get('username')
    server_list = SaltServer.objects.all()
    contexts = {'server_list': server_list, 'server_id': server_id}
    try:
        salt_server = SaltServer.objects.get(id=server_id)
    except:  # id不存在时返回第一个
        salt_server = SaltServer.objects.all()[0]
        if not salt_server:
            pass
    contexts.update({'salt_server': salt_server})
    try:
        if request.method == 'POST':
            # print server_id
            server = request.POST.get("server", None)
            # print server
            dest = request.POST.get('dest')
            # print dest
            if not server:
                contexts.update({'error': u'目标主机不能为空！！'})
            elif not dest:
                contexts.update({'error': u'下载文件不能为空！！'})
            else:
                sapi = SaltAPI(url=salt_server.url, username=salt_server.username, password=salt_server.password)
                ##检索目录或者文件
                arg = 'ls %s' % dest
                # print arg
                files_list = sapi.SaltCmd(tgt=server, fun="cmd.run",expr_form='list', arg=arg)['return'][0][server]
                # print files_list
                if 'No such file or directory' in files_list:
                    contexts.update({'error': u'文件或目录不存在'})
                else:
                    nginx_url = 'http://' + glob_config('nginx', 'host') + ':' + glob_config('nginx','port') + '/' + upload_dir + '/'
                    contexts.update({'files_list':files_list.split(),'nginx_url':nginx_url,'server':server,'dest':dest})
                return render(request,'deploy/download_file.html',contexts)

    except Exception as e:
        pass
    return render(request,'deploy/download_file.html',contexts)

def download_fun(request,server_id):
    username = request.session.get('username')
    server_list = SaltServer.objects.all()
    contexts = {'server_list': server_list, 'server_id': server_id}
    try:
        salt_server = SaltServer.objects.get(id=server_id)
    except:  # id不存在时返回第一个
        salt_server = SaltServer.objects.all()[0]
        if not salt_server:
            pass
    contexts.update({'salt_server': salt_server})
    try:
        file = request.POST.get('file')
        server = request.POST.get("server", None)
        dest = request.POST.get('dest')
        print file
        print server
        print dest
        arg=dest+file
        sapi = SaltAPI(url=salt_server.url, username=salt_server.username, password=salt_server.password)
        result = sapi.SaltCmd(tgt=server,fun='cp.push',expr_form='list',arg=arg)
        print result
        roots=sapi.SaltRun(client='wheel', fun='file_roots.list_roots')['return'][0]['data']['return']['base'][0].keys()[0]
        print roots
        arg1='mkdir -p %s/temp && mv %s/minions/%s/files%s%s %s/temp/%s' % (roots,glob_config('salt_api','cachedir'),server,dest,file,roots,file)
        print arg1
        sapi.SaltCmd(tgt=master,fun='cmd.run',arg=arg1)
        arg2='salt://%s %s/%s/%s' % (file,os.path.dirname(os.path.dirname(os.path.abspath(__file__))),upload_dir,file)
        print arg2
        sapi.SaltCmd(tgt=glob_config('nginx','host'),fun='cp.get_file',makedirs=True,arg=arg2)
        nginx_url = 'http://' + glob_config('nginx', 'host') + ':' + glob_config('nginx','port') + '/' + upload_dir + '/'
        contexts.update({'nginx_url': nginx_url, 'server': server, 'dest': dest})

    except Exception as e:
        pass
    return render(request, 'deploy/download_file.html', contexts)





@login_required
def files_his(request):
    his_list = files_history.objects.all().order_by('-active_time')     ##active_time操作时间倒序
    contexts = {'his_list': his_list}
    return render(request, 'deploy/history.html', contexts)
