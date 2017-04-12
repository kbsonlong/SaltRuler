#encoding:utf-8
from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'^registry/(?P<server_id>[0-9]+)/$', views.registry_list, name='registry_list'),
    url(r'^registry_add/(?P<server_id>[0-9]+)/$', views.registry_add, name='registry_add'),
    url(r'^registry_del/(?P<server_id>[0-9]+)/$', views.registry_del, name='registry_del'),
    url(r'^registry_image/(?P<reg_id>[0-9]+)/$', views.registry_image, name='registry_image'),
    url(r'^image_tag/(?P<reg_id>[0-9]+)/$', views.image_tag, name='image_tag'),
]