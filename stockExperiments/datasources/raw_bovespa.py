import configurations as config
import sources.cotahist as cotahist

from instances import data_engine


@data_engine.datasource('RAW_BOVESPA', tags=['RAW'])
class RawBovespa(object):

    def __init__(self):
        self._dataFrameMap = None

    def evaluate(self, context, symbol, start=None, end=None):
        result = self._get_dataFrameMap().get(symbol)

        if start and end:
            return result[start:end]
        if start:
            return result[start:]
        if end:
            return result[:end]

        return result

    def _get_dataFrameMap(self):
        if not self._dataFrameMap:
            self._dataFrameMap = cotahist.CotahistImporter(config.DATA_DIR).getDataFrameMap()
        return self._dataFrameMap
