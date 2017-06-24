#! usr/bin/env python
# -*- coding: utf-8 -*-

import argparse

import shutil         #Contains functions for operating files
import os         #imports the os
import sys
import re
import logging


class Argparser(object):
    def __init__(self, arguments_string=''):
        self.parser = self.add_parser()
        if arguments_string != '':
            splited_arguments_string = arguments_string.split(' ')
            self.args = self.parser.parse_args(splited_arguments_string)
        else:
            self.args = self.parser.parse_args()

    def add_parser(self):
        parser = argparse.ArgumentParser()

        parser.add_argument('-smrm', nargs='*', dest='remove', help='remove file or directory')
        parser.add_argument('-smrmr', nargs='*', dest='remove_regular', help='remove file or directory by regular')
        parser.add_argument('-smtrc', nargs='*', dest='clean', help='clean trash')
        parser.add_argument('-smtrr', nargs='*', dest='restore', help='restore 1 item in trash')
        parser.add_argument('-smtrra', nargs='*', dest='restore_all', help='restore all items in trash')
        parser.add_argument('-smtrrm', nargs='*', dest='remove_from_trash', help='remove from trash')
        parser.add_argument('-smtrs', nargs='*', dest='show_trash', help='show trash')
        parser.add_argument('-smcs', nargs='*', dest='show_config', help='show config')

        parser.add_argument('-smtrcr', nargs='*', dest='clean_regular', help='clean from trash by regular')
        parser.add_argument('-smtrrr', nargs='*', dest='restore_regular', help='restore from trash by regular')

        parser.add_argument('-i', '-interactive', dest='interactive', action='store_true', help='interactive mode')
        parser.add_argument('-f', '-force', dest='force', action='store_true', help='force mode')
        parser.add_argument('-v', '-verbose', dest='verbose', action='store_true', help='verbose mode')
        parser.add_argument('-s', '-silent', dest='silent', action='store_true', help='silent mode')
        parser.add_argument('-d', '-dryrun', dest='dryrun', action='store_true', help='dry-run mode')

        parser.add_argument('path', nargs='*', help='path of file or directory')
        parser.add_argument('--configs', dest='configs', nargs='*', help='configurations for 1 run')

        # -smrm - remove
        # -smrmr - remove regular
        # -smtrc - trash clean
        # -smtrr - trash restore
        # -smtrs - trash show
        # -smcs  - config show
        #
        # -i - interactive
        # -v - verbose
        # -f - force
        # -s - silent
        # -d - dryrun
        #
        # path - path of file/directory
        # configs - change configs for 1 time

        return parser

    def define_command_line(self):
        return sys.argv[1:]

    def define_path(self, rm_file):
        if os.path.exists(rm_file):
            return os.path.abspath(os.path.expanduser(rm_file)) #  rm_file
        if rm_file.find('/') == -1:
            path = os.path.abspath(rm_file)
            # path = os.path.abspath(os.getcwd()+'/()'.format(rm_file))
        else:
            path = os.path.abspath(os.path.expanduser(rm_file))
        return path

    def create_outlist(self, args, command):
        outlist = []
        if args.remove_regular is not None:
            for item in args.remove_regular:
                outlist.append(item)
            for item in args.path:
                outlist.append(item)

        elif args.remove is not None:
            for item in args.remove:
                outlist.append(self.define_path(item))
            for item in args.path:
                outlist.append(self.define_path(item))

        elif args.restore is not None:
            for item in args.restore:
                outlist.append(item)
            for item in args.path:
                outlist.append(item)

        elif args.restore_regular is not None:
            for item in args.restore_regular:
                outlist.append(item)
            for item in args.path:
                outlist.append(item)

        elif args.clean_regular is not None:
                for item in args.clean_regular:
                    outlist.append(item)
                for item in args.path:
                    outlist.append(item)

        elif args.remove_from_trash is not None:
                for item in args.remove_from_trash:
                    outlist.append(item)
                for item in args.path:
                    outlist.append(item)

        return outlist

