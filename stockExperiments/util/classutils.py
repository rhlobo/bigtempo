

def instantiate(classes):
    return [clazz() for clazz in classes]


def get_all_subclasses(clazz):
    recursiveResult = []
    for subClazz in clazz.__subclasses__():
        recursiveResult.extend(get_all_subclasses(subClazz))
    return clazz.__subclasses__() + recursiveResult
