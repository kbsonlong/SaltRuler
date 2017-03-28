#coding:utf-8
import os
import time
from django.shortcuts import render
from EmpAuth.decorators import login_required
from SaltRuler.glob_config import glob_config
from deploy.models import files_history
from saltstack.models import SaltServer
from saltstack.saltapi import *


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
            mdir = request.POST.get('mdir',None)
            mtime = request.POST.get('mtime',None)
            dest_path = 'dest='
            nginx_path = ''
            sapi = SaltAPI(url=salt_server.url, username=salt_server.username, password=salt_server.password)
            dir_result = sapi.SaltCmd(client='local', tgt=server, fun='file.directory_exists', arg=dest)['return'][0]

            if not myFile:
                contexts.update({'error':u'请选择上传文件!'})
                dest_path = u'dest=请选择上传文件!'
                # return render(request, 'deploy/uploadfile.html', contexts)
            elif not server:
                contexts.update({'error': u'目标主机不能为空！！'})
                dest_path = u'dest=目标主机不能为空！!'
                # return render(request, 'deploy/uploadfile.html', contexts)
            elif not dir_result[server]:
                contexts.update({'error': u'目标主机目录不存在，请选择创建目录！！'})
                dest_path = u'dest=目标主机目录不存在，请选择创建目录!'
                # return render(request, 'deploy/uploadfile.html', contexts)
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
    print contexts
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
    sapi = SaltAPI(url=salt_server.url, username=salt_server.username, password=salt_server.password)
    try:
        if request.method == 'POST':
            server = request.POST.get("server", None)
            dest = request.POST.get('dest')
            dir_result = sapi.SaltCmd(client='local', tgt=server, fun='file.directory_exists', arg=dest)['return'][0][server]
            if not server:
                contexts.update({'error': u'目标主机不能为空！！'})
                action_result = u'目标主机不能为空！！'
            elif not dest:
                contexts.update({'error': u'下载文件不能为空！！'})
                action_result = u'下载文件不能为空！！'
            elif not dir_result :
                contexts.update({'error': u'文件或目录不存在'})
                action_result = u'文件或目录不存在！！'
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
        contexts.update({'error': e})

    return render(request,'deploy/download_file.html',contexts)

##点击下载按钮是触发调用download_fun动作
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
def file_remote(request, server_id):
    server_list = SaltServer.objects.all()
    try:
        salt_server = SaltServer.objects.get(id=server_id)
    except:  # id不存在时返回第一个
        salt_server = SaltServer.objects.all()[0]
    context = {'server_list': server_list, 'salt_server': salt_server}
    if request.method == 'GET':
        tgt=request.GET.get('server')
        path=request.GET.get('dest','').replace('//','/').encode('utf-8')
        if path!='/':
            path=path.rstrip('/')
        dir=None
        if tgt and path:
            try:
                #目录存在时返回目录列表
                sapi = SaltAPI(url=salt_server.url,username=salt_server.username,password=salt_server.password)
                result = sapi.SaltCmd(client='local',tgt=tgt,fun='file.directory_exists',arg=path)['return'][0][tgt]
                print result
                if result:
                    path_str=path.split('/')
                    if path_str[-1]=='..':#返回上层
                        if len(path_str)>3:
                            dir='/'.join(path_str[0:-2])
                        else:
                            dir='/'
                    else:
                        dir=path
                    svn_info=sapi.SaltCmd(client='local',tgt=tgt,fun='svn.info',arg=dir,arg1='fmt=dict')['return'][0][tgt][0]
                    if isinstance(svn_info,dict):
                        context['svn']={'URL':svn_info['URL'],'Revision':svn_info['Revision'],'LastChangedRev':svn_info['Last Changed Rev'],'LastChangeDate':svn_info["Last Changed Date"][0:20]}
                #文件存在时，返回文件内容，加上文件格式、大小限制
                elif sapi.SaltCmd(client='local',tgt=tgt,fun='file.file_exists',arg=path)['return'][0][tgt]:
                    if os.path.splitext(path)[1] in glob_config('ftp','FILE_FORMAT'):
                        stats=sapi.SaltCmd(client='local',tgt=tgt,fun='file.stats',arg=path)['return'][0][tgt]
                        if stats['size'] <= 1024000000:
                            content=sapi.SaltCmd(client='local',tgt=tgt,fun='cmd.run',arg='cat '+path)['return'][0][tgt]
                            context['content']=content
                            context['stats']=stats
                        else:
                            context['error']=u"文件大小超过1G，拒绝访问！"
                    else:
                        context['error']=u"文件格式不允许访问，请检查setting.FILE_FORMAT！"
                    path_str=path.rstrip('/').split('/')
                    if len(path_str)>2:
                        dir='/'.join(path_str[0:-1])
                    else:
                        dir='/'
                    svn_info=sapi.SaltCmd(client='local',tgt=tgt,fun='svn.info',arg=dir,arg1='fmt=dict',arg2='targets=%s'%path_str[-1])['return'][0][tgt][0]
                    if isinstance(svn_info,dict):
                        context['svn']={'URL':svn_info['URL'],'Revision':svn_info['Revision'],'LastChangedRev':svn_info['Last Changed Rev'],'LastChangeDate':svn_info["Last Changed Date"][0:20]}
                else:
                    context['error']=u"目标不存在或者不是目录或文件！"

                # 根据路径获取列表
                if dir:
                    dirs = sapi.SaltCmd(client='local',tgt=tgt,fun='file.readdir',arg=dir)['return'][0][tgt]
                    try:
                        dirs.remove('.')
                        dirs.remove('.svn')
                    except:pass
                    if dir=='/':
                        dirs.remove('..')
                    # result = {'dirs':sorted(dirs) ,'type':'dir','pdir':path}
                    context['dir']=dir
                    context['dir_list']=dirs
                    context['tgt']=tgt
                # return JsonResponse(result,safe=False)
            except Exception as e:
                context['error']=e
    return render(request, 'deploy/download_file.html', context)






@login_required
def files_his(request):
    his_list = files_history.objects.all().order_by('-active_time')     ##active_time操作时间倒序
    contexts = {'his_list': his_list}
    return render(request, 'deploy/history.html', contexts)
