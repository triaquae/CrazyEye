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
            name='BindHosts',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
            ],
            options={
                'verbose_name': '\u4e3b\u673a\u4e0e\u7528\u6237\u7ed1\u5b9a',
                'verbose_name_plural': '\u4e3b\u673a\u4e0e\u7528\u6237\u7ed1\u5b9a',
            },
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
                ('ssh_key', models.CharField(max_length=64, null=True, blank=True)),
                ('memo', models.CharField(max_length=128, null=True, blank=True)),
            ],
            options={
                'verbose_name': '\u4e3b\u673a\u7528\u6237',
                'verbose_name_plural': '\u4e3b\u673a\u7528\u6237',
            },
        ),
        migrations.CreateModel(
            name='PUserGroups',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(unique=True, max_length=64)),
                ('host_groups', models.ManyToManyField(to='web.HostGroups')),
            ],
            options={
                'verbose_name': '\u5821\u5792\u673a\u7528\u6237\u7ec4',
                'verbose_name_plural': '\u5821\u5792\u673a\u7528\u6237\u7ec4',
            },
        ),
        migrations.CreateModel(
            name='UserProfile',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(unique=True, max_length=32)),
                ('department', models.CharField(max_length=32, verbose_name='\u90e8\u95e8')),
                ('valid_begin_time', models.DateTimeField(default=django.utils.timezone.now)),
                ('valid_end_time', models.DateTimeField()),
                ('user', models.OneToOneField(to=settings.AUTH_USER_MODEL)),
                ('user_groups', models.ManyToManyField(to='web.PUserGroups')),
            ],
            options={
                'verbose_name': '\u5821\u5792\u673a\u7528\u6237',
                'verbose_name_plural': '\u5821\u5792\u673a\u7528\u6237',
            },
        ),
        migrations.AddField(
            model_name='bindhosts',
            name='host',
            field=models.ForeignKey(to='web.Hosts'),
        ),
        migrations.AddField(
            model_name='bindhosts',
            name='host_group',
            field=models.ForeignKey(to='web.HostGroups'),
        ),
        migrations.AddField(
            model_name='bindhosts',
            name='host_user',
            field=models.ForeignKey(to='web.HostUsers'),
        ),
        migrations.AlterUniqueTogether(
            name='bindhosts',
            unique_together=set([('host', 'host_user')]),
        ),
    ]
