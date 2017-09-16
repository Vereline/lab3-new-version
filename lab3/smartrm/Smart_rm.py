#! usr/bin/env python
# -*- coding: utf-8 -*-

import logging
import multiprocessing
import os  # imports the os
import shutil  #  Contains functions for operating files

import ExeptionListener
import Regular


class SmartRm(object):
    def __init__(self, path, q=None):
        self.trash_path = path
        self.exception_listener = ExeptionListener.ExceptionListener
        self.ask_for_confirmation = q
        self.lock = multiprocessing.Lock()

    def operate_with_removal(self, items, exit_codes, trash, dry_run=False, verbose=False, interactive=False):
        return_code = exit_codes['success']
        removal_processes = []

        semaphore = multiprocessing.Semaphore(multiprocessing.cpu_count() * 2)

        for item in items:
            if interactive:
                answer = self.ask_for_confirmation(item)
                if not answer:
                    continue
            exists = check_file_path(item)
            if not exists:
                logging.error('File {file} does not exist'.format(file=item))
                return_code = exit_codes['no_file']
            else:
                access = check_access(exit_codes, item)
                if access == exit_codes['error']:
                    logging.error('Item {file} is a system unit'.format(file=item))
                    return_code = exit_codes['error']
                else:
                    # print item
                    file_id = trash.log_writer.create_file_dict(item)
                    item = rename_file_name_to_id(item, file_id, dry_run)
                    trash.log_writer.write_to_json(dry_run)
                    trash.log_writer.write_to_txt(dry_run)

                    rem_process = multiprocessing.Process(target=self.remove_to_trash_file,
                                                          args=(item, dry_run, verbose, semaphore))
                    removal_processes.append(rem_process)

        for rem_process in removal_processes:
            rem_process.start()
        for rem_process in removal_processes:
            rem_process.join()

        return return_code

    def operate_with_regex_removal(self, element, trash, exit_codes, path_of_regular_search,
                                   dry_run=False, verbose=False, interactive=False):
        items = Regular.define_regular_path(element, path_of_regular_search)
        remove_processes = []
        return_code = exit_codes['success']

        semaphore = multiprocessing.Semaphore(multiprocessing.cpu_count() * 2)

        if len(items) < 1:
            return_code = exit_codes['error']
        for item in items:
            if interactive:
                answer = self.ask_for_confirmation(item)
                if not answer:
                    continue
            exists = check_file_path(item)
            if not exists:
                logging.error('File {file} does not exist'.format(file=item))
                return_code = exit_codes['no_file']
            else:
                access = check_access(exit_codes, item)
                if access == exit_codes['error']:
                    logging.error('Item {file} is a system unit'.format(file=item))
                    return_code = exit_codes['error']
                else:
                    file_id = trash.log_writer.create_file_dict(item)
                    item = rename_file_name_to_id(item, file_id, dry_run)
                    trash.log_writer.write_to_json(dry_run)
                    trash.log_writer.write_to_txt(dry_run)
                    rem_process = multiprocessing.Process(target=self.remove_to_trash_file,
                                                          args=(item, dry_run, verbose, semaphore,))
                    remove_processes.append(rem_process)

        for rem_process in remove_processes:
            rem_process.start()
        for rem_process in remove_processes:
            rem_process.join()

        return return_code

    def remove_to_trash_file(self, path, dry_run, verbose, semaphore):  # works
        with semaphore:
            # print 'with semaphore'
            logging.info(multiprocessing.current_process())
            logging.info('Remove {path}'.format(path=path))
            try:
                if not dry_run:
                    # head, tail = os.path.split(path)
                    # new_path = os.path.join(self.trash_path, tail)
                    shutil.move(path, self.trash_path)
                    # return new_path
                else:
                    print 'remove file'
                if verbose:
                    print path + ' removed'
            except ExeptionListener.WrongItemException as ex:
                logging.error(ex.msg)
            except Exception as ex:
                logging.error(ex.message)


def check_file_path(path):
    # if not self.silent:
    logging.info('Check if the path is correct')
    # if the file is already not existing for the delete function or the file exists for restore
    if os.path.exists(path):
        return True
    else:
        return False


def rename_file_name_to_id(path, file_id, dry_run):  # works
    print path
    logging.info('Rename item with id')
    # _id = self.trash.log_writer.get_id_path(path)
    _id = file_id
    index = 0
    for i in reversed(range(len(path))):
        if path[i] == '/':
            index = i
            break

    directory_name = path[:(index+1)] + _id

    if dry_run:
        print 'rename file name to id'
    else:
        os.rename(path, directory_name)
    return directory_name


def ask_for_confirmation(filename, silent=False):
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


def check_access(exit_codes, path):
    logging.info('Check {file} access'.format(file=path))
    if os.access(path, os.R_OK):
        return exit_codes['success']
    else:
        logging.error('This is a system unit')
        # raise system directory exception
        # write this in logger
        return exit_codes['error']
