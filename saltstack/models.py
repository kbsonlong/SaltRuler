#coding:utf-8
from django.db import models

# Create your models here.
class SaltServer(models.Model):
    Role = (
    ('Master', 'Master'),
    ('Backend', 'Backend'),
    )
    idc = models.CharField(max_length=100,verbose_name=u'所属机房')
    url = models.URLField(max_length=100,verbose_name=u'URL地址')
    username = models.CharField(max_length=50, verbose_name=u'用户名')
    password = models.CharField(max_length=50,verbose_name=u'密码')
    role = models.CharField(choices=Role,max_length=20,default='Master',verbose_name=u'角色')
    def __unicode__(self):
        return u"%s - %s - %s" %(self.idc,self.url,self.role)
    class Meta:
        verbose_name = u'Salt服务器'
        verbose_name_plural = u'Salt服务器列表'

class State(models.Model):
    #命令
    client = models.CharField(max_length=20,blank=True,verbose_name=u'执行方式')
    fun = models.CharField(max_length=50,verbose_name=u'命令')
    arg = models.CharField(max_length=255,blank=True,verbose_name=u'参数')
    tgt_type =  models.CharField(max_length=20,verbose_name=u'目标类型')
    #返回
    jid = models.CharField(blank=True,max_length=50,verbose_name=u'任务号')
    minions = models.CharField(max_length=500,blank=True,verbose_name=u'目标主机')
    result = models.TextField(blank=True,verbose_name=u'返回结果')
    #其他信息
    server = models.ForeignKey(SaltServer,verbose_name=u'所属Salt服务器')
    user = models.CharField(max_length=50,verbose_name=u'操作用户')
    datetime =models.DateTimeField(auto_now_add=True,verbose_name=u'执行时间')
    def __unicode__(self):
        return self.datetime
    class Meta:
        verbose_name = u'部署结果'
        verbose_name_plural = u'部署结果'

class SvnProject(models.Model):
    name = models.CharField(max_length=50,blank=True,verbose_name=u'项目名称')
    salt_server = models.ForeignKey(SaltServer,verbose_name=u'所属Salt服务器')
    host = models.CharField(max_length=50,verbose_name=u'项目主机')
    path = models.CharField(max_length=200,verbose_name=u'项目根路径')
    target = models.CharField(max_length=50,verbose_name=u'项目目录')
    script = models.CharField(max_length=50,verbose_name=u'项目启动脚本')
    url = models.CharField(max_length=200,verbose_name=u'SVN地址')
    username = models.CharField(max_length=40,verbose_name=u'SVN账号')
    password = models.CharField(max_length=40,blank=True,verbose_name=u'SVN密码')
    status = models.CharField(max_length=40,default=u'新建',verbose_name=u'状态')
    create_date=models.DateTimeField(auto_now_add=True,verbose_name=u'创建时间')
    info = models.TextField(max_length=500,blank=True,verbose_name=u'信息')
    def __unicode__(self):
        return u"%s: %s - %s/%s"%(self.name,self.host,self.path,self.target)
    class Meta:
        verbose_name = u'SVN项目'
        verbose_name_plural = u'SVN项目列表'
        unique_together = ("host", "path", "target")


class Minions(models.Model):
    Status = (
    ('Accepted', 'Accepted'),
    ('Unaccepted', 'Unaccepted'),
    ('Rejected', 'Rejected'),
    )
    minion = models.CharField(max_length=50,verbose_name=u'客户端',unique=True)
    saltserver = models.ForeignKey(SaltServer,verbose_name=u'所属Salt服务器')
    status = models.CharField(choices=Status,max_length=20,default='Unknown',verbose_name=u'Key状态')
    create_date=models.DateTimeField(auto_now_add=True,verbose_name=u'创建时间')

    def __unicode__(self):
        return self.minion

    class Meta:
        verbose_name = u'Salt客户端'
        verbose_name_plural = u'Salt客户端列表'

class MinionStatus(models.Model):
    minion = models.OneToOneField(Minions)
    minion_status = models.CharField(max_length=20,verbose_name=u'在线状态')
    # 上次检测时间
    alive_time_last = models.DateTimeField(auto_now=True,null=True)
    # 当前检测时间
    alive_time_now = models.DateTimeField(auto_now=True,null=True)

class MinionGroup(models.Model):
    groupname = models.CharField(u'Minion组',max_length=50,default='default')
    minions = models.ManyToManyField(Minions,verbose_name=u'Minions',blank=True)

    def __unicode__(self):
        return self.groupname

    class Meta:
        verbose_name = u'Minion组'
        verbose_name_plural = u'Minion组'