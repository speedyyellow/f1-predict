# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('predict', '0015_remove_teamdriver_name'),
    ]

    operations = [
        migrations.AddField(
            model_name='teamdriver',
            name='name',
            field=models.CharField(default='', max_length=100),
            preserve_default=False,
        ),
    ]
