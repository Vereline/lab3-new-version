# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models
import os
# Create your models here.


class Trash(models.Model):
    name = models.CharField(max_length=256)
    path = models.CharField(max_length=256)
    info_path = models.CharField(max_length=256, default=' ')
    maximum_size = models.IntegerField(default=1000)
    maximum_time = models.IntegerField(default=7)
    policy_time = models.BooleanField(default=False)
    policy_size = models.BooleanField(default=False)

    class Meta:
        db_table = 'trashes'

    def __str__(self):              # __unicode__ on Python 2
        return os.path.abspath(self.path)


class TaskToDo(models.Model):
    # file_task = models.CharField(max_length=256)
    name = models.CharField(max_length=256, default=' ')
    file_path = models.CharField(max_length=256, default=' ')
    trash = models.ForeignKey(Trash, default=None)
    force = models.BooleanField(default=False)
    dry_run = models.BooleanField(default=False)
    silent = models.BooleanField(default=False)

    tasks = (
        ('delete by regex', 'delete by regex'),
        ('delete by filename', 'delete by filename'),
        ('recover all trash', 'recover all trash'),
        ('clear all trash', 'clear all trash')
    )

    file_task = models.CharField(max_length=256, choices=tasks, default=None)
    regular = models.CharField(max_length=256, default=' ')
    info_path = models.CharField(max_length=256, default=' ')
    maximum_size = models.IntegerField(default=1000)
    maximum_time = models.IntegerField(default=7)
    task_is_done = models.BooleanField(default=False)

    class Meta:
        db_table = 'task'

    def __str__(self):              # __unicode__ on Python 2
        return self.name
