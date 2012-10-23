

import data.cotahist.cotahist as cotahist


def get():
    c_dataMapFactory = SymbolMapFactory()
    return (DataProvider(CachedProvider(c_dataMapFactory.get()),
                         RawCotationProvider(c_dataMapFactory.get())))


class AbstractProvider():

    def __init__(self):
        pass

    def load(self, s_symbol):
        raise NotImplemented

    def update(self, s_symbol, c_dataFrame):
        raise NotImplemented


class DataProvider(AbstractProvider):

    def __init__(self, *providers):
        self.providers = providers

    def load(self, s_symbol):
        lc_providers = []
        for provider in self.providers:
            result = provider.load(s_symbol)

            if result is None:
                lc_providers.append(provider)
            else:
                self.__updateProviders(lc_providers, s_symbol, result)
                return result

        return None

    def __updateProviders(self, lc_providers, s_symbol, data):
        for provider in lc_providers:
            provider.update(s_symbol, data)

    def update(self, s_symbol, c_dataFrame):
        raise NotImplemented


class CachedProvider(AbstractProvider):

    def __init__(self, c_dataMap):
        AbstractProvider.__init__(self)
        self.c_dataMap = c_dataMap

    def load(self, s_symbol):
        c_dataFrame = self.c_dataMap.get(s_symbol)
        if len(c_dataFrame) == 0:
            return None
        return c_dataFrame

    def update(self, s_symbol, c_dataFrame):
        self.c_dataMap.get(s_symbol).update(c_dataFrame)


class RawCotationProvider(AbstractProvider):

    def __init__(self, c_dataMap):
        AbstractProvider.__init__(self)
        self.c_dataMap = c_dataMap

    def load(self, s_symbol):
        c_dataFrame = self.c_dataMap.get(s_symbol)
        if len(c_dataFrame) == 0:
            self.__importData()
        return c_dataFrame

    def update(self, s_symbol, c_dataFrame):
        pass

    def __importData(self):
        la_quote = cotahist.importData()
        for s_symbol, date, f_open, f_min, f_max, f_close, i_vol in la_quote:
            c_dataFrame = self.c_dataMap.get(s_symbol)
            c_dataFrame[date] = (date, f_open, f_min, f_max, f_close, i_vol)


class SymbolMapFactory():

    def get(self):
        return SymbolMap()


class SymbolMap():

    def __init__(self):
        self.c_dataMap = {}

    def get(self, s_symbol):
        if s_symbol not in self.c_dataMap:
            self.c_dataMap[s_symbol] = {}
        return self.c_dataMap[s_symbol]


class DataFrame():

    def __init__(self):
        self.d_data = {}

    def update(self, c_dataFrame):
        self.d_data.update(c_dataFrame.d_data)
