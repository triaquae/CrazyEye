# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('web', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='userprofile',
            name='hosts',
        ),
        migrations.AddField(
            model_name='userprofile',
            name='bind_hosts',
            field=models.ManyToManyField(to='web.BindHosts', verbose_name='\u6388\u6743\u4e3b\u673a'),
        ),
    ]
