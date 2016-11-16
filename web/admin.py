#_*_coding:utf-8_*_
from django.contrib import admin
from django import forms
from django.contrib.auth.admin import UserAdmin


from web import models

from django.shortcuts import render_to_response,render,HttpResponse

from django.contrib.admin.views.decorators import staff_member_required

from django.conf.urls import include, url
# Register your models here.


from django.contrib.auth.admin import UserAdmin
from django.contrib.auth.forms import ReadOnlyPasswordHashField

from django.contrib.auth import  forms as auth_form

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
        return password2

    def save(self, commit=True):
        # Save the provided password in hashed format
        user = super(UserCreationForm, self).save(commit=False)
        user.set_password(self.cleaned_data["password1"])
        if commit:
            user.save()
        return user


class UserChangeForm(forms.ModelForm):
    """A form for updating users. Includes all the fields on
    the user, but replaces the password field with admin's
    password hash display field.
    """
    password = ReadOnlyPasswordHashField(label="Password",
        help_text=("Raw passwords are not stored, so there is no way to see "
                    "this user's password, but you can change the password "
                    "using <a href=\"password/\">this form</a>."))

    class Meta:
        model = models.UserProfile
        fields = ('email','password','is_active', 'is_admin')

    def clean_password(self):
        # Regardless of what the user provides, return the initial value.
        # This is done here, rather than on the field, because the
        # field does not have access to the initial value
        return self.initial["password"]


class UserProfileAdmin(UserAdmin):
    # The forms to add and change user instances
    form = UserChangeForm
    add_form = UserCreationForm

    # The fields to be used in displaying the User model.
    # These override the definitions on the base UserAdmin
    # that reference specific fields on auth.User.
    list_display = ('id','email','is_admin','is_active')
    list_filter = ('is_admin',)
    fieldsets = (
        (None, {'fields': ('email','name', 'password')}),
        ('Personal info', {'fields': ('department','memo')}),
        #('API TOKEN info', {'fields': ('token',)}),
        ('Permissions', {'fields': ('is_active','is_admin')}),
        ('有权限操作的主机或主机组', {'fields': ('bind_hosts','host_groups')}),
        ('账户有效期', {'fields': ('valid_begin_time','valid_end_time')}),
    )
    # add_fieldsets is not a standard ModelAdmin attribute. UserAdmin
    # overrides get_fieldsets to use this attribute when creating a user.
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('email',  'password1', 'password2','is_active','is_admin')}
        ),
    )
    search_fields = ('email',)
    ordering = ('email',)
    filter_horizontal = ('host_groups','bind_hosts')


class HostAdmin(admin.ModelAdmin):
    search_fields = ('hostname','ip_addr')
    list_display = ('hostname','ip_addr','port','system_type','enabled')


# class BindHostInline(admin.TabularInline):
#     model = models.BindHosts.host_group.through
#
#     readonly_fields = ['hostname']
#     def hostname(self, instance):
#         return '%s(%s)' %(instance.bindhosts.host.hostname,instance.bindhosts.host.ip_addr)
#     hostname.short_description = 'row name'


class HostUserAdmin(admin.ModelAdmin):
    list_display = ('auth_method','username')

class BindHostAdmin(admin.ModelAdmin):
    list_display = ('host','host_user')
    list_filter = ('host','host_user')
    raw_id_fields = ("host",'host_user')

    # def get_urls(self):
    #
    #     urls = super(BindHostAdmin, self).get_urls()
    #     my_urls =("",url(r"^multi_add/$", self.multi_add)
    #     )
    #     #print(my_urls,urls)
    #     return my_urls + urls


    #@staff_member_required
    def multi_add(self, request):
        if request.user.is_superuser:
            import admin_custom_view
            err = {}
            result = None
            chosen_data = {}
            if request.method == 'POST':
                form_obj = admin_custom_view.BindHostsMultiHandle(request)
                if form_obj.is_valid():
                    form_obj.save()
                    result = form_obj.result
                else:
                    err = form_obj.err_dic
                chosen_data = form_obj.clean_data

            #else:
            host_users = models.HostUsers.objects.all()
            hosts = models.Hosts.objects.all()
            host_groups = models.HostGroups.objects.all()
            return render(request,'admin/web/BindHosts/multi_add.html',{
                'user':request.user,
                'host_users':host_users,
                'host_groups':host_groups,
                'hosts':hosts,
                'err':err,
                'chosen_data': chosen_data,
                'result': result
            })
        else:
            return HttpResponse("Only superuser can access this page!")

class HostGroupAdmin(admin.ModelAdmin):
    list_display = ('name',)
    # inlines = [
    #     BindHostInline,
    # ]

# class UserProfileAdmin(admin.ModelAdmin):
#     list_display = ('email','name','department','valid_begin_time','valid_end_time')
#     filter_horizontal = ('host_groups','bind_hosts')


class AuditLogAdmin(admin.ModelAdmin):
    list_display = ('id','session','user','host','action_type','cmd','date')
    list_filter = ('session','user','host','action_type','date')
    search_fields = ['user__user__username','host__host__hostname','host__host__ip_addr','cmd']
    actions = ['make_published']
    list_per_page =20
    choice_fields = ('action_type',)
    fk_fields = ('user','host')

    colored_fields = {
        'action_type':{'Login':'#83e277','Logout':'orange'}
    }

    def get_actions(self, request):
        actions = super(AuditLogAdmin, self).get_actions(request)

        if 'delete_selected' in actions:
            del actions['delete_selected']
        return actions

    def make_published(self, request, queryset):
        rows_deleted = models.AuditLog.objects.all()
        #if rows_updated == 1:
        message_bit = "1 story was"
        #else:
        #    message_bit = "%s stories were" % rows_updated
        self.message_user(request, "%s successfully marked as published." % message_bit)
    make_published.short_description = '删除3个月以前的审计日志' #

    def suit_row_attributes(self, obj, request):
        css_class = {
            1: 'success',
            2: 'warning',
            5: 'error',
        }.get(obj.action_type)
        if css_class:
            return {'class': css_class, 'data': obj.action_type}


    def has_add_permission(self, request, obj=None):
        return False

    def has_delete_permission(self, request, obj=None):
        return False
    #readonly_fields = models.AuditLog._meta.get_all_field_names()

class TaskLogAdmin(admin.ModelAdmin):
    list_display = ('id','start_time','end_time','task_type','user','cmd','total_task','success_task','failed_task','unknown_task','expire_time')
    list_filter = ('task_type','user','start_time')
    #readonly_fields = models.TaskLog._meta.get_all_field_names()
    def has_add_permission(self, request, obj=None):
        return False

    def has_delete_permission(self, request, obj=None):
        return False

    def total_task(self, obj):
        return obj.tasklogdetail_set.select_related().count()
    def success_task(self, obj):
        return obj.tasklogdetail_set.select_related().filter(result='success').count()
    def failed_task(self, obj):
        return obj.tasklogdetail_set.select_related().filter(result='failed').count()
    def unknown_task(self, obj):
        data = "<a href='#'> %s </a> " % obj.tasklogdetail_set.select_related().filter(result='unknown').count()

        return data
    unknown_task.allow_tags = True

class TaskLogDetailAdmin(admin.ModelAdmin):
    list_display = ('child_of_task','bind_host','result','date')
    list_filter = ('child_of_task','result','date')
    def suit_row_attributes(self, obj, request):
        css_class = {
            'success': 'success',
            'unknown': 'warning',
            'failed': 'error',
        }.get(obj.result)
        if css_class:
            return {'class': css_class, 'data': obj.result}
    def has_add_permission(self, request, obj=None):
        return False

    def has_delete_permission(self, request, obj=None):
        return False
    #readonly_fields = models.TaskLogDetail._meta.get_all_field_names()


class TokenAdmin(admin.ModelAdmin):
    list_display = ('user','host','token','date','expire')
    def has_add_permission(self, request, obj=None):
        return False
    def has_delete_permission(self, request, obj=None):
        return False
    #readonly_fields = models.Token._meta.get_all_field_names()




admin.site.register(models.Hosts,HostAdmin)
admin.site.register(models.HostUsers,HostUserAdmin)
admin.site.register(models.BindHosts,BindHostAdmin)
admin.site.register(models.HostGroups,HostGroupAdmin)
admin.site.register(models.UserProfile,UserProfileAdmin)
#admin.site.register(models.PUserGroups,PUserGroupAdmin)
admin.site.register(models.AuditLog,AuditLogAdmin)
admin.site.register(models.TaskLog, TaskLogAdmin)
#admin.site.register(models.TaskLogDetail)
admin.site.register(models.TaskLogDetail,TaskLogDetailAdmin)
admin.site.register(models.Token,TokenAdmin)
admin.site.register(models.IDC)
admin.site.register(models.Department)