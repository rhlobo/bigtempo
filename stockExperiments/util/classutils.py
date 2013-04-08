import re


def instantiate(classes, *args):
    return [clazz(*args) for clazz in classes]


def get_all_subclasses(clazz, s_filter=r'.*'):
    r_pattern = re.compile(s_filter, re.IGNORECASE)

    recursiveResult = []
    for subClazz in clazz.__subclasses__():
        if r_pattern.match(subClazz.__name__):
            recursiveResult.append(subClazz)
        recursiveResult.extend(get_all_subclasses(subClazz, s_filter))

    return recursiveResult
