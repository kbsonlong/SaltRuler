from django.db import models
import hashlib
# Create your models here.
class Users(models.Model):
    username = models.CharField(max_length=50)
    password = models.CharField(max_length=50)

    def save(self,*args,**kwargs):
        self.password = hashlib.sha1(self.password+self.username+'kbson').hexdigest()
        super(Users,self).save(*args,**kwargs)

    def __unicode__(self):
        return self.username


class Author(models.Model):
    name = models.CharField(max_length=100)
    url = models.CharField(max_length=100)
    title = models.CharField(max_length=3)
    birth_date = models.DateField(blank=True, null=True)
    content = models.CharField(max_length=100)
    sites = models.CharField(max_length=100)
    enable_comments = models.CharField(max_length=100)
    registration_required = models.CharField(max_length=100)
    template_name = models.CharField(max_length=100)
