from django.db import models

# Create your models here.
class registry(models.Model):
    name = models.CharField(max_length=30,unique=True)
    address = models.CharField(max_length=100)
    version = models.IntegerField()
    status = models.IntegerField(null=True)
    isactive = models.IntegerField(null=True)
    auth = models.CharField(max_length=30,null=True)

    def __unicode__(self):
        return self.address