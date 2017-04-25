#!/usr/bin/env python
#coding:utf-8


from EmpAuth.decorators import login_required
from django.shortcuts import render_to_response,render

from cobbler_api import *
# 权限的增删改查

def list(request):

    return render(request, 'cmdb/cobbler_bak.html')

def list2(request):

    return render(request, 'cmdb/cobbler.html')