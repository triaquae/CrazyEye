# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('web', '0007_sessiontrack'),
    ]

    operations = [
        migrations.AddField(
            model_name='auditlog',
            name='sesstion',
            field=models.ForeignKey(default=1, to='web.SessionTrack'),
        ),
    ]
