from django.conf.urls import include, url
from . import views

urlpatterns = [
    url(r'^gateone/$', views.gateone, name='gateone'),
    url(r'^get_auth_obj/$', views.get_auth_obj, name='get_auth_obj'),
]