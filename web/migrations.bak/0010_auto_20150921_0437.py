# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('web', '0009_tasklogdetail_bind_host'),
    ]

    operations = [
        migrations.AlterField(
            model_name='tasklog',
            name='task_type',
            field=models.CharField(max_length=50, choices=[(b'cmd', b'CMD'), (b'file_send', b'\xe6\x89\xb9\xe9\x87\x8f\xe5\x8f\x91\xe9\x80\x81\xe6\x96\x87\xe4\xbb\xb6'), (b'file_get', b'\xe6\x89\xb9\xe9\x87\x8f\xe4\xb8\x8b\xe8\xbd\xbd\xe6\x96\x87\xe4\xbb\xb6')]),
        ),
    ]
