"""CrazyEye URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.8/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Add an import:  from blog import urls as blog_urls
    2. Add a URL to urlpatterns:  url(r'^blog/', include(blog_urls))
"""
from django.conf.urls import include, url
from django.contrib import admin

from web import views,api_urls
from web import cus_admin

urlpatterns = [
    url(r'^admin/', include(admin.site.urls)),
     #url(r'^myadmin/', include(cus_admin.admin_site.urls)),
    url(r'session_security/', include('session_security.urls')),
    url(r'^$',views.dashboard ),
    url(r'^hosts/$',views.hosts, name='host_list' ),
    url(r'^hosts/multi/$',views.hosts_multi),
    url(r'^hosts/crontab/$',views.crontab),
    url(r'^multi_task/log/deatail/(\d+)/$',views.multi_task_log_detail,name='multi_task_log_detail'),
    url(r'^hosts/multi/filetrans$',views.hosts_multi_filetrans),
    url(r'^host/detail/', views.host_detail),
    url(r'^api/',include(api_urls)),
    url(r'^personal/',views.personal,name='personal'),
    url(r'^user_audit/(\d+)/$',views.user_audit, name='user_audit'),
    url(r'^audit/$',views.audit, name='audit'),
    url(r'^session/(\d+)/$',views.session_reccord, name='session_record'),

    url(r'^logout/',views.logout,name='logout'),

    url(r'^login/$',views.login,name='login'),
    url(r'^accounts/profile/$',views.personal),
    url(r'^configure/index/$',views.configure_index,name="table_index"),#显示所有注册的表
    url(r'^configure/(\w+)/$',views.configure_url_dispatch,name="table_list"), #显示每个表的数据
    url(r'^configure/(\w+)/change/(\d+)/$',views.table_change,name="table_change"),
    url(r'^configure/(\w+)/add/$',views.table_add,name="table_add"),

]
