#_*_coding:utf-8_*_
from django.db import models
import django
from django.contrib.auth.models import User
import datetime
# Create your models here.




class IDC(models.Model):
    name = models.CharField(max_length=64,unique=True)

    def __unicode__(self):
        return self.name
    class Meta:
        verbose_name = u'IDC'
        verbose_name_plural = u'IDC'

class Department(models.Model):
    name = models.CharField(max_length=64,unique=True)
    def __unicode__(self):
        return self.name
    class Meta:
        verbose_name = u'部门'
        verbose_name_plural = u'部门'

class Hosts(models.Model):
    hostname = models.CharField(max_length=64,unique=True)
    ip_addr = models.GenericIPAddressField(unique=True)
    system_type_choices = (
        ('windows','Windows'),
        ('linux', 'Linux/Unix')
    )
    idc = models.ForeignKey('IDC')
    system_type = models.CharField(choices=system_type_choices,max_length=32,default='linux')
    port = models.IntegerField(default=22)
    enabled = models.BooleanField(default=True,help_text=u'主机若不想被用户访问可以去掉此选项')
    #host_users = models.ForeignKey('HostUsers')
    #host_groups = models.ForeignKey('HostGroups')
    memo = models.CharField(max_length=128,blank=True,null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    def __unicode__(self):
        return '%s(%s)' %(self.hostname,self.ip_addr)
    class Meta:
        verbose_name = u'主机'
        verbose_name_plural = u'主机'
class HostUsers(models.Model):
    auth_method_choices = (('ssh-password',"SSH/Password"),('ssh-key',"SSH/KEY"))
    auth_method = models.CharField(choices=auth_method_choices,max_length=16,help_text=u'如果选择SSH/KEY，请确保你的私钥文件已在settings.py中指定')
    username = models.CharField(max_length=32)
    password = models.CharField(max_length=64,blank=True,null=True,help_text=u'如果auth_method选择的是SSH/KEY,那此处不需要填写..')
    memo = models.CharField(max_length=128,blank=True,null=True)
    def __unicode__(self):
        return '%s(%s)' %(self.username,self.password)
    class Meta:
        verbose_name = u'远程用户'
        verbose_name_plural = u'远程用户'
        unique_together = ('auth_method','password','username')
class BindHosts(models.Model):
    host = models.ForeignKey('Hosts')
    host_user = models.ForeignKey('HostUsers')
    host_group = models.ManyToManyField('HostGroups')
    enabled = models.BooleanField(default=True)
    def __unicode__(self):
        return '%s:%s' %(self.host.hostname,self.host_user.username)
    class Meta:
        unique_together = ("host", "host_user")
        verbose_name = u'主机与远程用户绑定'
        verbose_name_plural = u'主机远程与用户绑定'
    def get_groups(self):
            return ",\n".join([g.name for g in self.host_group.all()])

class HostGroups(models.Model):
    name = models.CharField(max_length=64,unique=True)
    memo = models.CharField(max_length=128,blank=True,null=True)
    def __unicode__(self):
        return self.name
    class Meta:
        verbose_name = u'主机组'
        verbose_name_plural = u'主机组'

class UserProfile(models.Model):
    user = models.OneToOneField(User)
    name = models.CharField(unique=True,max_length=32)
    department = models.ForeignKey('Department',verbose_name=u'部门')
    #user_groups = models.ManyToManyField('PUserGroups') #might use it in the future version
    host_groups = models.ManyToManyField('HostGroups',verbose_name=u'授权主机组')
    bind_hosts = models.ManyToManyField('BindHosts',verbose_name=u'授权主机')
    valid_begin_time = models.DateTimeField(default=django.utils.timezone.now)
    valid_end_time = models.DateTimeField()

    def __unicode__(self):
        return self.name
    class Meta:
        verbose_name = u'CrazyEye账户'
        verbose_name_plural = u'CrazyEye账户'

class SessionTrack(models.Model):

    date = models.DateTimeField(default=django.utils.timezone.now)
    closed = models.BooleanField(default=False)
    def __unicode__(self):
        return '%s' %self.id

class AuditLog(models.Model):
    session = models.ForeignKey(SessionTrack)
    user = models.ForeignKey('UserProfile')
    host = models.ForeignKey('BindHosts')
    action_choices = (
        (0,'CMD'),
        (1,'Login'),
        (2,'Logout'),
        (3,'GetFile'),
        (4,'SendFile'),
        (5,'exception'),
    )
    action_type = models.IntegerField(choices=action_choices,default=0)
    cmd = models.TextField()
    memo = models.CharField(max_length=128,blank=True,null=True)
    date = models.DateTimeField()


    def __unicode__(self):
        return '%s-->%s@%s:%s' %(self.user.user.username,self.host.host_user.username,self.host.host.ip_addr,self.cmd)
    class Meta:
        verbose_name = u'审计日志'
        verbose_name_plural = u'审计日志'



class TaskLog(models.Model):
    start_time = models.DateTimeField(auto_now_add=True)
    end_time = models.DateTimeField(null=True,blank=True)
    task_type_choices = (('cmd',"CMD"),('file_send',"批量发送文件"),('file_get',"批量下载文件"))
    task_type = models.CharField(choices=task_type_choices,max_length=50)
    user = models.ForeignKey('UserProfile')
    hosts = models.ManyToManyField('BindHosts')
    cmd = models.TextField()
    expire_time = models.IntegerField(default=30)
    task_pid = models.IntegerField(default=0)
    note = models.CharField(max_length=100,blank=True,null=True)
    def __unicode__(self):
        return "taskid:%s cmd:%s" %(self.id,self.cmd)
    class Meta:
        verbose_name = u'批量任务'
        verbose_name_plural = u'批量任务'

class TaskLogDetail(models.Model):
    child_of_task = models.ForeignKey('TaskLog')
    bind_host  = models.ForeignKey('BindHosts')
    date = models.DateTimeField(auto_now_add=True) #finished date
    event_log = models.TextField()
    result_choices= (('success','Success'),('failed','Failed'),('unknown','Unknown'))
    result = models.CharField(choices=result_choices,max_length=30,default='unknown')
    note = models.CharField(max_length=100,blank=True)

    def __unicode__(self):
        return "child of:%s result:%s" %(self.child_of_task.id, self.result)
    class Meta:
        verbose_name = u'批量任务日志'
        verbose_name_plural = u'批量任务日志'

class Token(models.Model):
    user = models.ForeignKey(UserProfile)
    host = models.ForeignKey(BindHosts)
    token = models.CharField(max_length=64)
    date = models.DateTimeField(default=django.utils.timezone.now)
    expire = models.IntegerField(default=300)

    def __unicode__(self):
        return '%s : %s' %(self.host.host.ip_addr,self.token)



#test
class Test(models.Model):
    test = models.CharField(max_length=32)
    num = models.IntegerField()

    def __unicode__(self):
        return self.test
