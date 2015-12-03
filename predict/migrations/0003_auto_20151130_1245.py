# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('predict', '0002_circuit_country'),
    ]

    operations = [
        migrations.CreateModel(
            name='TeamDriver',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
            ],
        ),
        migrations.RemoveField(
            model_name='driver',
            name='team',
        ),
        migrations.AddField(
            model_name='teamdriver',
            name='driver',
            field=models.ForeignKey(to='predict.Driver'),
        ),
        migrations.AddField(
            model_name='teamdriver',
            name='season',
            field=models.ForeignKey(to='predict.Season'),
        ),
        migrations.AddField(
            model_name='teamdriver',
            name='team',
            field=models.ForeignKey(to='predict.Team'),
        ),
    ]
