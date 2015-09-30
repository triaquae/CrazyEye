# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('web', '0009_auto_20150929_1430'),
    ]

    operations = [
        migrations.AlterField(
            model_name='auditlog',
            name='session',
            field=models.ForeignKey(to='web.SessionTrack'),
        ),
    ]
