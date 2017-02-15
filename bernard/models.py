from django.db import models
from web.models import BindHosts,HostGroups
from  django_celery_beat.models import PeriodicTask
# Create your models here.





class Plan(models.Model):
    '''store all task plans'''
    name = models.CharField(max_length=64)
    enabled = models.BooleanField(default=True)

    def __str__(self):
        return self.name




class Stage(models.Model):
    'sub steps of one task plan'
    plan = models.ForeignKey(Plan)
    name = models.CharField(max_length=64,default="Default plan")
    order = models.SmallIntegerField(default=1)
    date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return "plan:%s stage:%s"%(self.plan,self.name)

class Job(models.Model):
    "one stage can hold a list of jobs"
    stage = models.ForeignKey(Stage)
    name = models.CharField(max_length=64)
    order = models.SmallIntegerField(default=1)
    task_type_choices = (('sshtask','Run Shell Script'),
                         ('scptask','SSH File Transfer')
                         )
    task_type = models.CharField(choices=task_type_choices,max_length=64)
    enabled = models.BooleanField(default=True)
    date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return "order:%s, stage:%s,  job:%s"%(self.order,self.stage, self.name)


class SSHTask(models.Model):
    """shell script"""
    job = models.OneToOneField("Job")
    bind_hosts = models.ManyToManyField(BindHosts,blank=True)
    host_groups = models.ManyToManyField(HostGroups,blank=True)
    commands = models.TextField(verbose_name="ssh commands")

    def __str__(self):
        return self.commands


class SCPTask(models.Model):
    """file transfer by scp command"""
    job = models.OneToOneField("Job")
    bind_hosts = models.ManyToManyField(BindHosts, blank=True)
    host_groups = models.ManyToManyField(HostGroups, blank=True)
    local_path = models.CharField(max_length=128)
    remote_path = models.CharField(max_length=128)

    def __str__(self):
        return "%s %s"%(self.local_path,self.remote_path)


class ScheduleLog(models.Model):
    """Store Schedule run logs """
    plan = models.ForeignKey("Plan")
    status_choices = ((0,'failed'),(1,'success'),(2,'error'),(3,'running'))
    status = models.SmallIntegerField(choices=status_choices)
    errors = models.TextField(blank=True,null=True)
    start_date = models.DateTimeField(auto_now_add=True)
    end_date = models.DateTimeField(auto_now=True)


