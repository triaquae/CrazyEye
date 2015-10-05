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
import views

urlpatterns = [

    url(r'multitask/cmd/$', views.multitask_cmd,name='multitask_cmd'),
    url(r'multitask/res/$', views.multitask_res),
    url(r'multitask/file_download/(\d+)/$', views.file_download, name='file_download_url'),
    url(r'multitask/file_upload/$', views.multitask_file_upload),
    url(r'multitask/file/$', views.multitask_file,name='multitask_file'),
    url(r'multitask/action/$', views.multitask_task_action,name='multitask_action'),
    url(r'token/gen/$', views.token_gen,name='token_gen'),
    url(r'dashboard_summary/$', views.dashboard_summary,name='dashboard_summary'),
    url(r'dashboard_detail/$', views.dashboard_detail,name='dashboard_detail'),
    url(r'audit/user_counts/$', views.user_login_counts,name='user_login_counts'),
    url(r'audit/cmd_logs/$', views.audit_cmd_logs)
]
