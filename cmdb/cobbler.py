#!/usr/bin/env python
#coding:utf-8


from EmpAuth.decorators import login_required
from django.shortcuts import render_to_response,render,HttpResponseRedirect
from cmdb.cobbler_api import CobblerAPI
import time


capi=CobblerAPI("http://192.168.62.110/cobbler_api","cobbler","cobbler")

def distros(request):
    contexts = {"distros":[]}
    distros = capi.get_distro()
    for i in distros:
        ctime = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(i['ctime']))
        contexts["distros"].append({"name":i["name"],"kernel":i["kernel"],"ctime":ctime})
    print contexts
    return render(request,'cmdb/cobbler_distro.html',contexts)

def add_distro(request):
    contexts = {}
    if request.method == "POST":
        name = request.POST.get('name')
        url = request.POST.get('url')
        print url
        capi.add_distro(name,url)
    return render(request,'cmdb/cobbler_add_distro.html')

@login_required
def profile(request):
    contexts = {'profiles':[]}
    profiles =  capi.get_profile()
    for i in profiles:
        ctime = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(i['ctime']))
        contexts['profiles'].append({'name': i['name'], 'kickstart': i['kickstart'], 'distro': i['distro'], 'owners': i['owners'],'ctime': ctime})
    return render(request, 'cmdb/cobbler_profile.html', contexts)

@login_required
def add_profile(request):
    contexts = {'distros':[]}
    distro = capi.get_distro()
    for i in distro:
        contexts['distros'].append(i['name'])
    if request.method == "POST":
        name = request.POST.get('name')
        distro = request.POST.get('distro')
        ks = request.POST.get('ks')
        profiles =  capi.create_profile(name,distro,ks)
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
    contexts = {'systems':[]}
    systems = capi.get_systems()
    for i in systems:
        ctime = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(int(i['ctime'])))
        contexts['systems'].append({'hostname':i['hostname'],'profile':i['profile'],'ctime':ctime,'ip_address':i['interfaces']['eth0']['ip_address'],'mac_address':i['interfaces']['eth0']['mac_address'],'netmask':i['interfaces']['eth0']['netmask']})
    return render(request,'cmdb/cobbler_system.html',contexts)


@login_required
def add_system(request):
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
    return render(request,'cmdb/cobbler_add_system.html',contexts)


