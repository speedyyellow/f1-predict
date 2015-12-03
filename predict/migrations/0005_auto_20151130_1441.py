# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('predict', '0004_auto_20151130_1340'),
    ]

    operations = [
        migrations.CreateModel(
            name='ResultPosition',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('position', models.IntegerField()),
                ('pole_position', models.BooleanField()),
                ('fastest_lap', models.BooleanField()),
                ('driver', models.ForeignKey(to='predict.Driver')),
            ],
        ),
        migrations.CreateModel(
            name='ResultSummary',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('season_round', models.ForeignKey(to='predict.Round')),
            ],
        ),
        migrations.AddField(
            model_name='resultposition',
            name='result',
            field=models.ForeignKey(to='predict.ResultSummary'),
        ),
    ]
