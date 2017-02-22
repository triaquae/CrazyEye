#_*_coding:utf-8_*_

from django import forms

from kingadmin.admin_base import BaseKingAdmin,site
from web import models
from bernard import models as bernard_models

from django_celery_beat import  models as celery_beat_models



class UserCreationForm(forms.ModelForm):
    """A form for creating new users. Includes all the required
    fields, plus a repeated password."""
    password1 = forms.CharField(label='Password', widget=forms.PasswordInput)
    password2 = forms.CharField(label='Password confirmation', widget=forms.PasswordInput)

    class Meta:
        model = models.UserProfile
        fields = ('email','name')

    def clean_password2(self):
        # Check that the two password entries match
        password1 = self.cleaned_data.get("password1")
        password2 = self.cleaned_data.get("password2")
        if password1 and password2 and password1 != password2:
            raise forms.ValidationError("Passwords don't match")
        if len(password1) < 6:
            raise forms.ValidationError("Passwords takes at least 6 letters")
        return password2

    def save(self, commit=True):
        # Save the provided password in hashed format
        user = super(UserCreationForm, self).save(commit=False)
        user.set_password(self.cleaned_data["password1"])
        if commit:
            user.save()
        return user





class UserAdmin(BaseKingAdmin):
    add_form = UserCreationForm

    list_display = ('id','name','email','is_admin')
    filter_horizontal = ('user_permissions','groups','host_groups','bind_hosts')
    readonly_fields = ['password']

    search_fields = ['email','name']
    list_filter = ['is_admin']


class HostAdmin(BaseKingAdmin):
    list_display = ('id','hostname','ip_addr','port','idc','system_type','enabled','created_at')
    list_per_page = 50
    #readonly_fields = ['ip_addr',]
    search_fields = ['ip_addr','hostname','idc__name']
    list_filter = ['ip_addr','idc']


class BindHostAdmin(BaseKingAdmin):
    list_display = ('id','host','host_user')


class HostGroupAdmin(BaseKingAdmin):
    list_display = ('name','memo','bind_hosts')
    filter_horizontal = ('bind_hosts',)


class AuditLogAdmin(BaseKingAdmin):
    list_display = ('id','session','user','host','action_type','cmd','date')
    list_filter = ('session','user','host','action_type','date')
    search_fields = ['user__user__username','host__host__hostname','host__host__ip_addr','cmd']
    list_per_page =10
    choice_fields = ('action_type',)
    readonly_table = True


class HostUsersAdmin(BaseKingAdmin):
    list_display = ['auth_method','username','password']

class IDCAdmin(BaseKingAdmin):
    list_display = ('id','name')

class SessionAdmin(BaseKingAdmin):
    list_display = ['id','user', 'bind_host','stay_time','cmd_count','date','closed']
    list_filter = ['user','bind_host','date','closed']
    onclick_fields = {
        'id': 'session_record'
    }


    readonly_table = True


class TaskLogAdmin(BaseKingAdmin):
    list_display = ['id','start_time','end_time','task_type','user','cmd','host_nums','success_nums','failed_nums','log_details']
    list_filter = ['user','task_type','start_time']
    readonly_table = True

    def log_details(self):
        '''日志详情'''
        ele = '''<a class='btn-link' href='/kingadmin/web/tasklogdetail/?child_of_task=%s'>详情</a> ''' % self.instance.id
        return ele



    def host_nums(self):
        '''主机数量'''
        #print("customize field enroll",self.instance.hosts.select_related())
        return '''%s ''' % (self.instance.hosts.select_related().count())
    host_nums.display_name = "主机数量"


    def success_nums(self):
        return "%s" % self.instance.tasklogdetail_set.select_related().filter(result='success').count()
    success_nums.display_name = "成功数"


    def failed_nums(self):
        return "%s" % self.instance.tasklogdetail_set.select_related().filter(result='failed').count()
    failed_nums.display_name = '失败数'

    readonly_table = True

class TaskLogDetailAdmin(BaseKingAdmin):
    list_display =  ('child_of_task','bind_host','pretty_event_log','result','date','note')
    fk_fields = ('bind_host')
    choice_fields = ('result')
    list_filter = ('child_of_task','result','date')

    readonly_table = True
    def pretty_event_log(self):

        return "<pre>%s</pre>" % self.instance.event_log
    pretty_event_log.display_name = "任务结果"



class PlanAdmin(BaseKingAdmin):
    list_display = ('name','enabled')


class ScheduleAdmin(BaseKingAdmin):
    list_display = ('plan', 'date')

class StageAdmin(BaseKingAdmin):
    list_display = ('plan', 'name','order','date')

class JobAdmin(BaseKingAdmin):
    list_display = ('stage', 'name','task_type','enabled','order','date')

class SSHTaskAdmin(BaseKingAdmin):
    list_display = ('id','job', 'commands')
    filter_horizontal = ('bind_hosts','host_groups')

class SCPTaskAdmin(BaseKingAdmin):
    list_display = ('job', 'local_path','remote_path')
    filter_horizontal = ('bind_hosts', 'host_groups')




class CrontabAdmin(BaseKingAdmin):
    pass #list_display = ('id',)

class PeriodicTaskAdmin(BaseKingAdmin):
    pass
class IntervalAdmin(BaseKingAdmin):
    pass

site.register(models.UserProfile,UserAdmin)
site.register(models.Hosts,HostAdmin)
site.register(models.BindHosts,BindHostAdmin)
site.register(models.HostGroups,HostGroupAdmin)
site.register(models.HostUsers,HostUsersAdmin)
site.register(models.IDC,IDCAdmin)
site.register(models.Session,SessionAdmin)
site.register(models.TaskLog,TaskLogAdmin)
site.register(models.TaskLogDetail,TaskLogDetailAdmin)

site.register(bernard_models.Plan,PlanAdmin)
site.register(bernard_models.Stage,StageAdmin)
site.register(bernard_models.Job,JobAdmin)
site.register(bernard_models.SSHTask,SSHTaskAdmin)
site.register(bernard_models.SCPTask,SCPTaskAdmin)


site.register(celery_beat_models.CrontabSchedule, CrontabAdmin)
site.register(celery_beat_models.IntervalSchedule, IntervalAdmin)
site.register(celery_beat_models.PeriodicTask,PeriodicTaskAdmin )
# site.register(bernard_models.Schedule,ScheduleAdmin)



