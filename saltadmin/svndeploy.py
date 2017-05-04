# -*- coding: utf-8 -*-
from django.shortcuts import  render
from django.http import JsonResponse
from EmpAuth.decorators import login_required
from saltadmin.models import *
from saltadmin.saltapi import SaltAPI
from deploy.models import files_history
import time

#代码发布
@login_required
def deploy(request,server_id):
    server_list = SaltServer.objects.all()
    contexts = {'server_list': server_list}
    try:
        try:
            salt_server = SaltServer.objects.get(id=server_id)
        except:#id不存在时返回第一个
            salt_server = SaltServer.objects.all()[0]
        project_list = SvnProject.objects.filter(salt_server=salt_server).order_by('host')
        contexts.update({'salt_server': salt_server, 'project_list': project_list})
        return render(request, 'saltstack/svn_deploy.html', contexts)
    except:
        return render(request, 'saltstack/svn.html',contexts )



##签出项目
def checkout(request,server_id):
    server_list = SaltServer.objects.all()
    try:
        salt_server = SaltServer.objects.get(id=server_id)
    except:  # id不存在时返回第一个
        salt_server = SaltServer.objects.all()[0]
    try:
        project_id=request.GET.get('project_id')
    except:
        project_id=''
    project_list=SvnProject.objects.filter(salt_server=salt_server).order_by('host')
    contexts = {'server_list': server_list, 'salt_server': salt_server, 'project_list': project_list}
    if project_list and project_id:
        try:
            sapi = SaltAPI(url=salt_server.url,username=salt_server.username,password=salt_server.password)
            result=sapi.SaltRun(client='runner',fun='manage.status')
            contexts['minions_up']=result['return'][0]['up']
            #刷新页面检测并更新项目状态
            project = SvnProject.objects.filter(id=project_id)[0]

            path=project.path+'/'+project.target

            svn_info=sapi.SaltCmd(client='local',tgt=project.host,fun='svn.info',arg=path,arg1='fmt=dict')['return'][0][project.host][0]

            if isinstance(svn_info,dict):
                if project.url == svn_info['URL']:
                    project.status=u"已发布"
                    project.info=u"最近修改时间：%s\n最近修改版本：%s\n最新版本：%s"%(svn_info["Last Changed Date"][0:20],svn_info["Last Changed Rev"],svn_info["Revision"])
                else:
                    project.status=u"冲突"
                    project.info=u"SVN路径不匹配：\n本地SVN为'%s'\n项目SVN为'%s'"%(svn_info['URL'],project.url)
            else:
                #根路径不存在时创建
                if not sapi.SaltCmd(client='local',tgt=project.host,fun='file.directory_exists',arg=project.path)['return'][0][project.host]:
                    sapi.SaltCmd(client='local',tgt=project.host,fun='file.mkdir',arg=project.path)
                #目录未被版本控制，可能SVN未安装
                if not sapi.SaltCmd(client='local',tgt=project.host,fun='pkg.version',arg='subversion')['return'][0][project.host]:
                    sapi.SaltCmd(client='local',tgt=project.host,fun='pkg.install',arg='subversion')
                #签出项目、获取信息并存入库
                sapi.SaltCmd(client='local',tgt=project.host,fun='svn.checkout',arg=project.path,arg0='target=%s'%project.target,arg1='remote=%s'%project.url,arg2='username=%s'%project.username,arg3='password=%s'%project.password)

                #签出项目后更新项目状态
                svn_info=sapi.SaltCmd(client='local',tgt=project.host,fun='svn.info',arg=path,arg1='fmt=dict')['return'][0][project.host][0]
                project.status=u"已发布"
                project.info = u"最近修改时间：%s\n最近修改版本：%s\n最新版本：%s" % (svn_info["Last Changed Date"][0:20], svn_info["Last Changed Rev"], svn_info["Revision"])
            project.save()
            result = {'ret': True, 'msg': u'检出成功'}


        except Exception as error:
            result = {'ret': False, 'msg': u'错误：项目目录冲突'}
        fh = files_history()
        fh.username = request.session.get('username')
        fh.active = 'svn checkout'
        fh.active_time = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
        fh.remote_server = SvnProject.objects.filter(id=project_id)[0].host
        fh.path = result['msg']
        fh.save()
        return JsonResponse(result, safe=False)


#SVN提交、更新
@login_required
def deploy_fun(request,server_id):
    #SVN功能按钮
    if request.is_ajax() and request.method == 'GET':
        tgt=request.GET.get('tgt','')
        path=request.GET.get('path','').encode("utf-8")
        active=request.GET.get('active','')
        project_id=request.GET.get('project_id','')
        try:
            salt_server = SaltServer.objects.get(id=server_id)
            sapi = SaltAPI(url=salt_server.url,username=salt_server.username,password=salt_server.password)
            if project_id:
                project=SvnProject.objects.get(id=project_id)#指定项目
                path=project.path+'/'+project.target
                tgt=project.host
            else:
                project=None                                #项目不存在
                projects=SvnProject.objects.filter(host=tgt)
                for p in projects:
                    if path.startswith(p.path+'/'+p.target): #项目子目录
                        project=p
            #SvnProject里没有记录时自动创建，但密码需要在后台设置
            if not project:
                svn_info=sapi.SaltCmd(client='local',tgt=tgt,fun='svn.info',arg=path,arg1='fmt=dict')['return'][0][tgt][0]
                if isinstance(svn_info,dict):
                    result = {'ret':False,'msg':u'SVN项目不存在，请在后台页面添加！','add':True}
                else:
                    result = {'ret':False,'msg':u'错误：%s'%svn_info}
            #提交
            elif active=='commit' or active=='update':
                status=sapi.SaltCmd(client='local',tgt=tgt,fun='svn.status',arg=path)['return'][0][tgt]
                for s in status.split('\n'):
                    l=s.split(' ')
                    if l[0]=='?':
                        sapi.SaltCmd(client='local',tgt=tgt,fun='svn.add',arg=path,arg0=path+'/'+l[-1],arg2='username=%s'%project.username,arg3='password=%s'%project.password)
                    elif l[0]=='!':
                        sapi.SaltCmd(client='local',tgt=tgt,fun='svn.remove',arg=path,arg0=path+'/'+l[-1],arg2='username=%s'%project.username,arg3='password=%s'%project.password)
                ci=sapi.SaltCmd(client='local',tgt=tgt,fun='svn.commit',arg=path,arg1='msg=commit from %s'%tgt,arg2='username=%s'%project.username,arg3='password=%s'%project.password)['return'][0][tgt]
                result = {'ret': True, 'msg': u"提交成功！\n%s" % ci}

                #更新（先提交否则会冲突）
                if active=='update':
                    up=sapi.SaltCmd(client='local',tgt=tgt,fun='svn.update',arg=path,arg2='username=%s'%project.username,arg3='password=%s'%project.password)['return'][0][tgt]
                    result = {'ret':True,'msg':u"提交成功！\n%s\n更新成功！\n%s"%(ci,up)}

                ##更新完成后更新项目状态
                svn_info = sapi.SaltCmd(client='local', tgt=project.host, fun='svn.info', arg=path, arg1='fmt=dict')['return'][0][project.host][0]
                if isinstance(svn_info, dict):
                    if project.url == svn_info['URL']:
                        project.status = u"已发布"
                        project.info = u"最近修改时间：%s\n最近修改版本：%s\n最新版本：%s" % (svn_info["Last Changed Date"][0:20], svn_info["Last Changed Rev"], svn_info["Revision"])
                    else:
                        project.status = u"冲突"
                        project.info = u"SVN路径不匹配：\n本地SVN为'%s'\n项目SVN为'%s'" % (svn_info['URL'], project.url)
                project.save()

        except Exception as e:
            result = {'ret':False,'msg':u'错误：%s' % e}

        fh = files_history()
        fh.username = request.session.get('username')
        fh.active = 'svn update'
        fh.active_time = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
        fh.remote_server = SvnProject.objects.filter(id=project_id)[0].host
        fh.path = result['msg']
        fh.save()
        return JsonResponse(result,safe=False)


#启动、关闭应用
@login_required
def service_fun(request,server_id):
    url = SaltServer.objects.values('url').filter(id=server_id)[0]['url']
    username = SaltServer.objects.values('username').filter(id=server_id)[0]['username']
    password = SaltServer.objects.values('password').filter(id=server_id)[0]['password']
    if request.method == 'GET':
        active = request.GET.get('active')
        project_id = request.GET.get('project_id')
        script = SvnProject.objects.values('script').filter(id=project_id)[0]['script']
        tgt = SvnProject.objects.values('host').filter(id=project_id)[0]['host']
        arg = ''
        if active == 'stop':
            arg = script + ' stop'
        elif active == 'start':
            arg = script + ' start'
        elif active == 'status':
            arg = script + ' status'
        elif active == 'restart':
            arg = script + ' restart'
        try:
            sapi = SaltAPI(url=url, username=username, password=password)
            info = sapi.SaltCmd(tgt=tgt, fun='cmd.run', client='local', arg=arg)['return'][0][tgt]
            result = {'ret': True, 'msg': u'%s' % info}
        except Exception as e:
            result = {'error':str(e)}

        fh = files_history()
        fh.username = request.session.get('username')
        fh.active = '应用操作'
        fh.active_time = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
        fh.remote_server = SvnProject.objects.filter(id=project_id)[0].host
        fh.path = result['msg']
        fh.save()
        return JsonResponse(result, safe=False)
