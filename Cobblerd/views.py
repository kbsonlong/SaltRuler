#!/usr/bin/env python
#coding:utf-8


import time

from django.shortcuts import render,HttpResponseRedirect

from Cobblerd.cobbler_api import CobblerAPI
from EmpAuth.decorators import login_required
from SaltRuler.glob_config import glob_config

c_url = glob_config("cobbler_api","url")
c_username = glob_config("cobbler_api","username")
c_password = glob_config("cobbler_api","password")

s_url = glob_config("salt_api","url")
s_username = glob_config("salt_api","username")
s_password = glob_config("salt_api","password")

# capi=CobblerAPI(c_url,c_username,c_password)

@login_required
def distros(request):
    try:
        contexts = {"distros":[]}
        distros = capi.get_distro()
        for i in distros:
            ctime = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(i['ctime']))
            contexts["distros"].append({"name":i["name"],"kernel":i["kernel"],"ctime":ctime})
    except Exception as error:
        contexts = {'error':error}
    return render(request, 'cmdb/cobbler_distro.html', contexts)

@login_required
def add_distro(request):
    contexts = {}
    try:
        if request.method == "POST":
            name = request.POST.get('name')
            path = request.POST.get('path')
            arch = request.POST.get('arch')
            breed = request.POST.get('breed')
            os_version = request.POST.get('os_version')
            distros =  capi.get_distro()
            for i in distros:
                distro_name = "%s-%s" %(name,arch)
                if distro_name == i['name']:
                    contexts.update({"error": "%s 已经存在" % distro_name})
                    return render(request, 'cmdb/cobbler_add_distro.html', contexts)
            capi.add_distro(name,path,arch,breed,os_version)
            return HttpResponseRedirect('/cmdb/distros/')
    except Exception as e:
        contexts.update({"error":e})
    return render(request, 'cmdb/cobbler_add_distro.html', contexts)

@login_required
def remove_distro(request):
    try:
        contexts = {}
        distro_name = request.GET.get('distro_name')
        ret = capi.remove_distro(distro_name)
        print ret
        if ret:
            return HttpResponseRedirect('/cmdb/distros/')
    except Exception as error:
        contexts = {'error':error}
    return render(request, 'cmdb/cobbler_distro.html')


@login_required
def profile(request):
    try:
        contexts = {'profiles':[]}
        name =   request.GET.get('profile_name')
        profiles =  capi.get_profile()
        print profiles
        if name:
            pass

        for i in profiles:
            ctime = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(i['ctime']))
            contexts['profiles'].append({'name': i['name'], 'kickstart': i['kickstart'], 'distro': i['distro'], 'owners': i['owners'],'ctime': ctime})
    except Exception as error:
        contexts = {'error':error}
    return render(request, 'cmdb/cobbler_profile.html', contexts)

@login_required
def add_profile(request):
    try:
        contexts = {'distros':[]}
        distro = capi.get_distro()
        for i in distro:
            contexts['distros'].append(i['name'])
        if request.method == "POST":
            name = request.POST.get('name')
            distro = request.POST.get('distro')
            ks = request.POST.get('ks')
            profiles =  capi.create_profile(name,distro,ks)
    except Exception as error:
        contexts = {'error':error}
    return render(request, 'cmdb/cobbler_add_profile.html', contexts)

@login_required
def remove_profile(request):
    name = request.GET.get('profile_name')
    ret = capi.remove_profile(name)
    if ret['result']:
        return HttpResponseRedirect('/cmdb/profile/')
    return render(request, 'cmdb/cobbler_profile.html')

@login_required
def system(request):
    try:
        contexts = {'systems':[]}
        systems = capi.get_systems()
        for i in systems:
            ctime = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(int(i['ctime'])))
            contexts['systems'].append({'hostname':i['hostname'],'profile':i['profile'],'ctime':ctime,'ip_address':i['interfaces']['eth0']['ip_address'],'mac_address':i['interfaces']['eth0']['mac_address'],'netmask':i['interfaces']['eth0']['netmask']})
    except Exception as error:
        contexts = {'error':error}
    return render(request, 'cmdb/cobbler_system.html', contexts)


@login_required
def add_system(request):
    try:
        contexts={'profiles':[]}
        profiles = capi.get_profile()
        for i in profiles:
            contexts['profiles'].append({'name': i['name']})
        if request.method == "POST":
            hostname = request.POST.get('hostname')
            ip = request.POST.get('ip_addr')
            mac = request.POST.get('mac')
            profile = request.POST.get('profile')
            gateway = request.POST.get('gateway')
            netmask = request.POST.get('netmask')
            try:
                capi.add_system(hostname,ip,mac,profile,gateway,netmask)
            except Exception as e:
                print e
            return HttpResponseRedirect('/cmdb/system')
    except Exception as error:
        contexts = {'error':error}
    return render(request, 'cmdb/cobbler_add_system.html', contexts)


@login_required
def remove_system(request):
    try:
        contexts = {}
        name = request.GET.get('system_name')
        ret = capi.remove_system(name)
        print ret
    except Exception as error:
        contexts = {'error':error}
    return HttpResponseRedirect('/cmdb/system/')

