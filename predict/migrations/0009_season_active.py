# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('predict', '0008_auto_20151130_1643'),
    ]

    operations = [
        migrations.AddField(
            model_name='season',
            name='active',
            field=models.BooleanField(default=0),
            preserve_default=False,
        ),
    ]
