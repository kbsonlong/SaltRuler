from django.conf.urls import include, url
from . import views

urlpatterns = [
    # url(r'^$', views.login, name='init_login'),
    url(r'^login/$', views.login, name='login'),
    url(r'^logout/$', views.logout, name='logout'),
    url(r'^$', views.index, name='home'),
    url(r'^userinfo', views.userinfo, name='userinfo'),
    url(r'^change', views.change, name='change'),
    url(r'^useradd', views.useradd, name='useradd'),
    url(r'^userdel', views.userdel, name='userdel'),
]