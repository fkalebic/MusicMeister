# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('compositions', '0005_auto_20170907_1050'),
    ]

    operations = [
        migrations.AddField(
            model_name='composition',
            name='pdf_path',
            field=models.CharField(default=b'', max_length=200),
        ),
    ]
