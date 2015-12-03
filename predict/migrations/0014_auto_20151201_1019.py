# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('predict', '0013_auto_20151201_1016'),
    ]

    operations = [
        migrations.AlterField(
            model_name='resultposition',
            name='driver',
            field=models.ForeignKey(to='predict.TeamDriver'),
        ),
    ]
