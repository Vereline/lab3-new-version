# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.shortcuts import render
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from .models import Trash, TaskToDo
from django.shortcuts import get_object_or_404, render, redirect, HttpResponse
import os
import smartrm.Trash as smartrm_trash
#import smartrm.Smart_rm as smart_rm
# from smartrm.Trash import Trash
import smartrm.Logger as Logger
import logging
from .forms import TrashForm, TaskForm
from django.urls import reverse_lazy
import json
import ast
import smartrm.threading_smartrm as threading_smrm
import time
import multiprocessing

# Create your views here.


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


def define_action(request, pk):
    trash_object = get_object_or_404(Trash, pk=pk)
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
                                q=ask_for_confirmation("trash"))
    # trash_path = os.path.join(trash_object.path, "trash")
    # info_path = os.path.join(trash_object.path, "info")

    trash_list = trash.watch_trash()
    print {"pk": pk, "trash_list": trash_list}
    return render(request, "define_action.html", {"pk": pk, "trash_list": trash_list})


def remove_file(request, pk):
    trash_object = get_object_or_404(Trash, pk=pk)
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
                                q=ask_for_confirmation("trash"))

    # print trash
    path = request.POST.getlist('file')
    # info_path = os.path.join(trash_object.path, "info")

    # REDO REDO REDO

    # print 'REMOVE'
    my_names = []
    my_ids = []
    for item in path:
        s = ast.literal_eval(item)  # str to dict
        my_names.append(s['name'])
        my_ids.append(s['id'])

        # s = item.encode('utf-8')
        # info_dict = json.loads(item)  # problems with double quotes

    trash.delete_manually(my_names, my_ids)
    logging.info('Check policies')
    trash.check_policy(dry_run=False, verbose=True)
    return define_action(request, pk)


def recover_file(request, pk):
    trash_object = get_object_or_404(Trash, pk=pk)
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
                                DEFAULT_CONFIG['current_size'],
                                DEFAULT_CONFIG['max_capacity'],
                                t_max_t,
                                q=ask_for_confirmation("trash"))

    print trash
    path = request.POST.getlist('file')

    my_names = []
    my_ids = []
    for item in path:
        s = ast.literal_eval(item)  # str to dict
        my_names.append(s['name'])
        my_ids.append(s['id'])


    logger = Logger.Logger(trash_object.info_logging_path, silent=False)
    trash.restore_trash_manually(my_names, custom_ids=my_ids)
    logging.info('Check policies')
    trash.check_policy(dry_run=False, verbose=True)
    return define_action(request, pk)


def do_the_task(request, pk):

    print 'do the task'
    print pk
    trash_task_object = get_object_or_404(TaskToDo, pk=pk)
    print trash_task_object
    print 'do the task'
    trash_object = trash_task_object.trash
    all_tasks = list(TaskToDo.objects.all())

    all_tasks.remove(trash_task_object)
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
                                q=ask_for_confirmation("trash"))
                                # q=None)

    lock = multiprocessing.Lock()
    waiting_tasks = []
    waiting_tasks_previous_statuses = []

    with lock:
        trash_task_object.task_process = trash_task_object.INPROCESS
        trash_task_object.save()
        trash_object.is_busy = True
        trash_object.save()
        for task in all_tasks:
            if (task.trash == trash_task_object) or task.trash.is_busy:
                waiting_tasks_previous_statuses.append(task.task_process)
                task.task_process = task.WAITING
                task.save()
                waiting_tasks.append(task)

    # myproc = multiprocessing.Process(target=threading_smrm.define_task, args=(trash_task_object, trash, lock))
    myproc = multiprocessing.Process(target=threading_smrm.manage_tasks, args=(trash_task_object, trash, trash_object,
                                                                               waiting_tasks,
                                                                               waiting_tasks_previous_statuses, lock,))
    myproc.start()

    trash_list = trash.watch_trash()
    print 'do the task'
    print {"name": pk, "trash_list": trash_list}
    # return TaskList.as_view()
    return redirect('/task_list')


def ask_for_confirmation(filename, silent=False, answer='Y'):
    if answer is None:
        answer = raw_input('Operation with {filename}. Are you sure? [y/n]\n'.format(filename=filename))
    if answer == 'n' or answer == 'N':
        if not silent:
            print('Operation canceled')
        return False
    elif answer == 'y' or answer == 'Y':
        if not silent:
            print('Operation continued')
        return True
        # sys.exit(self.exit_codes['success'])
    elif answer != 'y' and answer != 'n' and answer != 'N' and answer != 'Y':
        ask_for_confirmation(filename)
