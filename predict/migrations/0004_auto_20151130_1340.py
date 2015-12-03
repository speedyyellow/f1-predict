# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('predict', '0003_auto_20151130_1245'),
    ]

    operations = [
        migrations.AlterField(
            model_name='round',
            name='date',
            field=models.DateField(verbose_name=b'race date'),
        ),
    ]
