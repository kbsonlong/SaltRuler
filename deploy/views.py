#coding:utf-8
import os
import time
from django.shortcuts import render
from EmpAuth.decorators import login_required
from SaltRuler.glob_config import glob_config
from deploy.models import files_history
from saltadmin.models import SaltServer
from saltadmin.saltapi import *
# Create your views here.


upload_dir = glob_config('nginx','upload_dir')
master = glob_config('salt_api','master')
@login_required
def upload_file(request,server_id):
    username = request.session.get('username')
    server_list = SaltServer.objects.all()
    contexts = {'server_list': server_list, 'server_id': server_id}
    try:
        try:
            salt_server = SaltServer.objects.get(id=server_id)
            print salt_server
        except Exception as e:  # id不存在时返回第一个
            salt_server = SaltServer.objects.all()[0]
            if not salt_server:
                contexts.update({'error':u'请先添加SaltServer API'})
    except Exception as e:
        return render(request, 'deploy/uploadfile.html', contexts)
    contexts.update({'salt_server': salt_server})
    try:
        if request.method == "POST":    # 请求方法为GET时，进行处理
            myFile =request.FILES.get("myfile", None)    # 获取上传的文件，如果没有文件，则默认为None
            server = request.POST.get("server",None)
            dest = request.POST.get('dest','/tmp/')
            mdir = request.POST.get('mdir',None)
            mtime = request.POST.get('mtime',None)
            nginx_path = ''
            sapi = SaltAPI(url=salt_server.url, username=salt_server.username, password=salt_server.password)
            minions = sapi.key_list('manage.status', client='runner')['return'][0]
            for s in server.split(','):
                if s not in minions['up']:
                    contexts.update({'error': u'目标主机 %s不存在或者已离线' % s})
                    action_result = contexts['error']
                    ###将操作过程写入数据库
                    fh = files_history()
                    fh.username = username
                    fh.active = 'upload'
                    fh.path = action_result
                    fh.remote_server = server
                    fh.active_time = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
                    fh.url = nginx_path
                    fh.save()
                    return render(request, 'deploy/uploadfile.html', contexts)
            dir_result = sapi.SaltCmd(client='local', tgt=server, fun='file.directory_exists', arg=dest, expr_form='list')['return'][0]
            if not myFile:
                contexts.update({'error':u'请选择上传文件!'})
                action_result = u'请选择上传文件!'
            elif not server:
                contexts.update({'error': u'目标主机不能为空！！'})
                action_result = u'目标主机不能为空！!'
            elif not dir_result[s]:
                contexts.update({'error': u'目标主机 %s 目录不存在，请选择创建目录！！' % s})
                action_result = contexts['error']
            else:
                ##将文件上传到平台所在服务器
                destination = open(os.path.join(upload_dir,myFile.name),'wb+')    # 打开特定的文件进行二进制的写操作
                for chunk in myFile.chunks():      # 分块写入文件
                    destination.write(chunk)
                destination.close()

                ##调用saltstack cp.get_url模块进行文件分发
                nginx_url = 'http://'+ glob_config('nginx','host') +':' + glob_config('nginx','port') + '/' + upload_dir + '/'
                ##文件上传后静态服务地址
                nginx_path = u'%s%s'% (nginx_url ,myFile.name)
                ##目标存放绝对路径
                dest_path = u'dest=/%s/%s' % (dest.strip('/'), myFile.name)

                ##备份文件
                if mtime:
                    file_path =u'/%s/%s'  % (dest.strip('/'),myFile.name)
                    file_result = sapi.SaltCmd(client='local', tgt=server, fun='file.file_exists', arg=file_path)['return'][0][server]
                    if file_result:
                        command = 'mv %s %s%s' % (file_path,file_path,time.strftime("%Y%m%d%H%M%S", time.localtime()))
                        sapi.SaltCmd(tgt=server, fun="cmd.run", expr_form='list', arg=command)
                if mdir:
                    command = 'mkdir -p %s' % dest
                    sapi.SaltCmd(tgt=server, fun="cmd.run", expr_form='list', arg=command)
                upload_results = sapi.SaltCmd(tgt=server, fun="cp.get_url", arg=nginx_path, arg1=dest_path,expr_form='list')['return'][0]
                #curl - k https: // 192.168.62.200:8000 - H "Accept: application/x-yaml" - H "X-Auth-Token: 69ce7566d2f6680f420cf673ab0d3dc8639ce7aa" - d client = 'local' - d tgt = '192.168.62.200,192.168.62.201' - d fun = 'cp.get_url' - d arg = 'http://192.168.62.1/upload/along_logo.png' - d arg = '/tmp/along_logo.png'
                # upload_results = {'return': [{'192.168.62.200': '/tmp/along_logo.png', '192.168.62.201': '/tmp/along_logo.png'}]}['return'][0]

                contexts.update({'success': u'%s 上传成功!' % upload_results})
                action_result = contexts['success']
                os.remove('%s/%s' % (upload_dir,myFile.name))
                print "移除后 : %s" % os.listdir(upload_dir)

            ###将操作过程写入数据库
            fh=files_history()
            fh.username=username
            fh.active='upload'
            fh.path=action_result
            fh.remote_server = server
            fh.active_time=time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
            fh.url = nginx_path
            fh.save()

    except Exception as e:
        print e
        contexts.update({'error':e})
    return render(request, 'deploy/uploadfile.html', contexts)

@login_required
def download_file(request,server_id):
    username = request.session.get('username')
    server_list = SaltServer.objects.all()
    contexts = {'server_list': server_list, 'server_id': server_id}
    try:
        try:
            salt_server = SaltServer.objects.get(id=server_id)
        except:  # id不存在时返回第一个
            salt_server = SaltServer.objects.all()[0]
            if not salt_server:
                contexts.update({'error': u'请先添加SaltServer API'})
    except Exception as e:
        return render(request,'deploy/download_file.html',contexts)
    contexts.update({'salt_server': salt_server})
    sapi = SaltAPI(url=salt_server.url, username=salt_server.username, password=salt_server.password)
    server = ''
    try:
        if request.method == 'POST':
            server = request.POST.get("server", None)
            dest = request.POST.get('dest')
            dir_result = sapi.SaltCmd(client='local', tgt=server, fun='file.directory_exists', arg=dest)['return'][0][server]
            file_result = sapi.SaltCmd(client='local', tgt=server, fun='file.file_exists', arg=dest)['return'][0][server]
            if not server:
                contexts.update({'error': u'目标主机不能为空！！'})
                action_result = u'目标主机不能为空！！'
            elif not dest:
                contexts.update({'error': u'下载文件不能为空！！'})
                action_result = u'下载文件不能为空！！'
            elif not dir_result and not file_result :
                contexts.update({'error': u'%s 文件或目录不存在' % dest})
                action_result =  u'%s 文件或目录不存在' % dest
            else:
                ##检索目录或者文件
                arg = 'ls %s' % dest
                files_list = sapi.SaltCmd(tgt=server, fun="cmd.run", expr_form='list', arg=arg)['return'][0][server]
                nginx_url = 'http://' + glob_config('nginx', 'host') + ':' + glob_config('nginx','port') + '/' + upload_dir + '/'
                contexts.update({'files_list': files_list.split(), 'nginx_url': nginx_url, 'server': server, 'dest': dest})
                action_result = arg
            fh = files_history()
            fh.username = username
            fh.active = 'download list'
            fh.path = action_result
            fh.remote_server = server
            fh.active_time = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
            fh.save()


    except Exception as e:
        contexts.update({'error':u'目标主机和目标路径不能为空！！'})


    return render(request,'deploy/download_file.html',contexts)

##点击下载按钮时触发调用download_fun动作
def download_fun(request,server_id):
    username = request.session.get('username')
    server_list = SaltServer.objects.all()
    contexts = {'server_list': server_list, 'server_id': server_id}
    try:
        salt_server = SaltServer.objects.get(id=server_id)
    except:  # id不存在时返回第一个
        salt_server = SaltServer.objects.all()[0]
        if not salt_server:
            contexts.update({'error': u'请先添加SaltServer API'})
    contexts.update({'salt_server': salt_server})
    sapi = SaltAPI(url=salt_server.url, username=salt_server.username, password=salt_server.password)
    try:
        files = request.POST.get('myfile')
        server = request.POST.get("server", None)
        dest = request.POST.get('dest')
        file_path=dest + '/' + files
        dir_result = sapi.SaltCmd(client='local', tgt=server, fun='file.directory_exists', arg=file_path)['return'][0][server]
        if dir_result:
            arg = 'ls %s' % file_path
            files_list = sapi.SaltCmd(tgt=server, fun="cmd.run", expr_form='list', arg=arg)['return'][0][server]
            contexts.update({'files_list': files_list.split(),  'server': server, 'dest': file_path})
            action_result = arg
        else:
            ftp_url = 'http://' + glob_config('ftp', 'host') + ':' + glob_config('ftp','port')
            command = 'python /tmp/ftp_client.py %s %s' % (ftp_url,file_path)
            code =  sapi.SaltCmd(tgt=server, fun='cmd.run', expr_form='list', arg=command)['return'][0][server]
            if int(code) == 200:
                contexts.update({'code':code})
            nginx_url = 'http://' + glob_config('nginx', 'host') + ':' + glob_config('nginx','port') + '/' + upload_dir + '/'
            contexts.update({'files':files,'nginx_url': nginx_url, 'server': server, 'dest': dest})
            action_result = file_path
            # os.remove(upload_dir + '/' + files)
        fh = files_history()
        fh.username = username
        fh.active = 'download'
        fh.path = action_result
        fh.remote_server = server
        fh.active_time = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
        fh.save()
    except Exception as e:
        contexts.update({'error': e})
    return render(request, 'deploy/download_file.html', contexts)


@login_required
def files_his(request):
    his_list = files_history.objects.all().order_by('-id')     ##id倒序
    contexts = {'his_list': his_list}
    return render(request, 'deploy/history.html', contexts)


