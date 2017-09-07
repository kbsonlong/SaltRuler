# -*- coding: utf8 -*-
from django.shortcuts import render,HttpResponsePermanentRedirect,HttpResponseRedirect
# Create your views here.
import docker
from EmpAuth.decorators import login_required

from registry_api import BASE_REGISTRY_API
from models import registry
from remote_api import Dockerapi




url = 'http://192.168.62.200:5001/'   ##私有仓库地址

b = BASE_REGISTRY_API()


##查看镜像仓库
@login_required
def registry_list(request):
    reg_list = registry.objects.all()
    contexts = {}
    for i in reg_list:
        status =  b.checkStatus(i.address,version=i.version)
        if status == True:
            i.status=0
        else:
            i.status=1
        i.save()
    contexts.update({'reg_list':reg_list})
    return render(request, 'DockerWeb/registry.html', contexts)

##添加镜像仓库
@login_required
def registry_add(request):
    contexts = {}
    res = {}
    if request.method == 'POST':
        name = request.POST.get('name')
        address = request.POST.get('addr')
        version = request.POST.get('version')
        auth = request.POST.get('auth')
        if name and address:
            try:
                registry.objects.get(name=name)
                res = {'error': u'%s 已经存在' % name}
            except:
                reg = registry()
                reg.name = name
                reg.address = address
                reg.version = version
                reg.auth = auth
                if b.checkStatus(address,version):
                    reg.status = '0'
                else:
                    reg.status = '1'
                reg.save()
                res = {'success': u'%s 添加成功' % name}
        else:
            contexts.update({'error':'name and address is not Null!!'})
    print res
    contexts.update(res)
    return render(request, 'DockerWeb/registry_add.html', contexts)


##删除镜像仓库
@login_required
def registry_del(request):
    contexts = {}
    reg_id = request.GET.get('reg_id')
    reg = registry.objects.filter(id=reg_id).delete()
    res = {'msg': None, 'code': 0, 'success': True}
    contexts.update(res)
    return HttpResponseRedirect('/docker/registry/')


##获取所有镜像
@login_required
def registry_image(request,reg_id):
    contexts = {}
    try:
        url = registry.objects.filter(id=reg_id).values('address')[0]['address']
        images_list = b.search_all_repository(url=url, version=2)
    except:
        url = registry.objects.all().values('address')[0]
        images_list = b.search_all_repository(url=url['address'],version=2)
        reg_id = registry.objects.all().values()[0]['id']
    contexts.update({'images':images_list['data'],'reg_id':reg_id,'reg_url':url})
    return render(request, 'DockerWeb/image.html', contexts)


##获取某个镜像所有标签
@login_required
def image_tag(request,reg_id):
    contexts = {"reg_id":reg_id}
    image_name=request.GET.get('imagename')
    try:
        url = registry.objects.filter(id=reg_id).values('address')[0]['address']
    except:
        url = registry.objects.all().values('address')[0]['address']
    digest = b.list_image_tags(ImageName=image_name,url=url,version=2)
    L=[]
    for i in digest['data']:
        d = {"image_name":image_name, "digest": i.values()[0],"tag":i.keys()[0]}
        L.append(d)
    contexts.update({"image_tags":L,'image_name':image_name})
    return render(request,'DockerWeb/image_tag.html',contexts)


##删除镜像站不支持v2
@login_required
def image_del(request,reg_id):
    contexts = {}
    imagename = request.GET.get('imagename')
    try:
        url = registry.objects.filter(id=reg_id).values()[0]['address']
        version = registry.objects.filter(id=reg_id).values()[0]['version']
    except:
        url = registry.objects.all().values()[0]['address']
        version = registry.objects.all().values()[0]['version']

    print imagename,url,version
    print b.delete_image(ImageName=imagename,url=url)
    return HttpResponseRedirect('/docker/registry_image/%s/' % reg_id)


##查询镜像标签信息
@login_required
def tag_list(request,reg_id):
    contexts = {}
    imagename = request.GET.get('imagename')
    tag = request.GET.get('tag')
    try:
        url = registry.objects.filter(id=reg_id).values()[0]['address']
        version = registry.objects.filter(id=reg_id).values()[0]['version']
    except:
        url = registry.objects.all().values()[0]['address']
        version = registry.objects.all().values()[0]['version']
    imageId = b.from_image_tag_getId(imagename,tag,url,version)
    tag_info = b.get_imageId_info(ImageId=imageId,url=url,version=version,tag=tag,ImageName=imagename)
    contexts.update({'data':tag_info['data']})
    return render(request, 'DockerWeb/tag_info.html', contexts)





