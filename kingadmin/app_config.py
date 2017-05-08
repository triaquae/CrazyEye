#_*_coding:utf-8_*_

from django import conf


for app in conf.settings.INSTALLED_APPS:
    try:
        admin_module = __import__("%s.kingadmin" % app)
        #print(admin_module.kingadmin.site)
    except ImportError:
        pass
