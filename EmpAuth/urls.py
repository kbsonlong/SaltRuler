from django.conf.urls import include, url
from . import views

urlpatterns = [
    url(r'^login/$', views.login, name='login'),
    url(r'^logout/$', views.logout, name='logout'),
    url(r'^$', views.index, name='home'),
    url(r'^userinfo', views.userinfo, name='userinfo'),
    url(r'^change/(?P<id>[0-9]+)/$', views.change, name='change'),
    url(r'^useradd', views.useradd, name='useradd'),
    url(r'^userdel/(?P<id>[0-9]+)/$', views.userdel, name='userdel'),
]