# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.shortcuts import render
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from .models import Trash, TaskToDo
from django.shortcuts import get_object_or_404, render
import os
# from mrm import add_trash, trash_policy
from .forms import TrashForm
from django.urls import reverse_lazy

# Create your views here.


# def trash_main(request):
#     return render(request, 'main.html', {})

class Main(ListView):
    template_name = 'main.html'
    model = Trash


class AddTrash(CreateView):
    success_url = reverse_lazy('main')
    template_name = "add_trash.html"
    model = Trash
    form_class = TrashForm


class RefreshTrash(UpdateView):
    success_url = reverse_lazy('main')
    template_name = "refresh_trash.html"
    model = Trash
    fields = ('path', 'name', 'info_path', )

#
# class DeleteTrash(DeleteView):
#     success_url = reverse_lazy('main')
#     template_name = "delete_trash.html"
#     model = Trash
