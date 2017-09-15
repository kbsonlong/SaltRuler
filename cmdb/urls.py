from django.conf.urls import include, url
from . import views
#from . import cobbler

urlpatterns = [
    url(r'^asset_table/$', views.asset_table, name='asset_table'),
    url(r'^asset_add/$', views.asset_add, name='asset_add'),
    url(r'^asset_del/$', views.asset_del, name='asset_del'),
    url(r'^asset_update/$', views.asset_update, name='asset_update'),
    url(r'^host_table/$', views.host_table, name='host_table'),
    url(r'^host_add_html/$', views.host_add_html, name='host_add_html'),
    url(r'^host_update_html/$', views.host_update_html, name='host_update_html'),
    url(r'^host_del_html/$', views.host_del_html, name='host_del_html'),
    url(r'^host_list/(?P<server_ip>[^/]+)/$', views.host_list, name='host_list'),
    url(r'^server_collect/(?P<server_id>[^/]+)/$', views.server_collect, name='server_collect'),


]