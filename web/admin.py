#_*_coding:utf-8_*_
from django.contrib import admin


# Register your models here.
import models


class BindHostsInline(admin.TabularInline):
    model = models.BindHosts



class HostAdmin(admin.ModelAdmin):
    search_fields = ('hostname','ip_addr')
    list_display = ('hostname','ip_addr','port','system_type','enabled')


class HostUserAdmin(admin.ModelAdmin):
    list_display = ('auth_method','username','password')
class BindHostAdmin(admin.ModelAdmin):
    list_display = ('host','host_user','get_groups')
    filter_horizontal = ('host_group',)
    raw_id_fields = ("host",'host_user')


class HostGroupAdmin(admin.ModelAdmin):
    list_display = ('name',)
    #inlines = [
    #    BindHostsInline,
    #]

class UserProfileAdmin(admin.ModelAdmin):
    list_display = ('user','name','department','valid_begin_time','valid_end_time')
    filter_horizontal = ('host_groups','bind_hosts')

class AuditLogAdmin(admin.ModelAdmin):
    list_display = ('id','session','user','host','action_type','cmd','date')
    date_hierarchy = 'date'
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


class TaskLogAdmin(admin.ModelAdmin):
    list_display = ('id','start_time','end_time','task_type','user','cmd','expire_time')

class TaskLogDetailAdmin(admin.ModelAdmin):
    list_display = ('child_of_task','bind_host','result','date')

    def suit_row_attributes(self, obj, request):
        css_class = {
            'success': 'success',
            'unknown': 'warning',
            'failed': 'error',
        }.get(obj.result)
        if css_class:
            return {'class': css_class, 'data': obj.result}


class TokenAdmin(admin.ModelAdmin):
    list_display = ('user','host','token','date','expire')
admin.site.register(models.Hosts,HostAdmin)
admin.site.register(models.HostUsers,HostUserAdmin)
admin.site.register(models.BindHosts,BindHostAdmin)
admin.site.register(models.HostGroups,HostGroupAdmin)
admin.site.register(models.UserProfile,UserProfileAdmin)
#admin.site.register(models.PUserGroups,PUserGroupAdmin)
admin.site.register(models.AuditLog,AuditLogAdmin)
admin.site.register(models.TaskLog, TaskLogAdmin)
admin.site.register(models.TaskLogDetail,TaskLogDetailAdmin)
admin.site.register(models.Token,TokenAdmin)
admin.site.register(models.IDC)
admin.site.register(models.Department)