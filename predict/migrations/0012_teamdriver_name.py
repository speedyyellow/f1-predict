# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('predict', '0011_auto_20151201_0958'),
    ]

    operations = [
        migrations.AddField(
            model_name='teamdriver',
            name='name',
            field=models.CharField(default='', max_length=10),
            preserve_default=False,
        ),
    ]
