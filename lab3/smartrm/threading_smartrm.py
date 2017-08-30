#! usr/bin/env python
# -*- coding: utf-8 -*-

import threading
# потом из file delete configurator копирнуть все функции, которые я потестила в консольной версии file delete configurator , ток не через if, а через отдельные функции

class WorkingThread(threading.Thread):
    def __init__(self, filename_list, filename_list_lock):
        super(WorkingThread, self).__init__()
        self.filename_list = filename_list
        self.filename_list_lock = filename_list_lock

    def run(self):
        while (True):
            next_filename = self.grab_next_filename()
            if next_filename is None:
                break
            self.retrieve_filename(next_filename)

    def grab_next_filename(self):
        self.filename_list_lock.acquire(1)  # start the lock section
        if len(self.filename_list) < 1:
            next_filename = None
        else:
            next_filename = self.filename_list[0]
            del self.filename_list[0]
        self.filename_list_lock.release()  # finish the lock section

        return next_filename

    def retrieve_filename(self, next_filename):
        # text = open(nexturl).read()
        # print text
        # print '################### %s #######################' % nexturl
        pass


def parallel_remove():
    pass


def parallel_restore():
    pass


def parallel_regex_remove():
    pass


def parallel_searching_directories():
    pass


def parallel_regex_restore():
    pass

# def parallel_regex_remove():
#     pass
#
# def parallel_regex_remove():
#     pass
