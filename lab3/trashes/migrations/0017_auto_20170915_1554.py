# -*- coding: utf-8 -*-
# Generated by Django 1.11.2 on 2017-09-15 15:54
from __future__ import unicode_literals

import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('trashes', '0016_auto_20170915_1546'),
    ]

    operations = [
        migrations.AlterField(
            model_name='trash',
            name='maximum_size',
            field=models.PositiveIntegerField(default=1000, validators=[django.core.validators.MaxValueValidator(50000000)]),
        ),
        migrations.AlterField(
            model_name='trash',
            name='maximum_time',
            field=models.PositiveIntegerField(default=7, validators=[django.core.validators.MaxValueValidator(50000000)]),
        ),
    ]
