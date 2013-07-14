# -*- coding: utf-8 -*-


import os
import re


def _path_sort(path):
    return path.lower()


def listdir(s_dir, s_regex=r'.*', f_sort=_path_sort):
    r_pattern = re.compile(s_regex, re.IGNORECASE)
    result = []

    for s_filename in os.listdir(s_dir):
        if r_pattern.search(s_filename):
            result.append(os.path.abspath(os.path.join(s_dir, s_filename)))

    return sorted(result, key=f_sort)


def get_test_data_files_path(test_filename, ls_filenames, test_filename_to_data_dir_function=None):
    result = []
    for s_filename in ls_filenames:
        result.append(get_test_data_file_path(test_filename, s_filename, test_filename_to_data_dir_function))
    return result


def get_test_data_file_path(test_filename, s_filename, test_filename_to_data_dir_function=None):
    conversion_function = test_filename_to_data_dir_function if test_filename_to_data_dir_function else get_test_data_dir
    return os.path.abspath(os.path.join(conversion_function(test_filename), s_filename))


def get_test_data_dir(test_filename):
    return '%s_data' % (os.path.splitext(test_filename)[0])


def get_commum_test_data_dir(test_filename, directory_name='data'):
    return os.path.join(os.path.dirname(test_filename), directory_name)
