# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('predict', '0019_auto_20151202_2213'),
    ]

    operations = [
        migrations.AlterField(
            model_name='prediction',
            name='fastest_lap',
            field=models.ForeignKey(related_name='prediction_fastest_lap', to='predict.TeamDriver', null=True),
        ),
        migrations.AlterField(
            model_name='prediction',
            name='pole_position',
            field=models.ForeignKey(related_name='prediction_pole_position', to='predict.TeamDriver', null=True),
        ),
        migrations.AlterField(
            model_name='raceresult',
            name='fastest_lap',
            field=models.ForeignKey(related_name='result_fastest_lap', to='predict.TeamDriver', null=True),
        ),
        migrations.AlterField(
            model_name='raceresult',
            name='pole_position',
            field=models.ForeignKey(related_name='result_pole_position', to='predict.TeamDriver', null=True),
        ),
    ]
