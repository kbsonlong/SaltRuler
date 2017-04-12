# -*- coding: utf8 -*-
from django.shortcuts import render,HttpResponsePermanentRedirect,HttpResponseRedirect
# Create your views here.
import docker
import json

from registry_api import BASE_REGISTRY_API
from models import registry


c = docker.Client(base_url='tcp://192.168.62.200:2375',version='1.14',timeout=10)
url = 'http://192.168.62.200:5001/'   ##私有仓库地址

b = BASE_REGISTRY_API()
b.search_all_repository(url=url,version=2)
def registry_list(request,server_id):
    reg_list = registry.objects.all()
    contexts = {}
    contexts.update({'reg_list':reg_list})
    return render(request, 'DockerWeb/registry.html', contexts)

def registry_add(request,server_id):
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

def registry_del(request,server_id):
    contexts = {}
    if request.method == 'POST':
        name = request.POST.get('name')
        address = request.POST.get('addr')
        version = request.POST.get('version')
        auth = request.POST.get('auth')
        if name and address:
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
        else:
            contexts.update({'error':'name and address is not Null!!'})
    reg_id = request.GET.get('reg_id')
    reg = registry.objects.filter(id=reg_id).delete()
    print reg

    res = {'msg': None, 'code': 0, 'success': True}
    contexts.update(res)
    # return render(request, 'DockerWeb/registry.html', contexts)
    return HttpResponseRedirect('/docker/registry/0/')


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

def image_tag(request,reg_id):
    contexts = {}
    try:
        url = registry.objects.filter(id=reg_id).values('address')[0]['address']
        images_list = b.search_all_repository(url=url, version=2)
        print images_list
        for i in images_list['data']:
            image_name = i['name']
        print image_name
    except:
        url = registry.objects.all().values('address')[0]
        images_list = b.search_all_repository(url=url['address'],version=2)
        reg_id = registry.objects.all().values()[0]['id']
        image_name = images_list['data'][0]['name']

    digest = b.list_image_tags(ImageName=image_name,url=url,version=2)
    contexts.update({'image_name':image_name,'digest':digest,})
    print contexts
    return render(request,'DockerWeb/image_tag.html',contexts)

def image_del(request,reg_id):
    contexts = {}
