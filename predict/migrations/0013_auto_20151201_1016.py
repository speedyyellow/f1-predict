# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('predict', '0012_teamdriver_name'),
    ]

    operations = [
        migrations.AlterField(
            model_name='resultposition',
            name='driver',
            field=models.ForeignKey(to='predict.Driver'),
        ),
    ]
