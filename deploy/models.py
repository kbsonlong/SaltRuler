from django.db import models

# Create your models here.
class files_history(models.Model):
    username = models.CharField(max_length = 30)
    active = models.CharField(max_length=30)
    path = models.CharField(max_length=600)
    active_time = models.DateTimeField()
    remote_server = models.CharField(max_length = 300)
    url = models.CharField(max_length = 300)

    def __unicode__(self):
        return self.username

class Upload(models.Model):
    headImg = models.ImageField(upload_to='./upload/')