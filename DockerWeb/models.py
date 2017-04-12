from django.db import models

# Create your models here.
class registry(models.Model):
    name = models.CharField(max_length=30)
    address = models.CharField(max_length=100)
    version = models.IntegerField()
    status = models.IntegerField()
    isactive = models.IntegerField()
    auth = models.CharField(max_length=30)