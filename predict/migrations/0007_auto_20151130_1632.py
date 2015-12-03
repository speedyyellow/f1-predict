# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('predict', '0006_auto_20151130_1524'),
    ]

    operations = [
        migrations.RenameModel(
            old_name='ResultSummary',
            new_name='RaceResult',
        ),
    ]
