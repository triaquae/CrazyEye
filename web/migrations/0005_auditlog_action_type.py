# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('web', '0004_auto_20150924_1237'),
    ]

    operations = [
        migrations.AddField(
            model_name='auditlog',
            name='action_type',
            field=models.IntegerField(default=0, choices=[(0, b'CMD'), (1, b'Login'), (2, b'Logout'), (3, b'GetFile'), (4, b'SendFile')]),
        ),
    ]
