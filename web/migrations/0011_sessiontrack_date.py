# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('web', '0010_auto_20150929_1432'),
    ]

    operations = [
        migrations.AddField(
            model_name='sessiontrack',
            name='date',
            field=models.DateTimeField(default=django.utils.timezone.now),
        ),
    ]
