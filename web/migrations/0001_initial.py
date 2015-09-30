# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import django.utils.timezone
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='AuditLog',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('cmd', models.TextField()),
                ('memo', models.CharField(max_length=128, null=True, blank=True)),
                ('date', models.DateTimeField()),
            ],
            options={
                'verbose_name': '\u5ba1\u8ba1\u65e5\u5fd7',
                'verbose_name_plural': '\u5ba1\u8ba1\u65e5\u5fd7',
            },
        ),
        migrations.CreateModel(
            name='BindHosts',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('enabled', models.BooleanField(default=True)),
            ],
            options={
                'verbose_name': '\u4e3b\u673a\u4e0e\u7528\u6237\u7ed1\u5b9a',
                'verbose_name_plural': '\u4e3b\u673a\u4e0e\u7528\u6237\u7ed1\u5b9a',
            },
        ),
        migrations.CreateModel(
            name='Department',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(unique=True, max_length=64)),
            ],
        ),
        migrations.CreateModel(
            name='HostGroups',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(unique=True, max_length=64)),
                ('memo', models.CharField(max_length=128, null=True, blank=True)),
            ],
            options={
                'verbose_name': '\u4e3b\u673a\u7ec4',
                'verbose_name_plural': '\u4e3b\u673a\u7ec4',
            },
        ),
        migrations.CreateModel(
            name='Hosts',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('hostname', models.CharField(unique=True, max_length=64)),
                ('ip_addr', models.GenericIPAddressField(unique=True)),
                ('system_type', models.CharField(default=b'linux', max_length=32, choices=[(b'windows', b'Windows'), (b'linux', b'Linux/Unix')])),
                ('port', models.IntegerField(default=22)),
                ('enabled', models.BooleanField(default=True)),
                ('memo', models.CharField(max_length=128, null=True, blank=True)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
            ],
            options={
                'verbose_name': '\u4e3b\u673a',
                'verbose_name_plural': '\u4e3b\u673a',
            },
        ),
        migrations.CreateModel(
            name='HostUsers',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('auth_method', models.CharField(max_length=16, choices=[(b'ssh-password', b'SSH/Password'), (b'ssh-key', b'SSH/KEY')])),
                ('username', models.CharField(max_length=32)),
                ('password', models.CharField(max_length=64, null=True, blank=True)),
                ('ssh_key', models.TextField(null=True, blank=True)),
                ('memo', models.CharField(max_length=128, null=True, blank=True)),
            ],
            options={
                'verbose_name': '\u4e3b\u673a\u7528\u6237',
                'verbose_name_plural': '\u4e3b\u673a\u7528\u6237',
            },
        ),
        migrations.CreateModel(
            name='IDC',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(unique=True, max_length=64)),
            ],
        ),
        migrations.CreateModel(
            name='TaskLog',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('start_time', models.DateTimeField(auto_now_add=True)),
                ('end_time', models.DateTimeField(null=True, blank=True)),
                ('task_type', models.CharField(max_length=50, choices=[(b'cmd', b'CMD'), (b'file_send', b'\xe6\x89\xb9\xe9\x87\x8f\xe5\x8f\x91\xe9\x80\x81\xe6\x96\x87\xe4\xbb\xb6'), (b'file_get', b'\xe6\x89\xb9\xe9\x87\x8f\xe4\xb8\x8b\xe8\xbd\xbd\xe6\x96\x87\xe4\xbb\xb6')])),
                ('cmd', models.TextField()),
                ('expire_time', models.IntegerField(default=30)),
                ('note', models.CharField(max_length=100, null=True, blank=True)),
                ('hosts', models.ManyToManyField(to='web.BindHosts')),
            ],
        ),
        migrations.CreateModel(
            name='TaskLogDetail',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('date', models.DateTimeField(auto_now_add=True)),
                ('event_log', models.TextField()),
                ('result', models.CharField(default=b'unknown', max_length=30, choices=[(b'success', b'Success'), (b'failed', b'Failed'), (b'unknown', b'Unknown')])),
                ('note', models.CharField(max_length=100, blank=True)),
                ('bind_host', models.ForeignKey(to='web.BindHosts')),
                ('child_of_task', models.ForeignKey(to='web.TaskLog')),
            ],
        ),
        migrations.CreateModel(
            name='Token',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('token', models.CharField(max_length=64)),
                ('date', models.DateTimeField(default=django.utils.timezone.now)),
                ('expire', models.IntegerField(default=300)),
                ('host', models.ForeignKey(to='web.BindHosts')),
            ],
        ),
        migrations.CreateModel(
            name='UserProfile',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(unique=True, max_length=32)),
                ('valid_begin_time', models.DateTimeField(default=django.utils.timezone.now)),
                ('valid_end_time', models.DateTimeField()),
                ('department', models.ForeignKey(verbose_name='\u90e8\u95e8', to='web.Department')),
                ('host_groups', models.ManyToManyField(to='web.HostGroups', verbose_name='\u6388\u6743\u4e3b\u673a\u7ec4')),
                ('hosts', models.ManyToManyField(to='web.Hosts', verbose_name='\u6388\u6743\u4e3b\u673a')),
                ('user', models.OneToOneField(to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'verbose_name': '\u5821\u5792\u673a\u7528\u6237',
                'verbose_name_plural': '\u5821\u5792\u673a\u7528\u6237',
            },
        ),
        migrations.AddField(
            model_name='token',
            name='user',
            field=models.ForeignKey(to='web.UserProfile'),
        ),
        migrations.AddField(
            model_name='tasklog',
            name='user',
            field=models.ForeignKey(to='web.UserProfile'),
        ),
        migrations.AddField(
            model_name='hosts',
            name='idc',
            field=models.ForeignKey(to='web.IDC'),
        ),
        migrations.AddField(
            model_name='bindhosts',
            name='host',
            field=models.ForeignKey(to='web.Hosts'),
        ),
        migrations.AddField(
            model_name='bindhosts',
            name='host_group',
            field=models.ManyToManyField(to='web.HostGroups'),
        ),
        migrations.AddField(
            model_name='bindhosts',
            name='host_user',
            field=models.ForeignKey(to='web.HostUsers'),
        ),
        migrations.AddField(
            model_name='auditlog',
            name='host',
            field=models.ForeignKey(to='web.BindHosts'),
        ),
        migrations.AddField(
            model_name='auditlog',
            name='user',
            field=models.ForeignKey(to='web.UserProfile'),
        ),
        migrations.AlterUniqueTogether(
            name='bindhosts',
            unique_together=set([('host', 'host_user')]),
        ),
    ]
