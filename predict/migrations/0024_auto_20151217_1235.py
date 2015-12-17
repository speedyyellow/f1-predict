# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('predict', '0023_auto_20151210_1420'),
    ]

    operations = [
        migrations.AlterField(
            model_name='prediction',
            name='created',
            field=models.DateField(),
        ),
    ]
