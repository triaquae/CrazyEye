# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('web', '0005_tasklog'),
    ]

    operations = [
        migrations.DeleteModel(
            name='TaskLog',
        ),
    ]
