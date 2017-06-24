#! usr/bin/env python
# -*- coding: utf-8 -*-

import  logging
import Logger


class ExceptionListener(Exception):
    pass


class InvalidSizeError(ExceptionListener):
    def __init__(self, msg):
        self.msg = msg
# print 'size of file is bigger than the size of trash'
#  if the size of file is bigger than the size of trash


class FileDoesNotExistException(ExceptionListener):
    def __init__(self, msg):
        self.msg = msg
# print 'this file does not exist'
#  if the size of file is bigger than the size of trash


class ThisIsSystemDirectoryException(ExceptionListener):
    def __init__(self, msg):
        self.msg = msg
# print 'deleted file or directory is system'
#  if the deleted file or directory is system


class OverrideCapacityException(ExceptionListener):
    def __init__(self, msg):
        self.msg = msg
#  if the trash is full/else(not enough disk space)
# print 'not enough disk space'


class OverrideQuantityOfFilesException(ExceptionListener):
    def __init__(self, msg):
        self.msg = msg
#  checks if the quantity of files is big/bigger than in config
# print 'too many files in trash'


class DetectedCyclesException(ExceptionListener):
    def __init__(self, msg):
        self.msg = msg
# print 'cycles detected'


class CheckIfConflictException(ExceptionListener):
    def __init__(self, msg):
        self.msg = msg
# if in restore path this file already exists
# print 'conflict is detected'


class WrongItemException(ExceptionListener):
    def __init__(self, msg):
        self.msg = msg
# if the item /string is not correct


class TrashError(ExceptionListener):
    def __init__(self, msg):
        self.msg = msg
# errors in trash
