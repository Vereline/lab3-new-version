# -*- coding: utf-8 -*-
# Generated by Django 1.11.2 on 2017-09-04 23:07
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('trashes', '0007_auto_20170904_2216'),
    ]

    operations = [
        migrations.AlterField(
            model_name='tasktodo',
            name='task_process',
            field=models.CharField(choices=[(0, 'Not done'), (1, 'In process'), (2, 'Waiting'), (3, 'Done')], default='ggg', max_length=256),
        ),
    ]
