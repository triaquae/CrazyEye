# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('web', '0002_auto_20150923_1208'),
    ]

    operations = [
        migrations.AlterUniqueTogether(
            name='hostusers',
            unique_together=set([('auth_method', 'password', 'username')]),
        ),
    ]
