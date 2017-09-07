from django.shortcuts import render,HttpResponsePermanentRedirect,HttpResponseRedirect
from EmpAuth.decorators import login_required
from remote_api import Dockerapi

@login_required
def container_list(request,host,port):
    client = Dockerapi(host,port)
    images=client.AllImages()
    contexts={'images':images}
    return render(request,'DockerWeb/image.html',contexts)