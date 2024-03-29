#! usr/bin/env python
# -*- coding: utf-8 -*-

import threading
import smartrm.Trash as Trash
import smartrm.Smart_rm as Smart_rm
import smartrm.Logger as Logger
import logging
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


def define_task(task, trash, trash_object, lock):
    # lock = multiprocessing.Lock()
    return_code = EXIT_CODES['success']
    elements = []
    silent = task.silent  # redo for the trash_object.silent
    logger = Logger.Logger(trash_object.info_logging_path, silent)

    current_task = task.file_task
    regex = task.regular
    smart_rm = Smart_rm.SmartRm(trash.path)
    # print 'regex', regex
    # print 'current', current_task
    # print 'available', AVAILABLE_TASKS['rcfftr']

    elements.append(task.file_path)
    if current_task == AVAILABLE_TASKS['dbr']:
        return_code = smart_rm.operate_with_regex_removal(regex, trash, EXIT_CODES, task.file_path,
                                                          dry_run=task.dry_run, verbose=task.verbose)

    elif current_task == AVAILABLE_TASKS['dbf']:
        return_code = smart_rm.operate_with_removal(elements, EXIT_CODES, trash,
                                                    dry_run=task.dry_run, verbose=task.verbose)

    elif current_task == AVAILABLE_TASKS['rat']:
        return_code = trash.restore_trash_automatically(dry_run=task.dry_run, verbose=task.verbose)

    elif current_task == AVAILABLE_TASKS['cat']:
        return_code = trash.delete_automatically(dry_run=task.dry_run, verbose=task.verbose)

    elif current_task == AVAILABLE_TASKS['rmfft']:
        return_code = trash.delete_manually(elements, dry_run=task.dry_run, verbose=task.verbose)

    elif current_task == AVAILABLE_TASKS['rcfft']:
        return_code = trash.restore_trash_manually(elements, dry_run=task.dry_run, verbose=task.verbose)

    elif current_task == AVAILABLE_TASKS['rmfftr']:
        return_code = trash.clean_by_regular(regex, dry_run=task.dry_run, verbose=task.verbose)

    elif current_task == AVAILABLE_TASKS['rcfftr']:
        return_code = trash.restore_by_regular(regex, dry_run=task.dry_run, verbose=task.verbose)

    logging.info('Check policies')
    trash.check_policy(task.dry_run, verbose=task.verbose)

    with lock:
        trash_object.is_busy = False
        if return_code == EXIT_CODES['success']:
            task.task_process = task.DONE
        else:
            task.task_process = task.ERROR
        trash_object.save()
        task.save()


def manage_tasks(task, trash, trash_object, another_trash_tasks, tasks_statuses, lock):
    define_task(task, trash, trash_object, lock)

    # with lock:
    lock.acquire()
    for i in range(len(another_trash_tasks)):
        another_trash_tasks[i].task_process = tasks_statuses[i]
        another_trash_tasks[i].save()
    lock.release()

        # for task in another_trash_tasks:
        #     task.task_process = task.WAITING
        #     task.save()
