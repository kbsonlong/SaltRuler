from django.conf.urls import include, url
from . import views

urlpatterns = [
    url(r'^gateone_service/$', views.gateone_service, name='gateone_service'),
    url(r'^get_auth_obj/$', views.get_auth_obj, name='get_auth_obj'),
]