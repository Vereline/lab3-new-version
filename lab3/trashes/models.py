# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models

# Create your models here.


class Trash(models.Model):
    name = models.CharField(max_length=256)
    path = models.CharField(max_length=256)
    info_path = models.CharField(max_length=256)

    def __str__(self):              # __unicode__ on Python 2
        return self.path


class TrashContentFiles(models.Model):
    trash = models.ForeignKey(Trash)
    file_id = models.CharField(max_length=256)
    file_name = models.CharField(max_length=256)
    file_path = models.CharField(max_length=256)

    def __str__(self):              # __unicode__ on Python 2
        return self.file_path
