# -*- coding: utf-8 -*-
# Generated by Django 1.11.2 on 2017-09-08 10:22
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('trashes', '0012_auto_20170905_2239'),
    ]

    operations = [
        migrations.AddField(
            model_name='trash',
            name='is_busy',
            field=models.BooleanField(default=False),
        ),
    ]
