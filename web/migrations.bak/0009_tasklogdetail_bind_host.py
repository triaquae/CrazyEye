# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('web', '0008_auto_20150915_0521'),
    ]

    operations = [
        migrations.AddField(
            model_name='tasklogdetail',
            name='bind_host',
            field=models.ForeignKey(default=1, to='web.BindHosts'),
            preserve_default=False,
        ),
    ]
