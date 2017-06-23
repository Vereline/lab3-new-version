# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models

# Create your models here.


class Trash(models.Model):
    name = models.CharField(max_length=256)
    path = models.CharField(max_length=256)
    info_path = models.CharField(max_length=256)

    class Meta:
        db_table = 'trashes'

    # def __str__(self):              # __unicode__ on Python 2
    #     return self.path


class TaskToDo(models.Model):
    file_task = models.CharField(max_length=256)
    file_path = models.CharField(max_length=256)

    class Meta:
        db_table = 'task'

    # def __str__(self):              # __unicode__ on Python 2
    #     return self.file_path
