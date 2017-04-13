#encoding:utf-8
from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'^registry/$', views.registry_list, name='registry_list'),
    url(r'^registry_add/$', views.registry_add, name='registry_add'),
    url(r'^registry_del/$', views.registry_del, name='registry_del'),
    url(r'^registry_image/(?P<reg_id>[0-9]+)/$', views.registry_image, name='registry_image'),
    url(r'^image_del/(?P<reg_id>[0-9]+)/$', views.image_del, name='image_del'),
    url(r'^image_tag/(?P<reg_id>[0-9]+)/$', views.image_tag, name='image_tag'),
    url(r'^tag_list/(?P<reg_id>[0-9]+)/$', views.tag_list, name='tag_list'),

]