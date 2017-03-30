from django.db import models
from django.core.urlresolvers import reverse

# Create your models here.
class Assetmanage(models.Model):
    asset_num =  models.CharField(max_length = 50,unique=True)
    type = models.CharField(max_length = 50)
    server_ip = models.CharField(max_length = 20,unique=True)
    remote_ip = models.CharField(max_length = 20)
    data_center = models.CharField(max_length = 50)
    room_num = models.CharField(max_length = 20)
    rack_num = models.CharField(max_length = 20)
    system_type = models.CharField(max_length = 20,default='-')
    cputype_num = models.CharField(max_length = 20,default='-')
    disksize_num = models.CharField(max_length = 20,default='-')
    memsize_num = models.CharField(max_length = 20,default='-')
    disk_raid = models.CharField(max_length = 20,default='-')
    card_type_num = models.CharField(max_length = 20,default='-')
    power_num = models.CharField(max_length = 20,default='-')
    service_num = models.CharField(max_length = 50,unique=True)
    buy_time = models.CharField(max_length = 50,default='-')
    expiration_time = models.CharField(max_length = 50,default='-')
    note = models.CharField(max_length = 200,default='-')

    def __unicode__(self):
        return self.asset_num

    def get_host_url(self):
        return reverse('host_list', args=(self.server_ip,))

class Hostinfo(models.Model):
    host_ip =  models.ForeignKey(Assetmanage,related_name='asset_set')
    local_ip = models.CharField(max_length = 20,unique=True)
    app = models.CharField(max_length = 50,default='-')
    host_note = models.CharField(max_length = 200,default='-')

    def __unicode__(self):
        return self.local_ip


class Servers(models.Model):
    local_ip = models.CharField(max_length = 20,unique=True)
    server_status = models.IntegerField(default=0)
    hostname = models.CharField(max_length=50)
    OS = models.CharField(max_length=100)
    Cpu_type = models.CharField(max_length=200)
    Cpus = models.IntegerField(20)
    Mem = models.IntegerField(100)
    minion_id = models.CharField(max_length=50)
    minion_accept = models.IntegerField(10)
    minion_unaccept = models.IntegerField(10)
    minion_reject = models.IntegerField(10)