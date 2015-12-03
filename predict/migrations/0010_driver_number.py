# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('predict', '0009_season_active'),
    ]

    operations = [
        migrations.AddField(
            model_name='driver',
            name='number',
            field=models.IntegerField(default=0),
            preserve_default=False,
        ),
    ]
