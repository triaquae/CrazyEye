#_*_coding:utf-8_*_
__author__ = 'jieli'

from django.contrib import admin
import models

class MyAdminSite(admin.AdminSite):
    site_header = 'TEST ADMIn site'

admin_site = MyAdminSite(name="TEST_ADMIN")
admin_site.register(models.BindHosts)