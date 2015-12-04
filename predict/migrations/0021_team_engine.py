# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('predict', '0020_auto_20151202_2217'),
    ]

    operations = [
        migrations.AddField(
            model_name='team',
            name='engine',
            field=models.CharField(default='Engine', max_length=50),
            preserve_default=False,
        ),
    ]
