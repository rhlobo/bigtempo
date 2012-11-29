

class AbstractProvider(object):

    def load(self, s_symbol):
        raise NotImplementedError


class AbstractCachingProvider(AbstractProvider):

    def update(self, s_symbol, c_dataFrame):
        raise NotImplementedError


class Provider(AbstractProvider):

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


class CachedProvider(AbstractCachingProvider):

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


class SymbolMapFactory(object):

    def get(self):
        return SymbolMap()


class SymbolMap(object):

    def __init__(self):
        self.c_dataMap = {}

    def get(self, s_symbol):
        if s_symbol not in self.c_dataMap:
            self.c_dataMap[s_symbol] = {}
        return self.c_dataMap[s_symbol]
