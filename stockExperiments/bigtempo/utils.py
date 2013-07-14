# -*- coding: utf-8 -*-


def assure_is_valid_set(obj):
    if not obj:
        obj = set()
    elif not isinstance(obj, set):
        try:
            obj = set(obj)
        except:
            obj = set()
    return obj


def slice(slicable, start=None, end=None):
    if start and end:
        return slicable[start:end]
    if start:
        return slicable[start:]
    if end:
        return slicable[:end]
    return slicable
