# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('predict', '0025_circuit_country_code'),
    ]

    operations = [
        migrations.AddField(
            model_name='teamdriver',
            name='active',
            field=models.BooleanField(default=True),
            preserve_default=False,
        ),
    ]
