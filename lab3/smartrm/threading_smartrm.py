#! usr/bin/env python
# -*- coding: utf-8 -*-

import threading
import Trash
import Smart_rm
import multiprocessing
import time

AVAILABLE_TASKS = {
    'dbr': 'delete by regex',
    'dbf': 'delete by filename',
    'rat': 'recover all trash',
    'cat': 'clear all trash',
    'rmfft': 'remove files from trash',
    'rcfft': 'recover files from trash',
    'rmfftr': 'remove files from trash by regex',
    'rcfftr': 'recover files from trash by regex'
}

EXIT_CODES = {
            'success': 0,
            'conflict': 1,
            'error': 2,
            'no_file': 3
        }


def define_task(task, trash, lock):
    # lock = multiprocessing.Lock()

    elements = []

    current_task = task.file_task
    regex = task.regular
    smart_rm = Smart_rm.SmartRm(trash.path)

    elements.append(task.file_path)
    if current_task == AVAILABLE_TASKS['dbr']:
        smart_rm.operate_with_regex_removal(regex, trash, EXIT_CODES)

    elif current_task == AVAILABLE_TASKS['dbf']:
        smart_rm.operate_with_removal(elements, EXIT_CODES, trash)

    elif current_task == AVAILABLE_TASKS['rat']:
        trash.restore_trash_automatically()

    elif current_task == AVAILABLE_TASKS['cat']:
        trash.delete_automatically()

    elif current_task == AVAILABLE_TASKS['rmfft']:
        trash.delete_manually(elements)

    elif current_task == AVAILABLE_TASKS['rcfft']:
        trash.restore_trash_manually(elements)

    elif current_task == AVAILABLE_TASKS['rmfftr']:
        trash.clean_by_regular(regex)

    elif current_task == AVAILABLE_TASKS['rcfftr']:
        trash.restore_by_regular(regex)
    time.sleep(3)
    with lock:
        task.task_process = task.DONE
        task.save()


def manage_tasks(task, trash, another_trash_tasks, lock):
    with lock:
        # if trash.path = task.trash.name => task from all_tasks.waiting
        # and freeze the button (do it) in html

        for task in another_trash_tasks:
            task.task_process = task.WAITING
            task.save()

    define_task(task, trash, lock)
    # maybe bring it to the views.py
    # and all tasks do previous state(save it somewhere)
    # in the end do trash.not busy