# -*- coding: utf-8 -*-
# Generated by Django 1.9 on 2017-03-16 11:47
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('predict', '0028_prediction_score'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='prediction',
            name='score',
        ),
    ]
