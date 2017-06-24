#! usr/bin/env python
# -*- coding: utf-8 -*-


import ConfigParser
import logging
import ExeptionListener
import sys


class ConfParser(object):
    def __init__(self, path):
        self.parser = ConfigParser.ConfigParser()
        self.dict = {}
        self.parser.read(path)
        self.sections = self.parser.sections()
        self.define_config_section(self.sections[0])

    def define_config_section(self, section):
        options = self.parser.options(section)
        for option in options:
            try:

                self.dict[option] = self.parser.get(section, option).decode('utf8')
                if self.dict[option] == -1:
                    logging.DEBUG("skip: %s", option)
                    # DebugPrint("skip: %s" % option)
            except ExeptionListener.WrongItemException as ex:
                logging.ERROR(ex)
                # logging.ERROR("exception on %s!" % option)
                self.dict[option] = None
            except Exception as ex:
                logging.error(ex)
