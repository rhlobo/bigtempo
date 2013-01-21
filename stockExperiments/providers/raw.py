import pandas
import sources.yahoofinance as yahoofinance
from base import *


class YahooCotationProvider(RawProvider):

    def __init__(self):
        RawProvider.__init__(self)
        self.mapping = [("open", 1), ("high", 2), ("low", 3), ("close", 4), ("volume", 5)]

    def load(self, s_symbol, da_start=None, da_end=None):
        ll_yahoo_data = yahoofinance.historical_prices(s_symbol + ".SA", da_start, da_end)
        ll_data = zip(*ll_yahoo_data[::-1])
        ts_index = ll_data[0]
        #return {s_name: self._createSeries(ll_data[i_columnIndex], ts_index, s_name) for s_name, i_columnIndex in self.mapping}
        return dict((s_name, self._createSeries(ll_data[i_columnIndex], ts_index, s_name)) for s_name, i_columnIndex in self.mapping)

    def _createSeries(self, data, ts_index, s_name):
        return pandas.TimeSeries(data, index=ts_index, name=s_name)
