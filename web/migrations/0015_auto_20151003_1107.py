# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('web', '0014_remove_hostusers_ssh_key'),
    ]

    operations = [
        migrations.AddField(
            model_name='tasklog',
            name='task_pid',
            field=models.IntegerField(default=0),
        ),
        migrations.AlterField(
            model_name='hosts',
            name='enabled',
            field=models.BooleanField(default=True, help_text='\u4e3b\u673a\u82e5\u4e0d\u60f3\u88ab\u7528\u6237\u8bbf\u95ee\u53ef\u4ee5\u53bb\u6389\u6b64\u9009\u9879'),
        ),
        migrations.AlterField(
            model_name='hostusers',
            name='auth_method',
            field=models.CharField(help_text='\u5982\u679c\u9009\u62e9SSH/KEY\uff0c\u8bf7\u786e\u4fdd\u4f60\u7684\u79c1\u94a5\u6587\u4ef6\u5df2\u5728settings.py\u4e2d\u6307\u5b9a', max_length=16, choices=[(b'ssh-password', b'SSH/Password'), (b'ssh-key', b'SSH/KEY')]),
        ),
        migrations.AlterField(
            model_name='hostusers',
            name='password',
            field=models.CharField(help_text='\u5982\u679cauth_method\u9009\u62e9\u7684\u662fSSH/KEY,\u90a3\u6b64\u5904\u4e0d\u9700\u8981\u586b\u5199..', max_length=64, null=True, blank=True),
        ),
    ]
