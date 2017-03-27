from django.conf.urls import include, url
from . import views

urlpatterns = [
    url(r'^uploadFile/(?P<server_id>[0-9]+)/$', views.upload_file, name='upload_file'),
    url(r'^downloadFile/(?P<server_id>[0-9]+)/$', views.download_file, name='download_file'),
    url(r'^download/(?P<server_id>[0-9]+)/$', views.download_fun, name='download'),
    url(r'^file_remote/(?P<server_id>[0-9]+)/$', views.file_remote, name='file_remote'),
    url(r'^history/$', views.files_his, name='history'),
]
