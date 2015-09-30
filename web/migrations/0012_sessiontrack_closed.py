# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('web', '0011_sessiontrack_date'),
    ]

    operations = [
        migrations.AddField(
            model_name='sessiontrack',
            name='closed',
            field=models.BooleanField(default=True),
        ),
    ]
