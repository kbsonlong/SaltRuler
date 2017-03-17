from django.conf.urls import url

from saltstack import views
from saltstack.svndeploy import *

urlpatterns = [
    url(r'^key_list/(?P<server_id>[0-9]+)/$', views.key_list, name='key_list'),
    url(r'^cmd_exec/(?P<server_id>[0-9]+)/$', views.cmd_exec, name='cmd_exec'),
    url(r'^state_exec/(?P<server_id>[0-9]+)/$', views.state_exec, name='state_exec'),
    url(r'^deploy/(?P<server_id>[0-9]+)/$', deploy, name='deploy'),
    url(r'^deploy_fun/(?P<server_id>[0-9]+)/$', deploy_fun, name='deploy_fun'),
    url(r'^service_fun/(?P<server_id>[0-9]+)/$', service_fun, name='service_fun'),
    url(r'^checkout/(?P<server_id>[0-9]+)/$', checkout, name='checkout'),
]