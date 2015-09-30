# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('web', '0007_tasklog_tasklogdetail'),
    ]

    operations = [
        migrations.AlterField(
            model_name='tasklogdetail',
            name='result',
            field=models.CharField(default=b'unknown', max_length=30, choices=[(b'success', b'Success'), (b'failed', b'Failed'), (b'unknown', b'Unknown')]),
        ),
    ]
