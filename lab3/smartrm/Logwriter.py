#! usr/bin/env python
# -*- coding: utf-8 -*-

import json
import os
from datetime import datetime
import sys
import codecs
import logging


class Logwriter(object):
    def __init__(self, path, txt_path):
        self.file_dict_arr = []  # what's in the trash
        self.file_dict = {}  # for temporary issues
        self.file_dict_path = path
        self.file_dict_path_txt = txt_path  # redo for path from config
        self.load_from_json()

    def create_file_dict(self, path):
        logging.info('Write data to json(create dict)')

        self.file_dict = self.write_file_dict(path)
        file_id = self.file_dict['id']
        self.file_dict_arr.append(self.file_dict)
        return file_id

    def write_file_dict(self, path):
        file_dict = {'path': path, 'id': str(datetime.now().__hash__()),
                     'date': datetime.strftime(datetime.now(), '%Y-%m-%d'),
                     'size': os.path.getsize(path)}
        if not os.path.isdir(path):
            name = os.path.split(path)
            file_dict['name'] = name[1]
            return file_dict
        elif os.path.isdir(path):
            index = 0
            for i in reversed(range(len(path))):
                if path[i] == '/':
                    index = i
                    break
            dirname = path[index+1:]
            file_dict['name'] = dirname
            file_list = []
            # d = os.listdir(path)
            # # print d
            # for item in d:
            #     subpath = os.path.join(path, item)
            #     if os.path.isdir(subpath):
            #         subfile = self.write_file_dict(subpath)
            #         file_list.append(subfile)
            #
            #     elif not os.path.isdir(subpath):
            #         subdict = self.write_file_dict(subpath)
            #         file_list.append(subdict)

            # tree = os.walk(path)
            # for d in tree:
            #     print ('\n')
            #     print d
            #     if d[2].__len__() != 0:
            #         for f in d[2]:
            #             subpath_f = os.path.join(d[0], f)  # формирование адреса
            #             subfile = self.write_json_log(subpath_f)
            #             file_list.append(subfile)
            #             print subfile
            #     if d[1].__len__() != 0:
            #         for dir in d[1]:
            #             subpath_d = os.path.join(d[0], dir)  # формирование адреса
            #             subdict = self.write_json_log(subpath_d)
            #             file_list.append(subdict)
            #             print subdict
            file_dict['content'] = file_list
        return file_dict

    def load_from_json(self):
        if os.path.exists(self.file_dict_path):
            with open(self.file_dict_path) as json_data:
                if os.path.getsize(self.file_dict_path) > 0:
                    self.file_dict_arr = json.load(json_data)
        else:
            self.file_dict_arr = []
            new_path = os.path.split(self.file_dict_path)
            if not os.path.exists(new_path[0]):
                os.makedirs(new_path[0])
            open(self.file_dict_path, 'w')

    def write_to_json(self, dry_run):
        if dry_run:
            print 'write data to json'
        else:
            json.dump(self.file_dict_arr, open(self.file_dict_path, 'w'))

    # ubrat eto
    def get_id_by_name(self, array, name):  # not checked
        file_id = ''

        for item in array:
                if item['name'] == name:
                    file_id = item['id']
                    break
                # elif item['content'] is not None:
                #     file_id = self.get_id_by_name(item['content'], name)

        return file_id

    # ubrat eto
    def get_id_by_path(self, array, path):  # not checked
        file_id = ''
        reload(sys)
        sys.setdefaultencoding('utf-8')

        for item in array:
                if item['path'] == path:
                    file_id = item['id']
                    break
                # elif item['content'] is not None:
                #     file_id = self.get_id_by_name(item['content'], path)

        return file_id

    def get_id(self, name):  # not checked
        return self.get_id_by_name(self.file_dict_arr, name)

    def get_id_path(self, path):
        return self.get_id_by_path(self.file_dict_arr, path)

    # ubrat eto
    def delete_by_id(self, array, file_id):  # not checked
        for item in array:
                if item['id'] == file_id:
                    array.pop(array.index(item))
                    break
                # elif item['content'] is not None:
                #     self.delete_by_id(item['content'], file_id)

    def delete_elem_by_id(self, file_id):
        self.delete_by_id(self.file_dict_arr, file_id)

    def get_path(self, file_id):  # not checked
        return self.get_path_by_id(self.file_dict_arr, file_id)

    # ubrat eto
    def get_path_by_id(self, array, file_id):  # not checked
        path = ''
        for item in array:
                if item['id'] == file_id:
                    return item['path']
                # elif item['content'] is not None:
                #     return self.get_path_by_id(item['content'], file_id)

    def get_name(self, file_id):  # not checked
        return self.get_name_by_id(self.file_dict_arr, file_id)

    # ubrat eto
    def get_name_by_id(self, array, file_id):  # not checked
        path = ''
        for item in array:
                if item['id'] == file_id:
                    return item['name']
                # elif item['content'] is not None:
                #     return self.get_path_by_id(item['content'], file_id)

    def get_date(self, file_id):  # not checked
        return self.get_date_by_id(self.file_dict_arr, file_id)

    # ubrat eto
    def get_date_by_id(self, array, file_id):  # not checked
        path = ''
        for item in array:
                if item['id'] == file_id:
                    return item['date']
                # elif item['content'] is not None:
                #     return self.get_path_by_id(item['content'], file_id)

    def write_to_txt(self, dry_run):  # not checked
        logging.info('Write to txt')
        if dry_run:
            print 'write data'
        else:
            try:
                if not os.path.exists(self.file_dict_path_txt):
                    dir_path = os.path.split(self.file_dict_path_txt)[0]
                    if not os.path.exists(dir_path):
                        os.makedirs(dir_path)
                txt_file = open(self.file_dict_path_txt, 'w')
                # reload(sys)
                # sys.setdefaultencoding('utf-8')

                # redo unicode utf-8
                for item in self.file_dict_arr:
                    txt_file.write(('Name:' + item['name']+'\n').encode('utf-8'))
                    txt_file.write(('Id:' + item['id']+'\n').encode('utf-8'))
                    txt_file.write(('Path:' + item['path']+'\n').encode('utf-8'))
                    txt_file.write(('Date:' + item['date']+'\n').encode('utf-8'))
                    txt_file.write('\n')
                txt_file.close()
            except IOError as io:
                logging.error(io.message)
            except Exception as ex:
                logging.error(ex.message)