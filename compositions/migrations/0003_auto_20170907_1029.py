# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('compositions', '0002_composition_comment'),
    ]

    operations = [
        migrations.AlterField(
            model_name='composition',
            name='order',
            field=models.CharField(default=b'', max_length=200),
        ),
    ]
