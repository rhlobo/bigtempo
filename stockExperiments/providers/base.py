

class AbstractProvider(object):

    def load(self, s_symbol, da_start=None, da_end=None):
        raise NotImplementedError

    def clear(self, s_symbol):
        raise NotImplementedError

    def typifies(self):
        raise NotImplementedError


class AbstractCachingProvider(AbstractProvider):

    def __init__(self):
        AbstractProvider.__init__(self)

    def update(self, s_symbol, c_dataFrame):
        raise NotImplementedError


class RawProvider(AbstractProvider):

    def __init__(self):
        AbstractProvider.__init__(self)

    def typifies(self):
        return self.__class__


class ByProductProvider(AbstractProvider):

    def __init__(self, locator):
        AbstractProvider.__init__(self)
        self.locator = locator

    def typifies(self):
        return self.__class__


class ProviderChainManager(AbstractProvider):

    def __init__(self, *providers):
        AbstractProvider.__init__(self)
        self.providers = providers

    def load(self, s_symbol, da_start=None, da_end=None):
        lc_providers = []
        for provider in self.providers:
            result = provider.load(s_symbol)

            if result is None:
                lc_providers.append(provider)
            else:
                self._updateProviders(lc_providers, s_symbol, result)
                return result

        return None

    def _updateProviders(self, lc_providers, s_symbol, data):
        for provider in lc_providers:
            provider.update(s_symbol, data)

    def typifies(self):
        return self.providers[-1].typifies()


class CachedProvider(AbstractCachingProvider):

    def __init__(self, c_dataMap):
        AbstractCachingProvider.__init__(self)
        self.c_dataMap = c_dataMap

    def load(self, s_symbol, da_start=None, da_end=None):
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
        if self.c_dataMap.get(s_symbol) is None:
            self.c_dataMap[s_symbol] = {}
        return self.c_dataMap[s_symbol]
