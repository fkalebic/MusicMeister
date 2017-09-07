# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('compositions', '0004_auto_20170907_1034'),
    ]

    operations = [
        migrations.AlterField(
            model_name='composition',
            name='comment',
            field=models.CharField(default=b'No comment yet', max_length=200, null=True),
        ),
    ]
