#! usr/bin/env python
# -*- coding: utf-8 -*-

import shutil         #Contains functions for operating files
import os         #imports the os
import re
import logging


def define_regular_path(path, path_of_regular_search):
    regular_expressions = validate_regular(path)
    # items = os.walk(os.path.abspath(os.curdir))
    # dir_paths = os.path.abspath(os.getcwd())

    dir_paths = path_of_regular_search
    files, dirs = get_data_from_directory(dir_paths)

    correct_regular_expressions = filter_items_by_regular(files, regular_expressions)
    correct_regular_expressions_dirs = filter_items_by_regular(dirs, regular_expressions)

    except_collisions(correct_regular_expressions_dirs, correct_regular_expressions)

    correct_regular_expressions.extend(correct_regular_expressions_dirs)
    # print 'correct expressions', correct_regular_expressions
    return correct_regular_expressions


def validate_regular(regular_expression):
    correct_regular_expression = []
    try:
        re.compile(regular_expression)
        correct_regular_expression.append(regular_expression)
        # print "correct expression", correct_regular_expression
    except:
        logging.error("Invalid regular expression {regexp}".format(regexp=regular_expression))

    return correct_regular_expression


def filter_items_by_regular(items, regular_expressions):
    filtered_items = []

    for item in items:
        # print "item before", item
        item_name = os.path.basename(item)
        # print 'basename', item_name
        for regular_expression in regular_expressions:
            if re.search(regular_expression, item_name) is not None:
                filtered_items.append(item)
                # print "item name", item
                break

    return filtered_items


def get_data_from_directory(directory, goto_links=False, info=False):
    files_in_directory = []
    dirs_in_directory = []

    for root, directories, files in os.walk(directory, topdown=goto_links):
        if info:
            logging.info('Scanning directory {directory_name}'.format(directory_name=root))
        for name in files:
            files_in_directory.append(os.path.abspath(os.path.join(root, name)))
        for name in directories:
            dirs_in_directory.append(os.path.abspath(os.path.join(root, name)))

    return files_in_directory, dirs_in_directory


def except_collisions(dirs, files):

    items_to_delete = []

    for dir in dirs:
        for _file in files:
            if dir in _file:
                # print 'dir', dir, 'in file', _file
                items_to_delete.append(_file)

    for dir in dirs:
        for dir2 in dirs:
            if (dir in dir2) and (dir != dir2):
                items_to_delete.append(dir)

    for item in items_to_delete:
        if item in files:
            files.remove(item)
        elif item in dirs:
            dirs.remove(item)

    # print "clean items", dirs, files
