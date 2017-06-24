#! usr/bin/env python
# -*- coding: utf-8 -*-

import shutil         #Contains functions for operating files
import os         #imports the os
import re
import logging


def define_regular_path(path):
    regular_expressions = validate_regular(path)
    # items = os.walk(os.path.abspath(os.curdir))
    dir_paths = os.path.abspath(os.getcwd())
    files, dirs = get_data_from_directory(dir_paths)
    correct_regular_expressions = filter_items_by_regular(files, regular_expressions)
    correct_regular_expressions_dirs = filter_items_by_regular(dirs, regular_expressions)
    correct_regular_expressions.extend(correct_regular_expressions_dirs)
    return correct_regular_expressions


def validate_regular(regular_expression):
    correct_regular_expression = []
    try:
        re.compile(regular_expression)
        correct_regular_expression.append(regular_expression)
    except:
        logging.error("Invalid regular expression {regexp}".format(regexp=regular_expression))

    return correct_regular_expression


def filter_items_by_regular(items, regular_expressions):
    filtered_items = []

    for item in items:
        item_name = os.path.basename(item)
        for regular_expression in regular_expressions:
            if re.search(regular_expression, item_name) is not None:
                filtered_items.append(item)
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

