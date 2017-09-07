# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.shortcuts import render
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from .models import Trash, TaskToDo
from django.shortcuts import get_object_or_404, render, redirect, HttpResponse
import os
import smartrm.Trash as smartrm_trash
import smartrm.Smart_rm as smart_rm
# from smartrm.Trash import Trash
from .forms import TrashForm, TaskForm
from django.urls import reverse_lazy
import json
import ast
import smartrm.threading_smartrm as threading_smrm
import time

# Create your views here.


# def trash_main(request):
#     return render(request, 'main.html', {})

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


class TaskList(ListView):
    template_name = 'task_list.html'
    model = TaskToDo
    #
    # def get_context_data(self, **kwargs):
    #     context = super(TaskList,self).get_context_data()
    #
    # def render_to_response(self, context, **response_kwargs):
    #     pass


class AddTrash(CreateView):
    success_url = reverse_lazy('main')
    template_name = "add_trash.html"
    model = Trash
    form_class = TrashForm


class RefreshTrash(UpdateView):
    success_url = reverse_lazy('main')
    template_name = "refresh_trash.html"
    model = Trash
    fields = ('name', 'path', 'info_path', 'info_txt_path',
              'info_logging_path', 'maximum_size', 'maximum_time', 'policy_size',
              'policy_time',)


class DeleteTrash(DeleteView):
    success_url = reverse_lazy('main')
    template_name = "delete_trash.html"
    model = Trash
    form_class = TrashForm
    fields = ('path', 'name', 'info_path',)


class AddTask(CreateView):
    success_url = reverse_lazy('task_list')
    template_name = 'add_task.html'
    model = TaskToDo
    form_class = TaskForm
    # fields = ('file_path', 'file_task', 'info_path', 'force', 'dry_run', 'silent',
    #           'task_is_done', 'maximum_time', 'maximum_size', 'trash', 'regular',)


class RefreshTask(UpdateView):
    success_url = reverse_lazy('task_list')
    template_name = "refresh_task.html"
    model = TaskToDo
    fields = ('name', 'file_path', 'file_task', 'info_path', 'force', 'dry_run', 'silent',
              'maximum_time', 'maximum_size', 'trash', 'regular', )


class DeleteTask(DeleteView):
    success_url = reverse_lazy('task_list')
    template_name = "delete_task.html"
    model = TaskToDo
    form_class = TaskForm
    fields = ('name', 'file_path', 'file_task', 'info_path', 'force', 'dry_run', 'silent',
              'maximum_time', 'maximum_size', 'trash', 'regular', )


def define_action(request, name):
    trash_object = get_object_or_404(Trash, name=name)
    trash_folder = trash_object.path
    trash_folder_info = trash_object.info_path
    # add_trash(trash_fold)
    trash_log_path_txt = trash_object.info_txt_path
    trash_logging = trash_object.info_logging_path
    t_policy_s = trash_object.policy_size
    t_policy_t = trash_object.policy_time
    t_max_s = trash_object.maximum_size
    t_max_t = trash_object.maximum_time
    trash = smartrm_trash.Trash(trash_folder, trash_folder_info,
                                trash_log_path_txt,
                                t_policy_t, t_policy_s,
                                t_max_s,
                                DEFAULT_CONFIG['current_size'], DEFAULT_CONFIG['max_capacity'],
                                t_max_t,
                                q=None)
    # trash_path = os.path.join(trash_object.path, "trash")
    # info_path = os.path.join(trash_object.path, "info")

    trash_list = trash.watch_trash()
    print {"name": name, "trash_list": trash_list}
    return render(request, "define_action.html", {"name": name, "trash_list": trash_list})


def remove_file(request, name):
    trash_object = get_object_or_404(Trash, name=name)
    # trash_path = os.path.join(trash_object.path, "trash")
    trash_folder = trash_object.path
    trash_folder_info = trash_object.info_path
    trash_log_path_txt = trash_object.info_txt_path
    trash_logging = trash_object.info_logging_path
    t_policy_s = trash_object.policy_size
    t_policy_t = trash_object.policy_time
    t_max_s = trash_object.maximum_size
    t_max_t = trash_object.maximum_time
    trash = smartrm_trash.Trash(trash_folder, trash_folder_info,
                                trash_log_path_txt,
                                t_policy_t, t_policy_s,
                                t_max_s,
                                DEFAULT_CONFIG['current_size'], DEFAULT_CONFIG['max_capacity'],
                                t_max_t,
                                q=None)

    # print trash
    path = request.POST.getlist('file')
    # info_path = os.path.join(trash_object.path, "info")
    print 'REMOVE'
    my_names = []
    for item in path:
        s = ast.literal_eval(item)  # str to dict
        my_names.append(s['name'])
        # s = item.encode('utf-8')
        # info_dict = json.loads(item)  # problems with double quotes

    trash.delete_manually(my_names)

    return define_action(request, name)


def recover_file(request, name):
    trash_object = get_object_or_404(Trash, name=name)
    # trash_path = os.path.join(trash_object.path, "trash")
    trash_folder = trash_object.path
    trash_folder_info = trash_object.info_path
    trash_log_path_txt = trash_object.info_txt_path
    trash_logging = trash_object.info_logging_path
    t_policy_s = trash_object.policy_size
    t_policy_t = trash_object.policy_time
    t_max_s = trash_object.maximum_size
    t_max_t = trash_object.maximum_time
    trash = smartrm_trash.Trash(trash_folder, trash_folder_info,
                                trash_log_path_txt,
                                t_policy_t, t_policy_s,
                                t_max_s,
                                DEFAULT_CONFIG['current_size'], DEFAULT_CONFIG['max_capacity'],
                                t_max_t,
                                q=None)

    print trash
    path = request.POST.getlist('file')

    my_names = []
    for item in path:
        s = ast.literal_eval(item)  # str to dict
        my_names.append(s['name'])
        # s = item.encode('utf-8')
        # info_dict = json.loads(item)  # problems with double quotes
        # print info_dict
        # my_names.append(info_dict['name'])

    trash.restore_trash_manually(my_names, False, False, False)
    return define_action(request, name)


def do_the_task(request, pk):

    print 'do the task'
    print pk
    trash_task_object = get_object_or_404(TaskToDo, pk=pk)
    print trash_task_object
    print 'do the task'
    trash_object = trash_task_object.trash

    # works
    #
    # trash_task_object.task_process = trash_task_object.DONE
    # trash_task_object.save()

    trash_folder = trash_object.path
    trash_folder_info = trash_object.info_path
    trash_log_path_txt = trash_object.info_txt_path
    trash_logging = trash_object.info_logging_path
    t_policy_s = trash_object.policy_size
    t_policy_t = trash_object.policy_time
    t_max_s = trash_object.maximum_size
    t_max_t = trash_object.maximum_time

    trash = smartrm_trash.Trash(trash_folder, trash_folder_info,
                                trash_log_path_txt,
                                t_policy_t, t_policy_s,
                                t_max_s,
                                DEFAULT_CONFIG['current_size'], DEFAULT_CONFIG['max_capacity'],
                                t_max_t,
                                q=None)
    trash_task_object.task_process = trash_task_object.INPROCESS
    trash_task_object.save()
    threading_smrm.define_task(trash_task_object, trash)
    time.sleep(3)
    trash_task_object.task_process = trash_task_object.DONE
    trash_task_object.save()

    trash_list = trash.watch_trash(dry_run=False)
    print 'do the task'
    print {"name": pk, "trash_list": trash_list}
    # return TaskList.as_view()
    return redirect('/task_list')


