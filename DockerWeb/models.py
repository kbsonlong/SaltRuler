from django.db import models

# Create your models here.
class registry(models.Model):
    name = models.CharField(max_length=30,unique=True)
    address = models.CharField(max_length=100)
    version = models.IntegerField()
    status = models.IntegerField(null=True,default=0)
    isactive = models.IntegerField(null=True)
    auth = models.CharField(max_length=30,null=True)

    # def __unicode__(self):
    #     return self.address


class docker_server(models.Model):
    name = models.CharField(max_length=30,unique=True)
    address = models.GenericIPAddressField()
    port = models.IntegerField()
