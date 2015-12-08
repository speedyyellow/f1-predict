# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('predict', '0021_team_engine'),
    ]

    operations = [
        migrations.CreateModel(
            name='Engine',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(max_length=50)),
            ],
        ),
        migrations.RemoveField(
            model_name='team',
            name='engine',
        ),
        migrations.AddField(
            model_name='teamdriver',
            name='engine',
            field=models.ForeignKey(to='predict.Engine', null=True),
        ),
    ]
