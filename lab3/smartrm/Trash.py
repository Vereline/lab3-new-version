#! usr/bin/env python
# -*- coding: utf-8 -*-


import shutil  # Contains functions for operating files
import os  # imports the os
import Logwriter
from datetime import datetime
import logging
import Regular
import re
import ExeptionListener
import threading
import multiprocessing


class Trash(object):
    def __init__(self, path_trash, path_log_j, path_log_t, policy_time, policy_size, size, cur_size, capacity, time, q):
        self.path = path_trash
        if not os.path.exists(self.path):
            logging.info('Create a new trash in the {path}'.format(path=self.path))
            os.makedirs(self.path)
        self.log_writer = Logwriter.Logwriter(path_log_j, path_log_t)
        if policy_time == 'True':
            self.policy_time = True
        elif policy_time == 'False':
            self.policy_time = False
        else:
            self.policy_time = bool(policy_time)

        if policy_size == 'True':
            self.policy_size = True
        elif policy_size == 'False':
            self.policy_size = False
        else:
            self.policy_size = bool(policy_size)

        # self.policy_size = bool(policy_size)
        self.max_size = int(size)
        self.cur_size = int(cur_size)
        self.max_capacity = int(capacity)  # the max quantity of files in trash
        self.max_time = int(time)
        self.ask_for_confirmation = q
        self.lock = threading.Lock()

    def remove_item_from_trash_for_automatical(self, subpath, dict_contains):
        try:
            if dict_contains:
                if os.path.isdir(subpath):
                    shutil.rmtree(subpath)
                elif not os.path.isdir(subpath):
                    os.remove(subpath)

        except ExeptionListener.TrashError as ex:
            logging.error(ex.msg)
        except Exception as ex:
            logging.error(ex.message)

    def delete_automatically(self, dry_run=False, verbose=False):  # works
        # delete the whole trash
        logging.info("Clean the whole trash".format())
        remove_processes = []
        if dry_run:
            print 'clean trash'
        else:
            d = os.listdir(self.path)
            for item in d:  # DO HERE PARALLEL
                subpath = os.path.join(self.path, item)  # form the address
                dict_contains = False
                for _dict in self.log_writer.file_dict_arr:
                    if _dict['id'] == item:
                        dict_contains = True
                        break
                remove_proc = multiprocessing.Process(target=self.remove_item_from_trash_for_automatical,
                                                      args=(subpath, dict_contains,))
                remove_processes.append(remove_proc)

            for proc in remove_processes:
                proc.start()
            for proc in remove_processes:
                proc.join()

            if verbose:
                print 'trash cleaned'
            logging.info("Clean information about files".format())
            clean_json = open(self.log_writer.file_dict_path, 'w')
            clean_json.close()
            clean_txt = open(self.log_writer.file_dict_path_txt, 'w')
            clean_txt.close()

    def delete_manually(self, paths, dry_run=False, verbose=False, interactive=False):  # not checked
        # delete one file manually
        remove_processes = []
        for path in paths:
            if interactive:
                answer = self.ask_for_confirmation(path)
                if not answer:
                    continue
            files_id = self.search_for_all_files_with_this_name(path)  # some problems with functions defined
            if len(files_id) > 1:
                logging.warning('Found more than 1 file with name {name}'.format(name=path))
            elif len(files_id) <= 0:
                logging.warning('There is no such file or directory')
                continue

            for file_id in files_id:
                # file_id = self.log_writer.get_id(path)
                clean_path = self.get_path_by_id(file_id, self.path)
                ans = True
                if len(files_id) > 1:
                    logging.info('Restore {name}, id = {id}?'.format(name=path, id=file_id))
                    ans = self.ask_for_confirmation(path)
                if not ans:
                    continue
                try:
                    if os.path.isdir(clean_path):
                        # logging.info("Remove directory".format())
                        if dry_run:
                            print 'remove directory'
                        else:
                            if check_file_path(clean_path):
                                proc = multiprocessing.Process(target=shutil.rmtree,
                                                               args=(clean_path,))
                                remove_processes.append(proc)
                                #shutil.rmtree(clean_path)
                            else:
                                logging.error('File {n} with id {id} does not exist'.format(n=path, id=file_id))

                    elif not os.path.isdir(clean_path):
                        # logging.info("Remove file".format())
                        if dry_run:
                            print 'remove file'
                        else:
                            if check_file_path(clean_path):
                                proc = multiprocessing.Process(target=os.remove,
                                                               args=(clean_path,))
                                remove_processes.append(proc)
                                # os.remove(clean_path)
                            else:
                                logging.error('File {n} with id {id} does not exist'.format(n=path, id=file_id))
                        if verbose:
                            print 'item removed'
                    self.log_writer.delete_elem_by_id(file_id)
                    self.log_writer.write_to_json(dry_run)
                    self.log_writer.write_to_txt(dry_run)

                except ExeptionListener.TrashError as ex:
                    logging.error(ex.msg)
                except Exception as ex:
                    logging.error(ex.message)

        for proc in remove_processes:
            logging.info('Delete item from trash'.format())
            proc.start()
        for proc in remove_processes:
            proc.join()

    def get_path_by_id(self, file_id, path):  # not checked
        d = os.listdir(path)
        for item in d:
            subpath = os.path.join(path, item)  # form the address
            if file_id in subpath:
                return subpath

    def watch_trash(self, dry_run=False):  # works
        logging.info("Show trash".format())
        if dry_run:
            print 'show trash'
        else:
            if self.log_writer.file_dict_arr is [] or self.log_writer.file_dict_arr is None or self.log_writer.file_dict_arr.__len__() == 0:
                print 'trash bucket is empty'
                return self.log_writer.file_dict_arr
            else:
                txt_file = open(self.log_writer.file_dict_path_txt, 'r')
                print(txt_file.read())
                return self.log_writer.file_dict_arr

    def restore_trash_automatically(self, dry_run=False, verbose=False):  # not tested
        # restore the the whole trash
        logging.info("Restore the whole trash".format())
        paths = []
        if dry_run:
            print 'restore the whole trash'
        else:
            d = os.listdir(self.path)
            for item in d: # DO HERE PARRALEL
                subpath = os.path.join(self.path, item)  # form the address
                dict_contains = False
                for _dict in self.log_writer.file_dict_arr:
                    if _dict['id'] == item:
                        dict_contains = True
                        break
                try:
                    if dict_contains:
                        subpath = os.path.split(subpath)
                        # subpath = self.get_path_by_id(subpath[1], subpath[0])
                        logging.info("Restore item".format())
                        path = self.log_writer.get_name(subpath[1])  # START LOCK
                        paths.append(path)

                        # if verbose:
                        #     print 'item restored'
                except ExeptionListener.TrashError as ex:
                    logging.error(ex.msg)
                except Exception as ex:
                    logging.error(ex.message)

        self.restore_trash_manually(paths, dry_run, verbose, interactive_mode=False)

            # with
            # clean_json = open(self.log_writer.file_dict_path, 'w')
            # clean_json.close()
            # clean_txt = open(self.log_writer.file_dict_path_txt, 'w')
            # clean_txt.close()

    def restore_trash_manually(self, paths, dry_run=False, verbose=False, interactive_mode=False):  # works
        # restore one file in the trash
        # check if the path already exists
        restore_processes = []
        for path in paths:
            if interactive_mode:
                answer = self.ask_for_confirmation(path)
                if not answer:
                    continue

            files_id = self.search_for_all_files_with_this_name(path)
            if len(files_id) > 1:
                logging.warning('Found more than 1 file with name {name}'.format(name=path))
            elif len(files_id) <= 0:
                logging.warning('There is no such file or directory')
                continue
            for file_id in files_id:
                ans = True
                # file_id = self.log_writer.get_id(path)
                # file_id = os.path.split(path)[1]
                clean_path = self.get_path_by_id(file_id, self.path)
                destination_path = self.log_writer.get_path(file_id)
                new_name = self.log_writer.get_name(file_id)

                if len(files_id) > 1:
                    logging.info('Restore {name}, id = {id}?'.format(name=new_name, id=file_id))
                    ans = self.ask_for_confirmation(new_name)
                if not ans:
                    continue

                logging.info("Operations with file {file}".format(file=new_name))
                index = 0
                if not check_file_path(clean_path):
                    logging.error('File {name} with id {id} does not exist'.format(name=new_name, id=file_id))
                    self.log_writer.delete_elem_by_id(file_id)
                    self.log_writer.write_to_json(dry_run)
                    self.log_writer.write_to_txt(dry_run)
                    continue

                for i in reversed(range(len(clean_path))):
                    if clean_path[i] == '/':
                        index = i
                        break
                dirname = clean_path[:(index + 1)] + new_name
                logging.info("Rename {file}".format(file=new_name))

                if os.path.exists(destination_path):
                    logging.warning('Item with this name already exists.id will be added to real name')
                    destination_path += '_' + file_id

                if dry_run:
                    print 'rename file and move to original directory'
                    print 'clean record from json'
                else:
                    if check_file_path(clean_path):
                        restore_proc = multiprocessing.Process(target=move_file_into_original_destination,
                                                               args=(clean_path, dirname, destination_path, verbose, ))

                        restore_processes.append(restore_proc)
                    else:
                        logging.error('File {name} with id {id} does not exist'.format(name=new_name, id=file_id))
                    self.log_writer.delete_elem_by_id(file_id)
                    self.log_writer.write_to_json(dry_run)
                    self.log_writer.write_to_txt(dry_run)

        print 'parallel mode'
        for proc in restore_processes:
            proc.start()
        for proc in restore_processes:
            proc.join()

    def define_time_policy(self, dry_run, verbose):
        d = os.listdir(self.path)
        for item in d:
            subpath = os.path.join(self.path, item)  # form the address
            dict_contains = False
            for _dict in self.log_writer.file_dict_arr:
                if _dict['id'] == item:
                    dict_contains = True
                    break
            if dict_contains:
                # logging.info('time policy')
                confirm = self.check_date_if_overflow(subpath)
                if confirm:
                    self.delete_manually(subpath, dry_run, verbose)

    def check_policy(self, dry_run, verbose):  # not checked(redo to check the whole bucket)
        logging.info("Check policies".format())
        if self.policy_time:
            logging.info('time policy')
            self.define_time_policy(dry_run, verbose)
        if self.policy_size:
            logging.info('size policy')
            self.check_size(dry_run, verbose)

    def count_days(self, path):
        name = os.path.split(path)

        if name[1] != '':
            # file_id = self.log_writer.get_id(name[1])
            file_id = name[1]
            file_date = self.log_writer.get_date(file_id)
            file_name = self.log_writer.get_name(file_id)
            logging.info("Check the time policy of {item}".format(item=file_name))
            # cur_date = datetime.date.today()
            cur_date = datetime.now()
            # file_date = file_date.split('-')
            date_a = datetime.strptime(file_date, "%Y-%m-%d")
            # date_a = datetime.date(int(file_date[0]), int(file_date[1]), int(file_date[2]))

            days = cur_date - date_a
            days = days.days
        return days

    def check_date_if_overflow(self, path):
        time = self.count_days(path)
        if time > self.max_time:
            return True
        else:
            return False

    def check_size(self, dry_run=False, verbose=False):
        # logging.info("Check the size policy".format())
        if int(self.max_size) - self.count_size(dry_run) <= 0:
            if dry_run:
                print 'not enough trash space'
            elif not dry_run:
                self.delete_automatically(dry_run, verbose)

    def count_size(self, dry_run):  # not tested
        total_size = 0
        if dry_run:
            print 'count real size of the whole trash'

        d = os.listdir(self.path)
        for item in d:
            subpath = os.path.join(self.path, item)  # form the address
            dict_contains = False
            for _dict in self.log_writer.file_dict_arr:
                if _dict['id'] == item:
                    dict_contains = True
                    break

            if dict_contains:
                if os.path.isdir(subpath):
                    total_size += self.get_size(subpath)
                elif not os.path.isdir(subpath):
                    total_size += os.path.getsize(subpath)

        return total_size

    def get_size(self, start_path='.'):
        logging.info("Get the size of file in the trash".format())
        total_size = 0
        for dirpath, dirnames, filenames in os.walk(start_path):
            for f in filenames:
                fp = os.path.join(dirpath, f)
                total_size += os.path.getsize(fp)
        return total_size

    def search_for_all_files_with_this_name(self, name):  # not tested
        files_id = []
        for file_dict in self.log_writer.file_dict_arr:
            if file_dict['name'] == name:
                files_id.append(file_dict['id'])

        return files_id

    def get_names_by_regular(self, regex):  # not tested
        suitable_names = []
        suitable_id = []
        names = []
        files_id = []
        for file_dict in self.log_writer.file_dict_arr:
            names.append(file_dict['name'])
            files_id.append(file_dict['id'])
        try:
            re.compile(regex)
        except:
            logging.error("Invalid regular expression {regexp}".format(regexp=regex))
            # for name in names:
            #     if re.search(regex, name) is not None:
            #         suitable_names.append(name)
        try:
            for i in range(len(names)):
                if re.search(regex, names[i]) is not None:
                    suitable_names.append(names[i])
                    suitable_id.append(files_id[i])
        except ExeptionListener.TrashError as ex:
            logging.error(ex.msg)
        except TypeError as ex:
            logging.error(ex.message)

        return suitable_names, suitable_id

    def restore_by_regular(self, regex, dry_run=False, interactive=False, verbos=False):  # not tested
        restore_processes = []
        names, ids = self.get_names_by_regular(regex)
        for file_id in ids:
            clean_path = self.get_path_by_id(file_id, self.path)
            destination_path = self.log_writer.get_path(file_id)
            new_name = self.log_writer.get_name(file_id)
            logging.info("Operations with file {file}".format(file=new_name))
            index = 0
            if not check_file_path(clean_path):
                logging.error('File {n} with id {id} does not exist'.format(n=new_name, id=file_id))
                self.log_writer.delete_elem_by_id(file_id)
                self.log_writer.write_to_json(dry_run)
                self.log_writer.write_to_txt(dry_run)
                continue

            for i in reversed(range(len(clean_path))):
                if clean_path[i] == '/':
                    index = i
                    break

            dirname = clean_path[:(index + 1)] + new_name
            logging.info("Rename {file}".format(file=new_name))
            logging.info("Move to original directory {file}".format(file=new_name))

            if os.path.exists(destination_path):
                logging.warning('Item with this name already exists.id will be added to real name')
                destination_path += '_' + file_id
            if dry_run:
                print 'rename file and move to original directory'
                print 'clean record from json'
            else:
                if interactive:
                    ans = self.ask_for_confirmation(new_name)
                    if ans:
                        try:
                            if check_file_path(clean_path):
                                proc = multiprocessing.Process(target=move_file_into_original_destination,
                                                               args=(clean_path, dirname, destination_path, verbose,))
                                restore_processes.append(proc)
                                # os.rename(clean_path, dirname)
                                # shutil.move(dirname, destination_path)
                            else:
                                logging.error('Item {n} with id {id} does not exist'.format(n=new_name, id=file_id))
                            # os.rename(clean_path, dirname)
                            # shutil.move(dirname, destination_path)
                            self.log_writer.delete_elem_by_id(file_id)
                            self.log_writer.write_to_json(dry_run)
                            self.log_writer.write_to_txt(dry_run)
                            if verbose:
                                print 'item restored'
                        except ExeptionListener.TrashError as ex:
                            logging.error(ex.msg)
                        except Exception as ex:
                            logging.error(ex.message)
                else:
                    try:
                        if check_file_path(clean_path):
                            proc = multiprocessing.Process(target=move_file_into_original_destination,
                                                           args=(clean_path, dirname, destination_path, verbose,))
                            restore_processes.append(proc)
                            # os.rename(clean_path, dirname)
                            # shutil.move(dirname, destination_path)
                        else:
                            logging.error('Item {n} with id {id} does not exist'.format(n=new_name, id=file_id))
                        # os.rename(clean_path, dirname)
                        # shutil.move(dirname, destination_path)
                        self.log_writer.delete_elem_by_id(file_id)
                        self.log_writer.write_to_json(dry_run)
                        self.log_writer.write_to_txt(dry_run)
                        if verbose:
                            print 'item restored'
                    except ExeptionListener.TrashError as ex:
                        logging.error(ex.msg)
                    except Exception as ex:
                        logging.error(ex.message)

        for proc in restore_processes:
            proc.start()
        for proc in restore_processes:
            proc.join()

    def clean_by_regular(self, regex, dry_run=False, verbose=False, interactive=False):  # not tested
        names, ids = self.get_names_by_regular(regex)
        # do here not cycle but parallel
        clean_processes = []
        for file_id in ids:
            clean_path = self.get_path_by_id(file_id, self.path)
            name = self.log_writer.get_name(file_id)
            answer = None
            if interactive:
                answer = self.ask_for_confirmation(name)
            if (answer is not None) and (answer is False):
                continue
            if os.path.isdir(clean_path):
                # logging.info("Remove directory {item}".format(item=name))
                if not dry_run:
                    if verbose:
                        print 'remove item'
                    if check_file_path(clean_path):
                        proc = multiprocessing.Process(target=shutil.rmtree, args=(clean_path,))
                        clean_processes.append(proc)
                        # shutil.rmtree(clean_path)
                    else:
                        logging.error('Directory {n} with id {id} does not exist'.format(n=name, id=file_id))
                    self.log_writer.delete_elem_by_id(file_id)
                    self.log_writer.write_to_json(dry_run)
                    self.log_writer.write_to_txt(dry_run)
                else:
                    print 'remove item'
            elif not os.path.isdir(clean_path):
                # logging.info("Remove file {item}".format(item=name))
                if not dry_run:
                    if verbose:
                        print 'remove item'
                    if check_file_path(clean_path):
                        proc = multiprocessing.Process(target=os.remove, args=(clean_path,))
                        clean_processes.append(proc)
                        # os.remove(clean_path)
                    else:
                        logging.error('File {n} with id {id} does not exist'.format(n=name, id=file_id))
                    self.log_writer.delete_elem_by_id(file_id)
                    self.log_writer.write_to_json(dry_run)
                    self.log_writer.write_to_txt(dry_run)
                else:
                    print 'remove item'

        for proc in clean_processes:
            logging.info('Remove item')
            proc.start()

        for proc in clean_processes:
            proc.join()


def move_file_into_original_destination(clean_path, dirname, destination_path, verbose):
    ###
    logging.info("Move to original directory {file}".format(file=clean_path))
    os.rename(clean_path, dirname)
    shutil.move(dirname, destination_path)
    if verbose:
        print 'item restored'
    ###


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


def check_file_path(path):
    # if not self.silent:
    logging.info('Check if the path is correct')
    # if the file is already not existing for the delete function or the file exists for restore
    if path is None:
        return False
    if os.path.exists(path):
        return True
    else:
        return False
