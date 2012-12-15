import pandas
import sources.pynvest as pynvest
from base import *


class YahooCotationProvider(RawProvider):

    def __init__(self):
        RawProvider.__init__(self)
        self.mapping = [("open", 1), ("min", 3), ("max", 2), ("close", 4), ("volume", 5)]

    def load(self, s_symbol, da_start=None, da_end=None):
        ll_data = zip(*pynvest.historical_prices(s_symbol + ".SA", da_start, da_end))
        ts_index = ll_data[0][::-1]
        #return {s_name: self.__createSeries(ll_data[i_columnIndex], ts_index, s_name) for s_name, i_columnIndex in self.mapping}
        return dict((s_name, self.__createSeries(ll_data[i_columnIndex], ts_index, s_name)) for s_name, i_columnIndex in self.mapping)

    def __createSeries(self, data, ts_index, s_name):
        return pandas.TimeSeries(data, index=ts_index, name=s_name)
