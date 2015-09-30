# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('web', '0003_auditlog'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='auditlog',
            name='cmd_res',
        ),
    ]
