import types
from collections import namedtuple
from providers.base import *
from providers.raw import *
import util.classutils as classutils


class Locator(object):

    def __init__(self, providerLoader):
        _PROVIDER_TYPE = namedtuple('ProviderType', 'name base_class constructor_args')
        _PROVIDER_DEFINITIONS = [
                                 _PROVIDER_TYPE("raw", RawProvider, []),
                                 _PROVIDER_TYPE("byproduct", ByproductProvider, [self])
                                ]

        def _getter_creator(provider_map):
            def _getter(self, providerClass=None):
                return provider_map.keys() if not providerClass else provider_map.get(providerClass)
            return _getter

        self.providers = {}
        setattr(self, 'get', types.MethodType(_getter_creator(self.providers), self))

        for provider_type in _PROVIDER_DEFINITIONS:
            setattr(self, provider_type.name, {})
            provider_map = getattr(self, provider_type.name)
            for provider in providerLoader.load(provider_type.base_class, *provider_type.constructor_args):
                provider_reference = provider.typifies()
                provider_map[provider_reference] = provider
                self.providers[provider_reference] = provider
            setattr(self, 'get_%s' % provider_type.name, types.MethodType(_getter_creator(provider_map), self))


class ProviderLoader(object):

    def __init__(self, builder):
        self.builder = builder

    def load(self, base_class, *args):
        return [self.builder.build(instance) for instance in self._create_instances(base_class, *args)]

    def _create_instances(self, base_class, *args):
        return classutils.instantiate(classutils.get_all_subclasses(base_class), *args)


class ProviderLazyLoadingChainBuider(object):

    def __init__(self):
        self.symbolMapFactory = SymbolMapFactory()

    def build(self, provider):
        symbolMap = self.symbolMapFactory.get()
        return ProviderChainManager(CachedProvider(symbolMap), provider)


def stock():
    return _stock_locator


_stock_locator = Locator(ProviderLoader(ProviderLazyLoadingChainBuider()))
