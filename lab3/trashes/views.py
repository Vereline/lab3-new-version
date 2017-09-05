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
    success_url = reverse_lazy('main')
    template_name = 'add_task.html'
    model = TaskToDo
    form_class = TaskForm
    # fields = ('file_path', 'file_task', 'info_path', 'force', 'dry_run', 'silent',
    #           'task_is_done', 'maximum_time', 'maximum_size', 'trash', 'regular',)


class RefreshTask(UpdateView):
    success_url = reverse_lazy('main')
    template_name = "refresh_task.html"
    model = TaskToDo
    fields = ('name', 'file_path', 'file_task', 'info_path', 'force', 'dry_run', 'silent',
              'maximum_time', 'maximum_size', 'trash', 'regular', )


class DeleteTask(DeleteView):
    success_url = reverse_lazy('main')
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

    trash = smartrm_trash.Trash(trash_folder, trash_folder_info,
            DEFAULT_CONFIG['trash_log_path_txt'],
            DEFAULT_CONFIG['policy_time'], DEFAULT_CONFIG['policy_size'], DEFAULT_CONFIG['max_size'],
            DEFAULT_CONFIG['current_size'], DEFAULT_CONFIG['max_capacity'], DEFAULT_CONFIG['max_time'],
            q=None)

    # trash_path = os.path.join(trash_object.path, "trash")
    # info_path = os.path.join(trash_object.path, "info")

    # trash_policy(trash_path, info_path, trash_object.policy, trash_object.savetime, trash_object.maxsize)
    trash_list = trash.watch_trash(dry_run=False)  # smartrm.show_trash_(trash_path, 0, dry=False)
    print "!!!!!!!!!!!!!!!!!!!!!!!!!!!1"
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

    print trash
    path = request.POST.getlist('file')
    print 'START PATH'
    print path
    print 'END PATH'
    info_path = os.path.join(trash_object.path, "info")
    print 'REMOVE'
    my_names = []
    for item in path:
        for element in item:
            pass
        # my_names.append(item['name'])
    # trash.delete_manually(my_names, False, False, False)  # do dry_run=false
    #smartrm.remove(path, trash_path, info_path, dry=False)
    return define_action(request, name)


def recover_file(request, name):
    trash_object = get_object_or_404(Trash, name=name)
    trash_path = os.path.join(trash_object.path, "trash")
    path = request.POST.getlist('file')
    print path
    info_path = os.path.join(trash_object.path, "info")
    print 'RESTORE OR RECOVER'
    #smartrm.recover(path, trash_path, info_path, dry=False)
    return define_action(request, name)


# do here queue of tasks(or what??!???!?!)
# do te status of tasks

# task_status=['done', 'created', 'expecting']

def do_the_task(request, pk): #################? do define action for tasks

    print 'do the task'
    print pk
    trash_task_object = get_object_or_404(TaskToDo, pk=pk)
    print trash_task_object
    print 'do the task'
    trash = trash_task_object.trash

    # works
    #
    # trash_task_object.task_process = trash_task_object.DONE
    # trash_task_object.save()
    #

    trash_folder = trash.path
    print 'do the task'
    trash_folder_info = trash.info_path
    # add_trash(trash_fold)
    print 'do the task'
    trash = smartrm_trash.Trash(trash_folder, trash_folder_info,
                                DEFAULT_CONFIG['trash_log_path_txt'],
                                DEFAULT_CONFIG['policy_time'], DEFAULT_CONFIG['policy_size'],
                                DEFAULT_CONFIG['max_size'],
                                DEFAULT_CONFIG['current_size'], DEFAULT_CONFIG['max_capacity'],
                                DEFAULT_CONFIG['max_time'],
                                q=None)

    # trash_path = os.path.join(trash_object.path, "trash")
    # info_path = os.path.join(trash_object.path, "info")

    # trash_policy(trash_path, info_path, trash_object.policy, trash_object.savetime, trash_object.maxsize)
    trash_list = trash.watch_trash(dry_run=False)  # smartrm.show_trash_(trash_path, 0, dry=False)
    print 'do the task'
    print {"name": pk, "trash_list": trash_list}
    # return TaskList.as_view()
    return redirect('/task_list')
    # return render(request, "task_list.html")


    # trash_object = get_object_or_404(Trash, name=name)
    # trash_path = os.path.join(trash_object.path, "trash")
    # path = request.POST.getlist('file')
    # print path
    # info_path = os.path.join(trash_object.path, "info")
    # print 'do this task'
    # #smartrm.recover(path, trash_path, info_path, dry=False)
    # return do_the_task(request, name)

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
