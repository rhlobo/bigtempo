# -*- coding: utf-8 -*-


import re
import sys


def reload_modules(pattern):
    regex = re.compile(pattern)
    for module_name, module_instance in [(key, value) for key, value in sys.modules.items() if regex.match(key)]:
        if module_instance is None:
            continue
        reload(module_instance)
