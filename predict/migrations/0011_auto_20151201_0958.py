# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('predict', '0010_driver_number'),
    ]

    operations = [
        migrations.CreateModel(
            name='Prediction',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('created', models.DateTimeField()),
            ],
        ),
        migrations.AlterField(
            model_name='resultposition',
            name='driver',
            field=models.ForeignKey(to='predict.TeamDriver'),
        ),
    ]
