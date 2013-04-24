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


def get_test_data_files_path(test_filename, ls_filenames):
    result = []
    for s_filename in ls_filenames:
        result.append(get_test_data_file_path(test_filename, s_filename))
    return result


def get_test_data_file_path(test_filename, s_filename):
    return os.path.abspath(os.path.join(get_test_data_dir(test_filename), s_filename))


def get_test_data_dir(test_filename):
    return "%s_data" % (os.path.splitext(test_filename)[0])
