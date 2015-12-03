# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('predict', '0018_remove_teamdriver_name'),
    ]

    operations = [
        migrations.CreateModel(
            name='PredictionPosition',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('driver', models.ForeignKey(to='predict.TeamDriver')),
                ('position', models.ForeignKey(to='predict.FinishingPosition')),
            ],
        ),
        migrations.RemoveField(
            model_name='resultposition',
            name='fastest_lap',
        ),
        migrations.RemoveField(
            model_name='resultposition',
            name='pole_position',
        ),
        migrations.AddField(
            model_name='prediction',
            name='fastest_lap',
            field=models.ForeignKey(related_name='prediction_fastest_lap', blank=True, to='predict.TeamDriver', null=True),
        ),
        migrations.AddField(
            model_name='prediction',
            name='pole_position',
            field=models.ForeignKey(related_name='prediction_pole_position', blank=True, to='predict.TeamDriver', null=True),
        ),
        migrations.AddField(
            model_name='prediction',
            name='user',
            field=models.ForeignKey(to=settings.AUTH_USER_MODEL, null=True),
        ),
        migrations.AddField(
            model_name='raceresult',
            name='fastest_lap',
            field=models.ForeignKey(related_name='result_fastest_lap', blank=True, to='predict.TeamDriver', null=True),
        ),
        migrations.AddField(
            model_name='raceresult',
            name='pole_position',
            field=models.ForeignKey(related_name='result_pole_position', blank=True, to='predict.TeamDriver', null=True),
        ),
        migrations.AlterField(
            model_name='seasonround',
            name='date',
            field=models.DateField(),
        ),
        migrations.AddField(
            model_name='predictionposition',
            name='prediction',
            field=models.ForeignKey(to='predict.Prediction'),
        ),
    ]
