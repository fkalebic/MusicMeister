# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('compositions', '0003_auto_20170907_1029'),
    ]

    operations = [
        migrations.AlterField(
            model_name='composition',
            name='comment',
            field=models.CharField(default=b'', max_length=200, null=True),
        ),
    ]
