# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('predict', '0026_teamdriver_active'),
    ]

    operations = [
        migrations.AlterField(
            model_name='teamdriver',
            name='active',
            field=models.BooleanField(default=True),
        ),
    ]
