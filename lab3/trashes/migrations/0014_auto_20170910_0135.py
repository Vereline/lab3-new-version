# -*- coding: utf-8 -*-
# Generated by Django 1.11.2 on 2017-09-10 01:35
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('trashes', '0013_trash_is_busy'),
    ]

    operations = [
        migrations.AlterField(
            model_name='tasktodo',
            name='task_process',
            field=models.CharField(choices=[('Not done', 'Not done'), ('In process', 'In process'), ('Waiting', 'Waiting'), ('Done', 'Done'), ('Error', 'Error')], default='Not done', max_length=256),
        ),
    ]