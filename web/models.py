#_*_coding:utf-8_*_
from django.db import models
import django
from django.contrib.auth.models import User
import datetime
from web import auth
# Create your models here.




class IDC(models.Model):
    name = models.CharField(max_length=64,unique=True)

    def __str__(self):
        return self.name
    class Meta:
        verbose_name = 'IDC'
        verbose_name_plural = 'IDC'

class Department(models.Model):
    name = models.CharField(max_length=64,unique=True)
    def __str__(self):
        return self.name
    class Meta:
        verbose_name = '部门'
        verbose_name_plural = '部门'

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
    enabled = models.BooleanField(default=True,help_text='主机若不想被用户访问可以去掉此选项')
    #host_users = models.ForeignKey('HostUsers')
    #host_groups = models.ForeignKey('HostGroups')
    memo = models.CharField(max_length=128,blank=True,null=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return '%s(%s)' %(self.hostname,self.ip_addr)

    class Meta:
        verbose_name = '主机'
        verbose_name_plural = '主机'

class HostUsers(models.Model):
    auth_method_choices = (('ssh-password',"SSH/Password"),('ssh-key',"SSH/KEY"))
    auth_method = models.CharField(choices=auth_method_choices,max_length=16,help_text='如果选择SSH/KEY，请确保你的私钥文件已在settings.py中指定')
    username = models.CharField(max_length=32)
    password = models.CharField(max_length=64,blank=True,null=True,help_text='如果auth_method选择的是SSH/KEY,那此处不需要填写..')
    memo = models.CharField(max_length=128,blank=True,null=True)

    def __str__(self):
        return '%s(%s)' %(self.username,self.password)

    class Meta:
        verbose_name = '远程用户'
        verbose_name_plural = '远程用户'
        unique_together = ('auth_method','password','username')

class BindHosts(models.Model):
    host = models.ForeignKey('Hosts')
    host_user = models.ForeignKey('HostUsers',verbose_name="远程用户")

    enabled = models.BooleanField(default=True)

    def __str__(self):
        return '%s:%s' %(self.host.hostname,self.host_user.username)

    class Meta:
        unique_together = ("host", "host_user")
        verbose_name = '主机与远程用户绑定'
        verbose_name_plural = '主机远程与用户绑定'

    # def get_groups(self):
    #         return ",\n".join([g.name for g in self.host_group.all()])

class HostGroups(models.Model):
    name = models.CharField(max_length=64,unique=True)
    memo = models.CharField(max_length=128,blank=True,null=True)
    bind_hosts = models.ManyToManyField('BindHosts',blank=True)
    def __str__(self):
        return self.name
    class Meta:
        verbose_name = '主机组'
        verbose_name_plural = '主机组'


#class UserProfile(AbstractBaseUser):
class UserProfile(auth.AbstractBaseUser,auth.PermissionsMixin):
    email = models.EmailField(
        verbose_name='email address',
        max_length=255,
        unique=True,
    )
    is_active = models.BooleanField(default=True)
    is_admin = models.BooleanField(default=False)
    is_staff = models.BooleanField(
        verbose_name='staff status',
        default=False,
        help_text='Designates whether the user can log into this admin site.',
    )
    name = models.CharField(max_length=32)
    #token = models.CharField('token', max_length=128,default=None,blank=True,null=True)
    department = models.ForeignKey('Department',verbose_name='部门',blank=True,null=True)
    host_groups = models.ManyToManyField('HostGroups',verbose_name='授权主机组',blank=True)
    bind_hosts = models.ManyToManyField('BindHosts',verbose_name='授权主机',blank=True)


    memo = models.TextField('备注', blank=True,null=True,default=None)
    date_joined = models.DateTimeField(blank=True,null=True, auto_now_add=True)
    valid_begin_time = models.DateTimeField(default=django.utils.timezone.now,help_text="yyyy-mm-dd HH:MM:SS")
    valid_end_time = models.DateTimeField(blank=True,null=True,help_text="yyyy-mm-dd HH:MM:SS")


    USERNAME_FIELD = 'email'
    #REQUIRED_FIELDS = ['name','token','department','tel','mobile','memo']
    REQUIRED_FIELDS = ['name']

    def get_full_name(self):
        # The user is identified by their email address
        return self.email

    def get_short_name(self):
        # The user is identified by their email address
        return self.email

    def __str__(self):              # __str__ on Python 2
        return self.email

    # def has_perm(self, perm, obj=None):
    #     "Does the user have a specific permission?"
    #     # Simplest possible answer: Yes, always
    #     return True
    def has_perms(self, perm, obj=None):
        "Does the user have a specific permission?"
        # Simplest possible answer: Yes, always
        return True
    def has_module_perms(self, app_label):
        "Does the user have permissions to view the app `app_label`?"
        # Simplest possible answer: Yes, always
        return True

    # @property
    # def is_staff(self):
    #     "Is the user a member of staff?"
    #     # Simplest possible answer: All admins are staff
    #     return self.is_admin
    @property
    def is_superuser(self):
        "Is the user a member of staff?"
        # Simplest possible answer: All admins are staff
        return self.is_admin

    class Meta:
        verbose_name = '用户信息'
        verbose_name_plural = u"用户信息"

    def __str__(self):
        return self.name

    objects = auth.UserManager()

    
    class Meta:
        verbose_name = 'CrazyEye账户'
        verbose_name_plural = 'CrazyEye账户'

        permissions = (
            ('web_access_dashboard', '可以访问 审计主页'),
            ('web_batch_cmd_exec', '可以访问 批量命令执行页面'),
            ('web_batch_batch_file_transfer', '可以访问 批量文件分发页面'),
            ('web_config_center', '可以访问 堡垒机配置中心'),
            ('web_config_items', '可以访问 堡垒机各配置列表'),
            ('web_table_change_page', '可以访问 堡垒机各配置项修改页'),
            ('web_table_change', '可以修改 堡垒机各配置项'),
        )

#
# class UserProfile(models.Model):
#     user = models.OneToOneField(User)
#     name = models.CharField(unique=True,max_length=32)
#     department = models.ForeignKey('Department',verbose_name='部门')
#     #user_groups = models.ManyToManyField('PUserGroups') #might use it in the future version
#     host_groups = models.ManyToManyField('HostGroups',verbose_name='授权主机组',blank=True)
#     bind_hosts = models.ManyToManyField('BindHosts',verbose_name='授权主机',blank=True)
#     valid_begin_time = models.DateTimeField(default=django.utils.timezone.now)
#     valid_end_time = models.DateTimeField()
#
#     def __str__(self):
#         return self.name
#     class Meta:
#         verbose_name = 'CrazyEye账户'
#         verbose_name_plural = 'CrazyEye账户'

class SessionTrack(models.Model):

    date = models.DateTimeField(auto_now_add=True)
    closed = models.BooleanField(default=False)
    def __str__(self):
        return '%s' %self.id


class Session(models.Model):
    '''生成用户操作session id '''
    user = models.ForeignKey('UserProfile')
    bind_host = models.ForeignKey('BindHosts')
    tag = models.CharField(max_length=128,default='n/a')
    closed = models.BooleanField(default=False)
    cmd_count = models.IntegerField(default=0) #命令执行数量
    stay_time = models.IntegerField(default=0, help_text="每次刷新自动计算停留时间",verbose_name="停留时长(seconds)")
    date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return '<id:%s user:%s bind_host:%s' % (self.id,self.user.email,self.bind_host.host)
    class Meta:
        verbose_name = '审计日志'
        verbose_name_plural = '审计日志'


#Deprecated
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
    cmd = models.TextField(blank=True,null=True)
    memo = models.CharField(max_length=128,blank=True,null=True)
    date = models.DateTimeField()


    def __str__(self):
        return '%s-->%s@%s:%s' %(self.user.email,self.host.host_user.username,self.host.host.ip_addr,self.cmd)
    class Meta:
        verbose_name = '审计日志'
        verbose_name_plural = '审计日志'



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

    def __str__(self):
        return "taskid:%s cmd:%s" %(self.id,self.cmd)

    class Meta:
        verbose_name = '批量任务'
        verbose_name_plural = '批量任务'

class TaskLogDetail(models.Model):
    child_of_task = models.ForeignKey('TaskLog')
    bind_host  = models.ForeignKey('BindHosts')
    date = models.DateTimeField(auto_now_add=True) #finished date
    event_log = models.TextField()
    result_choices= (('success','Success'),('failed','Failed'),('unknown','Unknown'))
    result = models.CharField(choices=result_choices,max_length=30,default='unknown')
    note = models.CharField(max_length=100,blank=True)

    def __str__(self):
        return "child of:%s result:%s" %(self.child_of_task.id, self.result)
    class Meta:
        verbose_name = '批量任务日志'
        verbose_name_plural = '批量任务日志'

class Token(models.Model):
    user = models.ForeignKey(UserProfile)
    host = models.ForeignKey(BindHosts)
    token = models.CharField(max_length=64)
    date = models.DateTimeField(default=django.utils.timezone.now)
    expire = models.IntegerField(default=300)

    def __str__(self):
        return '%s : %s' %(self.host.host.ip_addr,self.token)


