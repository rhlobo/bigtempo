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
