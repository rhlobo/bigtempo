import os
import bovespaparser.bovespaparser as bp


def importData():
    return __parseFile(__getFilepath('COTAHIST_A2011.txt'))


def __parseFile(filename):
    with open(filename, 'rU') as f:
        return bp.parsedata(f)


def __getFilepath(name):
    path = os.path.split(__file__)[0]
    return os.path.join(os.path.join(path, "data"), name)
