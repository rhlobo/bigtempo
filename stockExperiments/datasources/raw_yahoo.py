import pandas
import sources.yahoofinance as yahoofinance

from instances import data_engine


@data_engine.datasource('RAW_YAHOO_BR',
                        tags=['RAW'])
class RawYahoo(object):

    _columns = ['open', 'high', 'low', 'close', 'volume']
    _mappings = [("open", 1), ("high", 2), ("low", 3), ("close", 4), ("volume", 5)]

    def evaluate(self, context, symbol, start=None, end=None):
        data = zip(*self._load_yahoo_data(symbol, start, end)[::-1])

        ts_dict = dict(
            (column_name, self._createTimeSeries(data[column_index], data[0], column_name))
            for column_name, column_index in self._mappings
        )

        return pandas.DataFrame(ts_dict, columns=self._columns)

    def _load_yahoo_data(self, symbol, start=None, end=None):
        return yahoofinance.historical_prices(symbol + ".SA", start, end)

    def _createTimeSeries(self, data, dates, column_name):
        return pandas.TimeSeries(data, index=dates, name=column_name)
