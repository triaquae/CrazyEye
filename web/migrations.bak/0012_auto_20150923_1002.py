# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('web', '0011_token'),
    ]

    operations = [
        migrations.CreateModel(
            name='Department',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(unique=True, max_length=64)),
            ],
        ),
        migrations.CreateModel(
            name='IDC',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(unique=True, max_length=64)),
            ],
        ),
        migrations.RemoveField(
            model_name='pusergroups',
            name='host_groups',
        ),
        migrations.RemoveField(
            model_name='userprofile',
            name='user_groups',
        ),
        migrations.AddField(
            model_name='bindhosts',
            name='enabled',
            field=models.BooleanField(default=True),
        ),
        migrations.AddField(
            model_name='userprofile',
            name='host_groups',
            field=models.ManyToManyField(to='web.HostGroups', verbose_name='\u6388\u6743\u4e3b\u673a\u7ec4'),
        ),
        migrations.AddField(
            model_name='userprofile',
            name='hosts',
            field=models.ManyToManyField(to='web.Hosts', verbose_name='\u6388\u6743\u4e3b\u673a'),
        ),
        migrations.RemoveField(
            model_name='bindhosts',
            name='host_group',
        ),
        migrations.AddField(
            model_name='bindhosts',
            name='host_group',
            field=models.ManyToManyField(to='web.HostGroups'),
        ),
        migrations.AlterField(
            model_name='userprofile',
            name='department',
            field=models.ForeignKey(verbose_name='\u90e8\u95e8', to='web.Department'),
        ),
        migrations.DeleteModel(
            name='PUserGroups',
        ),
        migrations.AddField(
            model_name='hosts',
            name='idc',
            field=models.ForeignKey(default=0, to='web.IDC'),
            preserve_default=False,
        ),
    ]
