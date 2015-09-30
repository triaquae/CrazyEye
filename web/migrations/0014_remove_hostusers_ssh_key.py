# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('web', '0013_auto_20150930_1501'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='hostusers',
            name='ssh_key',
        ),
    ]
