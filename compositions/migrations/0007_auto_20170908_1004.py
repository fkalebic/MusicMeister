# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('compositions', '0006_composition_pdf_path'),
    ]

    operations = [
        migrations.RenameField(
            model_name='composition',
            old_name='graded',
            new_name='public',
        ),
    ]
