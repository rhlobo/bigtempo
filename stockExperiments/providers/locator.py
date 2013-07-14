# -*- coding: utf-8 -*-


from providers.base import *
from providers.raw import *
from providers.byproduct import *
import util.classutils as classutils


class Locator(object):

    def __init__(self, providerLoader):
        self.providers = {}
        self.providerLoader = providerLoader

    def add_provider_definition(self, base_class, *args):
        for provider in self.providerLoader.load(base_class, *args):
            self.providers[provider.typifies()] = provider

    def get(self, providerClass=None):
        return self.providers.keys() if not providerClass else self.providers.get(providerClass)


class ProviderLoader(object):

    def __init__(self, builder):
        self.builder = builder

    def load(self, base_class, *args):
        return [self.builder.build(instance) for instance in self._create_instances(base_class, *args)]

    def _create_instances(self, base_class, *args):
        return classutils.instantiate(classutils.get_all_subclasses(base_class), *args)


class ProviderLazyLoadingChainBuider(object):

    def build(self, provider):
        return ProviderChainManager(provider)


def stock():
    return _STOCK_LOCATOR


_STOCK_LOCATOR = Locator(ProviderLoader(ProviderLazyLoadingChainBuider()))
_STOCK_LOCATOR.add_provider_definition(RawProvider)
_STOCK_LOCATOR.add_provider_definition(ByproductProvider, _STOCK_LOCATOR)
