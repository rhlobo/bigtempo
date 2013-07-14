# -*- coding: utf-8 -*-


import pandas
import configurations as config
import sources.yahoofinance as yahoofinance
import sources.cotahist as cotahist
import providers.base as base


class YahooCotationProvider(base.RawProvider):

    def __init__(self):
        base.RawProvider.__init__(self)
        self.mapping = [("open", 1), ("high", 2), ("low", 3), ("close", 4), ("volume", 5)]

    def load(self, s_symbol, da_start=None, da_end=None):
        ll_yahoo_data = yahoofinance.historical_prices(s_symbol + ".SA", da_start, da_end)
        ll_data = zip(*ll_yahoo_data[::-1])
        ldt_index = ll_data[0]
        ts_dict = dict((s_name, self._createSeries(ll_data[i_columnIndex], ldt_index, s_name)) for s_name, i_columnIndex in self.mapping)
        return pandas.DataFrame(ts_dict, columns=['open', 'high', 'low', 'close', 'volume'])

    def _createSeries(self, data, ldt_index, s_name):
        return pandas.TimeSeries(data, index=ldt_index, name=s_name)


class CotahistProvider(base.RawProvider):

    def __init__(self):
        base.RawProvider.__init__(self)
        self.d_dataFrame = None

    def _get_dataFrameMap(self):
        if not self.d_dataFrame:
            self.d_dataFrame = cotahist.CotahistImporter(config.DATA_DIR).getDataFrameMap()
        return self.d_dataFrame

    #TODO: What to do if there was no df for s_symbol?
    def load(self, s_symbol, da_start=None, da_end=None):
        df_symbol = self._get_dataFrameMap().get(s_symbol)

        if da_start and da_end:
            return df_symbol[da_start:da_end]
        if da_start:
            return df_symbol[da_start:]
        if da_end:
            return df_symbol[:da_end]

        return df_symbol
