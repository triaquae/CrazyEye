#_*_coding:utf-8_*_

from web import models
from django import forms

from web.king_admin_base import ModelAdminBase,register


enabled_admins = {} #不要动，所有注册的表都会自动添加到这里



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





class UserAdmin(ModelAdminBase):
    model  = models.UserProfile
    add_form = UserCreationForm

    list_display = ('id','name','email','is_admin')
    filter_horizontal = ('host_groups','bind_hosts')
    readonly_fields = ['password']
    change_page_onclick_fields = {
        'password':['password_change_form','重置密码']
    }
    search_fields = ['email','name']
    list_filter = ['is_admin']


class HostAdmin(ModelAdminBase):
    model = models.Hosts
    list_display = ('id','hostname','ip_addr','port','idc','system_type','enabled','created_at')
    list_per_page = 50
    fk_fields = ['idc',]
    readonly_fields = ['ip_addr',]
    search_fields = ['ip_addr','hostname','idc__name']
    list_filter = ['ip_addr','idc']


class BindHostAdmin(ModelAdminBase):
    model = models.BindHosts
    list_display = ('id','host','host_user')
    fk_fields = ['host','host_user']


class HostGroupAdmin(ModelAdminBase):
    model = models.HostGroups
    list_display = ('name','memo','bind_hosts')
    filter_horizontal = ('bind_hosts',)


class AuditLogAdmin(ModelAdminBase):
    model = models.AuditLog
    list_display = ('id','session','user','host','action_type','cmd','date')
    list_filter = ('session','user','host','action_type','date')
    search_fields = ['user__user__username','host__host__hostname','host__host__ip_addr','cmd']
    list_per_page =10
    choice_fields = ('action_type',)
    fk_fields = ('user','host')
    readable_table = True


class HostUsersAdmin(ModelAdminBase):
    model = models.HostUsers
    list_display = ['auth_method','username','password']

class IDCAdmin(ModelAdminBase):
    model = models.IDC
    list_display = ('id','name')

class SessionAdmin(ModelAdminBase):
    model = models.Session
    list_display = ['id','user', 'bind_host','stay_time','cmd_count','date','closed']
    fk_fields = ['user','bind_host']
    list_filter = ['user','bind_host','date','closed']
    onclick_fields = {
        'id': 'session_record'
    }


    readable_table = True


class TaskLogAdmin(ModelAdminBase):
    model = models.TaskLog
    list_display = ['id','start_time','end_time','task_type','user','cmd','host_nums','success_nums','failed_nums','log_details']
    list_filter = ['user','task_type','start_time']
    fk_fields = ['user']
    readable_table = True

    def log_details(self):
        '''日志详情'''
        ele = '''<a class='btn-link' href='/configure/web_tasklogdetail/?child_of_task=%s'>详情</a> ''' % self.instance.id
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

    readable_table = True

class TaskLogDetailAdmin(ModelAdminBase):
    model = models.TaskLogDetail
    list_display =  ('child_of_task','bind_host','pretty_event_log','result','date','note')
    fk_fields = ('bind_host')
    choice_fields = ('result')
    list_filter = ('child_of_task','result','date')

    readable_table = True
    def pretty_event_log(self):

        return "<pre>%s</pre>" % self.instance.event_log
    pretty_event_log.display_name = "任务结果"
register(enabled_admins,UserAdmin)
register(enabled_admins,HostAdmin)
register(enabled_admins,HostGroupAdmin)
# register(enabled_admins,models.AuditLog,AuditLogAdmin)
register(enabled_admins,HostUsersAdmin)
register(enabled_admins,SessionAdmin)
register(enabled_admins,BindHostAdmin)
register(enabled_admins,TaskLogAdmin)
register(enabled_admins,TaskLogDetailAdmin)
register(enabled_admins,IDCAdmin)