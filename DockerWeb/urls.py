#encoding:utf-8
from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'^registry/(?P<server_id>[0-9]+)/$', views.registry_list, name='registry_list'),
    url(r'^registry_add/(?P<server_id>[0-9]+)/$', views.registry_add, name='registry_add'),
]