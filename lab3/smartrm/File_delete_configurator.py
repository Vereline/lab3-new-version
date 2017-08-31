#! usr/bin/env python
# -*- coding: utf-8 -*-

import json
import Smart_rm
import shutil         #Contains functions for operating files
import os
import sys
import Logwriter
import Argparser
import Trash
import re
import ExeptionListener
import pprint
import Regular
import Logger
import logging
import Config_parser
import threading


# rename here deleted file to the id
# -i - confirm every your deletion / restore
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


class RemoveThread(threading.Thread):
    def __init__(self, item, exit_codes, trash, dry_run, verbose, smartrm):
        super(RemoveThread, self).__init__()
        self.item = item
        self.e_c = exit_codes
        self.trash = trash
        self.dry_run = dry_run
        self.verbose = verbose
        self.smartrm = smartrm

    def run(self):
        self.smartrm.operate_with_removal(self.item, self.e_c, self.trash, self.dry_run, self.verbose)


class RemoveRegularThread(threading.Thread):
    def __init__(self, item, interactive, exit_codes, trash, dry_run, verbose, smartrm):
        super(RemoveRegularThread, self).__init__()
        self.item = item
        self.e_c = exit_codes
        self.trash = trash
        self.dry_run = dry_run
        self.verbose = verbose
        self.smartrm = smartrm
        self.trash = trash
        self.interactive = interactive

    def run(self):
        self.smartrm.operate_with_regex_removal(self.item, self.interactive, self.trash,
                                                self.e_c, self.dry_run, self.verbose)


class RemoveTrashItemThread(threading.Thread):
    def __init__(self, item, trash, dry_run, verbose):
        super(RemoveTrashItemThread, self).__init__()
        self.item = item
        self.trash = trash
        self.dry_run = dry_run
        self.verbose = verbose
        self.trash = trash

    def run(self):
        self.trash.delete_manually(self.item, self.dry_run, self.verbose)


class RestoreTrashItemThread(threading.Thread):
    def __init__(self, item, trash, dry_run, verbose):
        super(RestoreTrashItemThread, self).__init__()
        self.item = item
        self.trash = trash
        self.dry_run = dry_run
        self.verbose = verbose
        self.trash = trash

    def run(self):
        self.trash.restore_trash_manually(self.item, self.dry_run, self.verbose)


class FileDeleteConfigurator(object):
    def __init__(self, argparser, paths):
        self.argparser = argparser

        self.dry_run = False
        self.silent = False
        self.interactive = False
        self.verbose = False
        self.force = False

        if argparser.args.interactive:  # if there is no interactive, ask only if you have no roots
            self.interactive = True  # if there are many files, ask for every file
        if argparser.args.silent:
            self.silent = True
        if argparser.args.force:
            self.force = True
        if argparser.args.verbose:
            self.verbose = True
        if argparser.args.dryrun:
            self.dry_run = True

        if self.force or self.silent:
            self.interactive = False
            self.verbose = False

        self.exit_codes = {
            'success': 0,
            'conflict': 1,
            'error': 2,
            'no_file': 3
        }

        # load txt version as a user config after
        user_txt_path = '/home/vereline/Configure.txt'
        path = '/home/vereline/Configure.json'
        #
        # user_txt_path = os.path.split(sys.argv[0])[0] + '/Configure.txt'# 'smartrm/Configure.txt'
        try:
            # path = os.path.split(sys.argv[0])[0] + '/Configure.json'
            if not os.path.exists(path):
                try:
                    json_file = open(path, 'w')
                    json.dump(DEFAULT_CONFIG, json_file)
                    json_file.close()
                    # raise ExeptionListener.FileDoesNotExistException('config does not exist')
                except ExeptionListener.FileDoesNotExistException as ex:
                    print ex.msg
                    sys.exit(self.exit_codes['no_file'])
            self.config = json.load(open(path, 'r'))
            # self.config = json.load(open('smartrm/Configure.json', 'r'))
        except ExeptionListener.FileDoesNotExistException as ex:
            # logging.error(ex)  # check if this works before constructor
            print ex.msg
            sys.exit(self.exit_codes['no_file'])
        except Exception as ex:
            logging.error(ex.message)
            print ex.message
            sys.exit(self.exit_codes['no_file'])

        self.logger = Logger.Logger(self.config['trash_logging_path'], self.silent)

        try:
            if not os.path.exists(user_txt_path):
                try:
                    f = open(user_txt_path, 'w')
                    f.write('[Configs]\n')
                    for key in DEFAULT_CONFIG.keys():
                        f.write(("{key} = {value}\n".format(key=key, value=DEFAULT_CONFIG[key])))
                    f.close()
                    # raise ExeptionListener.FileDoesNotExistException('config does not exist')
                except ExeptionListener.FileDoesNotExistException as ex:
                    logging.error(ex.msg)
                    sys.exit(self.exit_codes['no_file'])
            self.config_parser = Config_parser.ConfParser(user_txt_path)
        except ExeptionListener.FileDoesNotExistException as ex:
            logging.error(ex.msg)
            sys.exit(self.exit_codes['no_file'])
        except Exception as ex:
            logging.error(ex.message)
            sys.exit(self.exit_codes['no_file'])

        self.change_configure_by_user_config()  # change config by the txt file
        self.change_configure()  # change config by the parsed command line

        try:
            # if critical - exit
            # if not critical - default settings(work in exceptionListener)
            self.trash = Trash.Trash(self.config['path'], self.config['trash_log_path'],
                                     self.config['trash_log_path_txt'],
                                     self.config['policy_time'], self.config['policy_size'], self.config['max_size'],
                                     self.config['current_size'], self.config['max_capacity'], self.config['max_time'],
                                     self.ask_for_confirmation)
        except ExeptionListener.FileDoesNotExistException as ex:
            # do not so broad exception
            # do closer exception
            logging.error('Unable to load trash')
            logging.error(ex.msg)
            sys.exit(self.exit_codes['error'])
        except Exception as ex:
            logging.error(ex.message)
            sys.exit(self.exit_codes['error'])

        try:
            self.smartrm = Smart_rm.SmartRm(self.config['path'], self.ask_for_confirmation)
        except ExeptionListener.FileDoesNotExistException as ex:
            logging.error('Unable to load smart rm')
            logging.error(ex.msg)
            sys.exit(self.exit_codes['error'])
        except Exception as ex:
            logging.error(ex.message)
            sys.exit(self.exit_codes['error'])

        self.paths = paths

    def define_action(self):
        logging.info('Define action')
        if self.argparser.args.remove is not None:

            # for item in self.paths:
            #     if self.interactive:
            #         answer = self.ask_for_confirmation(item)
            #         if not answer:
            #             continue
            #     self.smartrm.operate_with_removal(item, self.exit_codes, self.trash, self.dry_run, self.verbose)
            #     #############################
            removal_threads = []
            for item in self.paths:
                if self.interactive:
                    answer = self.ask_for_confirmation(item)
                    if answer:
                        new_thread = RemoveThread(item, self.exit_codes, self.trash, self.dry_run, self.verbose,
                                                  self.smartrm)
                        removal_threads.append(new_thread)
                        #continue
                else:
                    new_thread = RemoveThread(item, self.exit_codes, self.trash, self.dry_run, self.verbose,
                                              self.smartrm)
                    removal_threads.append(new_thread)
                    # continue

            for removal_thread in removal_threads:
                removal_thread.start()

            for removal_thread in removal_threads:
                removal_thread.join()
                #############################

        elif self.argparser.args.remove_regular is not None:
            # do here regular check
            for element in self.paths:
                items = Regular.define_regular_path(element)

                removal_threads = []

                for item in items:
                    # if self.interactive:
                    #     answer = self.ask_for_confirmation(item)
                    #     if answer:
                    new_thread = RemoveRegularThread(item, self.interactive, self.exit_codes, self.trash, self.dry_run,
                                                     self.verbose, self.smartrm)
                    removal_threads.append(new_thread)
                    # continue

                for removal_thread in removal_threads:
                    removal_thread.start()

                for removal_thread in removal_threads:
                    removal_thread.join()
                    ######################

            #
            # for element in self.paths:
            #     self.smartrm.operate_with_regex_removal(element, self.interactive, self.trash,
            #                                             self.exit_codes, self.dry_run, self.verbose)

        elif self.argparser.args.clean is not None:
            if self.interactive:  #?????
                answer = self.ask_for_confirmation('trash')
                if answer:
                    self.trash.delete_automatically(self.dry_run, self.verbose)

            else:
                self.trash.delete_automatically(self.dry_run, self.verbose)

        elif self.argparser.args.restore is not None:

            removal_threads = []
            for item in self.paths:
                if self.interactive:
                    answer = self.ask_for_confirmation(item)
                    if answer:
                        new_thread = RestoreTrashItemThread(item, self.trash, self.dry_run, self.verbose)
                        removal_threads.append(new_thread)
                        # continue
                else:
                    new_thread = RestoreTrashItemThread(item, self.trash, self.dry_run, self.verbose)
                    removal_threads.append(new_thread)
                    # continue

            for removal_thread in removal_threads:
                removal_thread.start()

            for removal_thread in removal_threads:
                removal_thread.join()
                #############################


                # for item in self.paths:
            #     if self.interactive:
            #         answer = self.ask_for_confirmation(item)
            #         if not answer:
            #             continue
            #     self.trash.restore_trash_manually(item, self.dry_run, self.verbose)

        elif self.argparser.args.restore_all is not None:
            if self.interactive:  #????
                answer = self.ask_for_confirmation('trash')
                if answer:
                    self.trash.restore_trash_automatically(self.dry_run, self.verbose)
                    # if self.verbose:
                    #     print 'trash restored'
            else:
                self.trash.restore_trash_automatically(self.dry_run, self.verbose)
                # if self.verbose:
                #     print 'trash restored'

        elif self.argparser.args.remove_from_trash is not None:
            removal_threads = []
            for item in self.paths:
                if self.interactive:
                    answer = self.ask_for_confirmation(item)
                    if answer:
                        new_thread = RemoveTrashItemThread(item, self.trash, self.dry_run, self.verbose)
                        removal_threads.append(new_thread)
                        # continue
                else:
                    new_thread = RemoveTrashItemThread(item, self.trash, self.dry_run, self.verbose)
                    removal_threads.append(new_thread)
                    # continue

            for removal_thread in removal_threads:
                removal_thread.start()

            for removal_thread in removal_threads:
                removal_thread.join()
                #############################

                # for item in self.paths:
            #     if self.interactive:
            #         answer = self.ask_for_confirmation(item)
            #         if not answer:
            #             continue
            #     self.trash.delete_manually(item, self.dry_run, self.verbose)
                # if self.verbose:
                #     print item + ' removed'

        elif self.argparser.args.clean_regular is not None:
            for item in self.paths:
                self.trash.clean_by_regular(item, self.dry_run, self.verbose, self.interactive)

        elif self.argparser.args.restore_regular is not None:

            for item in self.paths:
                self.trash.restore_by_regular(item, self.dry_run, self.interactive, self.verbose)

            return

        elif self.argparser.args.show_trash is not None:
            if self.interactive:
                answer = self.ask_for_confirmation('trash')
                if answer:
                    self.trash.watch_trash(self.dry_run)
            else:
                self.trash.watch_trash(self.dry_run)

        elif self.argparser.args.show_config is not None:
            if self.interactive:
                answer = self.ask_for_confirmation('config')
                if answer:
                    if self.dry_run:
                        print 'show config'
                    else:
                        pprint.pprint(self.config)
            else:
                if self.dry_run:
                    print 'show config'
                else:
                    pprint.pprint(self.config)

        logging.info('Check policies')
        self.trash.check_policy(self.dry_run, self.verbose)

    def ask_for_confirmation(self, filename):
        answer = raw_input('Operation with {filename}. Are you sure? [y/n]\n'.format(filename=filename))
        if answer == 'n' or answer == 'N':
            if not self.silent:
                print('Operation canceled')
            return False
        elif answer == 'y' or answer == 'Y':
            if not self.silent:
                print('Operation continued')
            return True
            # sys.exit(self.exit_codes['success'])
        elif answer != 'y' and answer != 'n' and answer != 'N' and answer != 'Y':
            self.ask_for_confirmation(filename)

    def check_access(self, path):
        logging.info('Check {file} access'.format(file=path))
        if os.access(path, os.R_OK):
            return self.exit_codes['success']
        else:
            logging.error('This is a system unit')
            # raise system directory exception
            # write this in logger
            return self.exit_codes['error']

    def change_configure(self):  # works
        if self.argparser.args.configs is not None:
            for config in self.argparser.args.configs:
                arr = config.split('=')
                if arr[0] in self.config.keys():
                    self.config[arr[0]] = arr[1]

    def change_configure_by_user_config(self):
        for key in self.config.keys():
            try:
                if self.config_parser.dict[key] is not None:
                    self.config[key] = self.config_parser.dict[key]
            except ExeptionListener.WrongItemException as ex:
                logging.ERROR(ex.msg)
            except Exception as ex:
                logging.error(ex.message)



