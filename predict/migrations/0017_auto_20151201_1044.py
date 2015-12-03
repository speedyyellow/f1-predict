# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('predict', '0016_teamdriver_name'),
    ]

    operations = [
        migrations.AlterField(
            model_name='teamdriver',
            name='name',
            field=models.CharField(max_length=100, blank=True),
        ),
    ]
