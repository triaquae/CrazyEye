#_*_coding:utf-8_*_

from web import models

from web.king_admin_base import ModelAdminBase,register


enabled_admins = {} #不要动，所有注册的表都会自动添加到这里

class UserAdmin(ModelAdminBase):
    model  = models.UserProfile
    list_display = ('id','name','email','is_admin')
    filter_horizontal = ('host_groups','bind_hosts')

class HostAdmin(ModelAdminBase):
    model = models.Hosts
    list_display = ('id','hostname','ip_addr','port','idc','system_type','enabled','created_at')
    list_per_page = 1
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

class HostUsersAdmin(ModelAdminBase):
    model = models.HostUsers
    list_display = ['auth_method','username','password']

register(enabled_admins,models.UserProfile,UserAdmin)
register(enabled_admins,models.Hosts,HostAdmin)
register(enabled_admins,models.HostGroups,HostGroupAdmin)
register(enabled_admins,models.AuditLog,AuditLogAdmin)
register(enabled_admins,models.HostUsers,HostUsersAdmin)