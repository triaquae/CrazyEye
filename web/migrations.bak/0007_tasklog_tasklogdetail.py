# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('web', '0006_delete_tasklog'),
    ]

    operations = [
        migrations.CreateModel(
            name='TaskLog',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('start_time', models.DateTimeField(auto_now_add=True)),
                ('end_time', models.DateTimeField(null=True, blank=True)),
                ('task_type', models.CharField(max_length=50, choices=[(b'cmd', b'CMD'), (b'file_transfer', b'FileTransfer')])),
                ('cmd', models.TextField()),
                ('expire_time', models.IntegerField(default=30)),
                ('note', models.CharField(max_length=100, null=True, blank=True)),
                ('hosts', models.ManyToManyField(to='web.BindHosts')),
                ('user', models.ForeignKey(to='web.UserProfile')),
            ],
        ),
        migrations.CreateModel(
            name='TaskLogDetail',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('date', models.DateTimeField(auto_now_add=True)),
                ('event_log', models.TextField()),
                ('result', models.CharField(default=b'unknown', max_length=30, choices=[(b'success', b'Success'), (b'failed', b'Failed'), (b'unkown', b'Unkown')])),
                ('note', models.CharField(max_length=100, blank=True)),
                ('child_of_task', models.ForeignKey(to='web.TaskLog')),
            ],
        ),
    ]
