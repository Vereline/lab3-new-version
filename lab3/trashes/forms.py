# -*- coding: utf-8 -*-

from django import forms
from .models import Trash


class TrashForm(forms.ModelForm):

    class Meta:
        model = Trash
        fields = ('name', 'path', 'info_path', )
