# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('web', '0008_auditlog_sesstion'),
    ]

    operations = [
        migrations.RenameField(
            model_name='auditlog',
            old_name='sesstion',
            new_name='session',
        ),
    ]
