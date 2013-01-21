import os
import bovespaparser.bovespaparser as bp


def importData():
    return _parseFile(_getFilepath('COTAHIST_A2011.txt'))


def _parseFile(filename):
    with open(filename, 'rU') as f:
        return bp.parsedata(f)


def _getFilepath(name):
    path = os.path.split(__file__)[0]
    return os.path.join(os.path.join(path, "data"), name)


class CotahistImporter(object):

    def __init__(self, c_dataMap):
        self.c_dataMap = c_dataMap

    def importData(self):
        la_quote = importData()
        for s_symbol, date, f_open, f_low, f_high, f_close, i_vol in la_quote:
            c_dataFrame = self.c_dataMap.get(s_symbol)
            c_dataFrame[date] = [date, f_open, f_high, f_low, f_close, i_vol]
