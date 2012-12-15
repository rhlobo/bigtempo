from providers.base import *
from providers.raw import *
import util.classutils as classutils


class Locator(object):

    def __init__(self, providerLoader):
        self.providers = {}
        for provider in providerLoader.load():
            self.providers[provider.typifies()] = provider

    def get(self, providerClass=None):
        if not providerClass:
            return self.providers.keys()
        return self.providers.get(providerClass)


class ProviderLoader(object):

    def __init__(self, builder):
        self.builder = builder

    def load(self):
        return [self.builder.build(instance) for instance in self.__load(RawProvider)]

    def __load(self, baseClass):
        return classutils.instantiate(classutils.get_all_subclasses(baseClass))


class ProviderLazyLoadingChainBuider(object):

    def __init__(self):
        self.symbolMapFactory = SymbolMapFactory()

    def build(self, provider):
        symbolMap = self.symbolMapFactory.get()
        return ProviderChainManager(CachedProvider(symbolMap), provider)


def stock():
    return __stock_locator


__stock_locator = Locator(ProviderLoader(ProviderLazyLoadingChainBuider()))
