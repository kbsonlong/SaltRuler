# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.shortcuts import render,render_to_response,HttpResponse
from EmpAuth.decorators import login_required
from SaltRuler.glob_config import glob_config
# Create your views here.

@login_required
def gateone(request):
    host_ip = request.GET.get('host',None)
    host_user = request.GET.get('user','root')
    host_port = request.GET.get('port',22)

    if host_port =="":
        host_port=22
        print host_port
    if not host_ip :
        return render_to_response('gateone/404.html', locals(), request)
    else:
        return render_to_response('gateone/gateone.html', locals(), request)

def create_signature(secret, *parts):
    import hmac, hashlib
    hash = hmac.new(secret, digestmod=hashlib.sha1)
    for part in parts:
        hash.update(str(part))
    return hash.hexdigest()

@login_required
def get_auth_obj(request):
    import time, hmac, hashlib, json
    user = request.user.username
    # 安装gateone的服务器以及端口.
    gateone_server = glob_config('gateone','gateone_server')
    # 之前生成的api_key 和secret
    secret  = glob_config('gateone','secret')
    api_key = glob_config('gateone',api_key)

    authobj = {
        'api_key': api_key,
        'upn': "gateone",
        'timestamp': str(int(time.time() * 1000)),
        'signature_method': 'HMAC-SHA1',
        'api_version': '1.0'
    }
    my_hash = hmac.new(secret, digestmod=hashlib.sha1)
    my_hash.update(authobj['api_key'] + authobj['upn'] + authobj['timestamp'])

    authobj['signature'] = my_hash.hexdigest()
    auth_info_and_server = {"url": gateone_server, "auth": authobj}
    valid_json_auth_info = json.dumps(auth_info_and_server)
    print valid_json_auth_info
    #   print valid_json_auth_info
    return HttpResponse(valid_json_auth_info)