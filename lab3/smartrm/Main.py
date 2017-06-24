#! usr/bin/env python
# -*- coding: utf-8 -*-

import json
import argparse
from argparse import *
import Smart_rm
import shutil         #Contains functions for operating files
import os         #imports the os
import Logwriter
import Argparser
import Trash
import File_delete_configurator


def main():
    argparser = Argparser.Argparser()
    cmd = argparser.define_command_line()
    out_list = argparser.create_outlist(argparser.args, cmd)  # here are all the paths placed
    fdc = File_delete_configurator.FileDeleteConfigurator(argparser, out_list)
    fdc.define_action()

if __name__ == '__main__':
    main()

