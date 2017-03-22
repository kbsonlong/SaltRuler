from django.db import models

# Create your models here.
class Upload(models.Model):
    headImg = models.ImageField(upload_to='./upload/')