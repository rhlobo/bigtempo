import pandas
import sources.cotahist as cotahist
import sources.pynvest as pynvest
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


class YahooCotationProvider(AbstractProvider):

    def __init__(self):
        AbstractProvider.__init__(self)
        self.mapping = [("open", 1), ("min", 3), ("max", 2), ("close", 4), ("volume", 5)]

    def load(self, s_symbol, da_start=None, da_end=None):
        ll_data = zip(*pynvest.historical_prices(s_symbol + ".SA", da_start, da_end))
        ts_index = ll_data[0][::-1]
        return [self.__createSeries(ll_data[i_index], ts_index, s_name) for s_name, i_index in self.mapping]

    def __createSeries(self, data, ts_index, s_name):
        return pandas.TimeSeries(data, index=ts_index, name=s_name)
