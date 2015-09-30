# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('web', '0003_auto_20150923_1404'),
    ]

    operations = [
        migrations.CreateModel(
            name='Test',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('test', models.CharField(max_length=32)),
                ('num', models.IntegerField()),
            ],
        ),
        migrations.AlterModelOptions(
            name='bindhosts',
            options={'verbose_name': '\u4e3b\u673a\u4e0e\u8fdc\u7a0b\u7528\u6237\u7ed1\u5b9a', 'verbose_name_plural': '\u4e3b\u673a\u8fdc\u7a0b\u4e0e\u7528\u6237\u7ed1\u5b9a'},
        ),
        migrations.AlterModelOptions(
            name='department',
            options={'verbose_name': '\u90e8\u95e8', 'verbose_name_plural': '\u90e8\u95e8'},
        ),
        migrations.AlterModelOptions(
            name='hostusers',
            options={'verbose_name': '\u8fdc\u7a0b\u7528\u6237', 'verbose_name_plural': '\u8fdc\u7a0b\u7528\u6237'},
        ),
        migrations.AlterModelOptions(
            name='idc',
            options={'verbose_name': 'IDC', 'verbose_name_plural': 'IDC'},
        ),
        migrations.AlterModelOptions(
            name='tasklog',
            options={'verbose_name': '\u6279\u91cf\u4efb\u52a1', 'verbose_name_plural': '\u6279\u91cf\u4efb\u52a1'},
        ),
        migrations.AlterModelOptions(
            name='tasklogdetail',
            options={'verbose_name': '\u6279\u91cf\u4efb\u52a1\u65e5\u5fd7', 'verbose_name_plural': '\u6279\u91cf\u4efb\u52a1\u65e5\u5fd7'},
        ),
        migrations.AlterModelOptions(
            name='userprofile',
            options={'verbose_name': 'CrazyEye\u8d26\u6237', 'verbose_name_plural': 'CrazyEye\u8d26\u6237'},
        ),
    ]
