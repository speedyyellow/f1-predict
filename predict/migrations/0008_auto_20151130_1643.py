# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('predict', '0007_auto_20151130_1632'),
    ]

    operations = [
        migrations.CreateModel(
            name='FinishingPosition',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('position', models.IntegerField()),
                ('points', models.IntegerField()),
            ],
        ),
        migrations.AlterField(
            model_name='resultposition',
            name='position',
            field=models.ForeignKey(to='predict.FinishingPosition'),
        ),
    ]
