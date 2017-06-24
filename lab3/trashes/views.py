# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.shortcuts import render
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from .models import Trash, TaskToDo
from django.shortcuts import get_object_or_404, render
import os
import smartrm.Trash as smartrm_trash
# from smartrm.Trash import Trash
from .forms import TrashForm
from django.urls import reverse_lazy

# Create your views here.


# def trash_main(request):
#     return render(request, 'main.html', {})


# get rid of this
DEFAULT_CONFIG = {
    "path": "/home/vereline/Trash",
    "trash_log_path": "/home/vereline/Trash/Trash_log/Trash_log.json",
    "trash_log_path_txt": "/home/vereline/Trash/Trash_log/Trash_log.txt",
    "trash_logging_path": "/home/vereline/Trash/Trash_log/out.log",
    "policy_time": "True",
    "policy_size": "False",
    "max_size": 100000,
    "current_size": 0,
    "max_capacity": 1000,
    "max_time": 7
}


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


class DeleteTrash(DeleteView):
    success_url = reverse_lazy('main')
    template_name = "delete_trash.html"
    model = Trash
    form_class = TrashForm
    fields = ('path', 'name', 'info_path',)


class Task(ListView):
    template_name = 'task_list.html'
    model = TaskToDo


def define_action(request, name):
    trash_object = get_object_or_404(Trash, name=name)
    trash_folder = trash_object.path
    trash_folder_info = trash_object.info_path
    # add_trash(trash_fold)

    trash = smartrm_trash.Trash(trash_folder, trash_folder_info,
            DEFAULT_CONFIG['trash_log_path_txt'],
            DEFAULT_CONFIG['policy_time'], DEFAULT_CONFIG['policy_size'], DEFAULT_CONFIG['max_size'],
            DEFAULT_CONFIG['current_size'], DEFAULT_CONFIG['max_capacity'], DEFAULT_CONFIG['max_time'],
            q=None)

    # trash_path = os.path.join(trash_object.path, "trash")
    # info_path = os.path.join(trash_object.path, "info")

    #trash_policy(trash_path, info_path, trash_object.policy, trash_object.savetime, trash_object.maxsize)
    trash_list = trash.watch_trash(dry_run=False)  # smartrm.show_trash_(trash_path, 0, dry=False)
    return render(request, "define_action.html", {"name": name, "trash_list": trash_list})
#
#
# def remove_file(request, name):
#     trash_object = get_object_or_404(Trash, name=name)
#     trash_path = os.path.join(trash_object.path, "trash")
#     path=request.POST['delete']
#     info_path = os.path.join(trash_object.path, "info")
#     #tack = Tack(tack='remove', target=path)
#     #tack.save()
#     #smartrm.remove(path, trash_path, info_path, dry=False)
#     return define_action(request, name)
#
# def recover(request, name):
#     trash_object = get_object_or_404(Trash, name=name)
#     trash_path = os.path.join(trash_object.path, "trash")
#     info_path = os.path.join(trash_object.path, "info")
#     target=request.POST['file']
#    # tack = Tack(tack='recover', target=target)
#    # tack.save()
#    # smartrm.recover(target, trash_path, info_path, dry=False)
#     return define_action(request, name)
#
#
# def clean_trash(request, name):
#     trash_object = get_object_or_404(Trash, name=name)
#     trash_path = os.path.join(trash_object.path, "trash")
#     info_path = os.path.join(trash_object.path, "info")
#     #tack = Tack(tack='clean', target=trash_object.name)
#     #tack.save()
#     #smartrm.empty_trash(trash_path, info_path, dry=False)
#     return define_action(request, name)
#
#
# def regular_expression(request, name):
#     trash_object = get_object_or_404(Trash, name=name)
#     trash_path = os.path.join(trash_object.path, "trash")
#     info_path = os.path.join(trash_object.path, "info")
#     subtree = request.POST['path']
#     reg = request.POST['reg']
#     #tack = Tack(tack='regular exptession', target=reg)
#     #tack.save()
#     #smartrm.regular_expression_rm(subtree, reg, trash_path, info_path)
#     print subtree, reg, trash_path, info_path
#     return define_action(request, name)
