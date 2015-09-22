#_*_coding:utf-8_*_
from django.contrib import admin
from django import forms
from django.contrib.auth.admin import UserAdmin


import models

from django.shortcuts import render_to_response,render,HttpResponse

from django.contrib.admin.views.decorators import staff_member_required

from django.conf.urls import patterns, include, url
# Register your models here.


class HostAdmin(admin.ModelAdmin):
    search_fields = ('hostname','ip_addr')
    list_display = ('hostname','ip_addr','port','system_type','enabled')


class BindHostInline(admin.TabularInline):
    model = models.BindHosts.host_group.through

    readonly_fields = ['hostname']
    def hostname(self, instance):
        print dir(instance)
        return '%s(%s)' %(instance.bindhosts.host.hostname,instance.bindhosts.host.ip_addr)
    hostname.short_description = 'row name'


class HostUserAdmin(admin.ModelAdmin):
    list_display = ('auth_method','username')
class BindHostAdmin(admin.ModelAdmin):
    list_display = ('host','host_user','get_groups')
    list_filter = ('host','host_user','host_group')
    filter_horizontal = ('host_group',)
    raw_id_fields = ("host",'host_user')

    def get_urls(self):

        urls = super(BindHostAdmin, self).get_urls()
        my_urls = patterns("",
            url(r"^multi_add/$", self.multi_add)
        )
        return my_urls + urls


    #@staff_member_required
    def multi_add(self, request):
        if request.user.is_superuser:
            import admin_custom_view
            err = {}
            result = None
            chosen_data = {}
            if request.method == 'POST':
                print request.POST
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
    inlines = [
        BindHostInline,
    ]

class UserProfileAdmin(admin.ModelAdmin):
    list_display = ('user','name','department','valid_begin_time','valid_end_time')
    filter_horizontal = ('host_groups','bind_hosts')

class AuditLogAdmin(admin.ModelAdmin):
    list_display = ('id','session','user','host','action_type','cmd','date')
    list_filter = ('session','user','host','action_type','date')
    search_fields = ['user__user__username','host__host__hostname','host__host__ip_addr','cmd']
    actions = ['make_published']

    def get_actions(self, request):
        actions = super(AuditLogAdmin, self).get_actions(request)

        if 'delete_selected' in actions:
            del actions['delete_selected']
        return actions

    def make_published(self, request, queryset):
        rows_deleted = models.AuditLog.objects.all()
        print '--row:',rows_deleted
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
    readonly_fields = models.AuditLog._meta.get_all_field_names()

class TaskLogAdmin(admin.ModelAdmin):
    list_display = ('id','start_time','end_time','task_type','user','cmd','total_task','success_task','failed_task','unknown_task','expire_time')
    list_filter = ('task_type','user','start_time')
    readonly_fields = models.TaskLog._meta.get_all_field_names()
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
    readonly_fields = models.TaskLogDetail._meta.get_all_field_names()


class TokenAdmin(admin.ModelAdmin):
    list_display = ('user','host','token','date','expire')
    def has_add_permission(self, request, obj=None):
        return False
    def has_delete_permission(self, request, obj=None):
        return False
    readonly_fields = models.Token._meta.get_all_field_names()




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