# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('web', '0002_auto_20150901_0352'),
    ]

    operations = [
        migrations.CreateModel(
            name='AuditLog',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('cmd', models.TextField()),
                ('cmd_res', models.SmallIntegerField()),
                ('memo', models.CharField(max_length=128, null=True, blank=True)),
                ('date', models.DateTimeField()),
                ('host', models.ForeignKey(to='web.BindHosts')),
                ('user', models.ForeignKey(to='web.UserProfile')),
            ],
            options={
                'verbose_name': '\u5ba1\u8ba1\u65e5\u5fd7',
                'verbose_name_plural': '\u5ba1\u8ba1\u65e5\u5fd7',
            },
        ),
    ]
