# -*- coding: utf-8 -*-

from django import forms
from .models import Trash, TaskToDo


class TrashForm(forms.ModelForm):

    class Meta:
        model = Trash
        fields = ('name', 'path', 'info_path', 'info_txt_path', 'info_logging_path',
                  'maximum_size', 'maximum_time', 'policy_size',
                  'policy_time', )


class TaskForm(forms.ModelForm):

    class Meta:
        model = TaskToDo
        fields = ('name', 'file_path', 'file_task', 'verbose', 'dry_run', 'silent',
                  'trash', 'regular', )
