from django.conf.urls import include, url
from . import views


urlpatterns = [
##cobbler_url
    url(r'^profile/$', views.profile, name='profile'),
    url(r'^add_profile/$', views.add_profile, name='add_profile'),
    url(r'^remove_profile/$', views.remove_profile, name='remove_profile'),
    url(r'^system/$', views.system, name='system'),
    url(r'^add_system/$', views.add_system, name='add_system'),
    url(r'^remove_system/$', views.remove_system, name='remove_system'),
    url(r'^distros/$', views.distros, name='distros'),
    url(r'^add_distro/$', views.add_distro, name='add_distro'),
    url(r'^remove_distro/$', views.remove_distro, name='remove_distro'),

]