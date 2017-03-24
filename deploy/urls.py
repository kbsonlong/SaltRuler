from django.conf.urls import include, url
from . import views

urlpatterns = [
    url(r'^uploadFile/(?P<server_id>[0-9]+)/$', views.upload_file, name='upload_file'),
    url(r'^history/$', views.files_his, name='history'),
]
