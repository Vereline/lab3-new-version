# -*- coding: utf-8 -*-
# Generated by Django 1.11.2 on 2017-06-25 21:40
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('trashes', '0004_auto_20170624_2335'),
    ]

    operations = [
        migrations.AddField(
            model_name='tasktodo',
            name='name',
            field=models.CharField(default=' ', max_length=256),
        ),
    ]
