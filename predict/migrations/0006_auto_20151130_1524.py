# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('predict', '0005_auto_20151130_1441'),
    ]

    operations = [
        migrations.CreateModel(
            name='SeasonRound',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('date', models.DateField(verbose_name=b'race date')),
                ('circuit', models.ForeignKey(to='predict.Circuit')),
                ('season', models.ForeignKey(to='predict.Season')),
            ],
        ),
        migrations.RemoveField(
            model_name='round',
            name='circuit',
        ),
        migrations.RemoveField(
            model_name='round',
            name='season',
        ),
        migrations.AlterField(
            model_name='resultsummary',
            name='season_round',
            field=models.ForeignKey(to='predict.SeasonRound'),
        ),
        migrations.DeleteModel(
            name='Round',
        ),
    ]
