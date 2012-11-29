import data.cotahist.cotahist as cotahist
from base import *


class CotahistProvider(AbstractProvider):

    def __init__(self, c_dataMap):
        AbstractProvider.__init__(self)
        self.c_dataMap = c_dataMap

    def load(self, s_symbol):
        c_dataFrame = self.c_dataMap.get(s_symbol)
        if len(c_dataFrame) == 0:
            self.__importData()
        return c_dataFrame

    def __importData(self):
        la_quote = cotahist.importData()
        for s_symbol, date, f_open, f_min, f_max, f_close, i_vol in la_quote:
            c_dataFrame = self.c_dataMap.get(s_symbol)
            c_dataFrame[date] = (date, f_open, f_min, f_max, f_close, i_vol)
