# -*- coding: utf-8 -*-

from django import forms
from .models import Trash, TaskToDo


class TrashForm(forms.ModelForm):

    class Meta:
        model = Trash
        fields = ('name', 'path', 'info_path', 'maximum_size', 'maximum_time', 'policy_size',
                  'policy_time', )


class TaskForm(forms.ModelForm):

    class Meta:
        model = TaskToDo
        fields = ('file_path', 'file_task', 'info_path', 'force', 'dry_run', 'silent',
                  'task_is_done', 'maximum_time', 'maximum_size', 'trash', 'regular', )
