"""fourthgen URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.8/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Add an import:  from blog import urls as blog_urls
    2. Add a URL to urlpatterns:  url(r'^blog/', include(blog_urls))
"""
from django.conf.urls import include, url
from django.contrib import admin


urlpatterns = [
    url(r'^admin/', include(admin.site.urls)),
    url(r'^saltstack/', include('saltstack.urls', namespace="saltstack")),
    url(r'^deploy/', include('deploy.urls', namespace="deploy")),
    url(r'^docker/', include('DockerWeb.urls', namespace="dockerweb")),
    url(r'^zabbix/', include('ZABBIX.urls', namespace="zabbix")),
    url(r'^cmdb/', include('cmdb.urls', namespace="cmdb")),
    url(r'^EmpAuth/', include('EmpAuth.urls', namespace="empauth")),
    url(r'^gateone/', include('gateone.urls', namespace="gateone")),
    url(r'^cobbler/', include('Cobblerd.urls', namespace="cobbler")),
    url(r'^$', include('EmpAuth.urls')),
]
