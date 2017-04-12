# -*- coding: utf8 -*-
from django.shortcuts import render
# Create your views here.
import docker
from registry_api import BASE_REGISTRY_API
from models import registry


c = docker.Client(base_url='tcp://192.168.62.200:2375',version='1.14',timeout=10)


url = 'http://192.168.62.200:5000/'   ##私有仓库地址


b = BASE_REGISTRY_API()


def registry_list(request,server_id):
    reg_list = registry.objects.all()

    contexts = {}
    contexts.update({'reg_list':reg_list})
    return render(request, 'DockerWeb/dockerweb.html', contexts)

def registry_add(request,server_id):
    name = request.POST.get('name')
    address = request.POST.get('address')
    version = request.POST.get('version')
    auth = request.POST.get('auth')
    contexts = {}

    reg = registry()
    reg.name = name
    reg.address = address
    reg.version = version
    reg.auth = auth
    if b.checkStatus(address,version):
        reg.status = '0'
    else:
        reg.status = '1'
    return render(request, 'DockerWeb/dockerweb.html', contexts)
