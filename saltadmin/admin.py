from django.contrib import admin
from models import *
from kombu.transport.django import models as kombu_models
# Register your models here.


class MinionGroupModels(admin.ModelAdmin):
    list_display = ('groupname',)
    filter_horizontal = ('minions', )
admin.site.register(SvnProject)
admin.site.register(SaltServer)
admin.site.register(MinionGroup,MinionGroupModels)
admin.site.register(kombu_models.Message)