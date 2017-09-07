# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.contrib import admin
from trashes.models import Trash, TaskToDo

# Register your models here.
admin.site.register(Trash)
admin.site.register(TaskToDo)
