# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('predict', '0022_auto_20151208_0804'),
    ]

    operations = [
        migrations.RenameField(
            model_name='seasonround',
            old_name='date',
            new_name='race_date',
        ),
        migrations.AddField(
            model_name='seasonround',
            name='event_date',
            field=models.DateField(null=True),
        ),
    ]
