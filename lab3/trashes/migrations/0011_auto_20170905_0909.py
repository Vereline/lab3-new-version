# -*- coding: utf-8 -*-
# Generated by Django 1.11.2 on 2017-09-05 09:09
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('trashes', '0010_auto_20170904_2337'),
    ]

    operations = [
        migrations.AddField(
            model_name='trash',
            name='info_logging_path',
            field=models.CharField(default=' ', max_length=256),
        ),
        migrations.AddField(
            model_name='trash',
            name='info_txt_path',
            field=models.CharField(default=' ', max_length=256),
        ),
    ]