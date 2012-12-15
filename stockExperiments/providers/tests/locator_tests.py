import unittest
from mockito import mock, when, verify, any as anya
import providers.locator as locator
import providers.base as base
import util.classutils as classutils


class TestLocatorModuleFunctions(unittest.TestCase):

    def test_module_should_have_get_method(self):
        locator.stock()

    def test_get_should_return_locator(self):
        c_locator = locator.stock()
        assert isinstance(c_locator, locator.Locator)


class TestProviderLoader(unittest.TestCase):

    def test_load_should_use_builder_to_assemble_provider_chain(self):
        m_builder = mock(locator.ProviderLazyLoadingChainBuider)
        l_class = classutils.get_all_subclasses(base.RawProvider)
        c_providerLoader = locator.ProviderLoader(m_builder)
        c_providerLoader.load()
        verify(m_builder, times=len(l_class)).build(anya())

    def test_load_should_return_every_raw_providers(self):
        l_class = classutils.get_all_subclasses(base.RawProvider)
        c_providerLoader = locator.ProviderLoader(locator.ProviderLazyLoadingChainBuider())
        l_provider = c_providerLoader.load()
        for clazz in l_class:
            assert clazz in [provider.typifies() for provider in l_provider]


class TestProviderLazyLoadingChainBuider(unittest.TestCase):

    def test_build_should_return_providerChainManager(self):
        c_builder = locator.ProviderLazyLoadingChainBuider()
        c_providerManager = c_builder.build(mock(base.AbstractProvider))
        assert isinstance(c_providerManager, base.ProviderChainManager)

    def test_build_should_return_providerChainManager_with_given_class_as_base_provider(self):
        c_builder = locator.ProviderLazyLoadingChainBuider()
        m_provider = base.RawProvider()
        c_providerManager = c_builder.build(m_provider)
        assert c_providerManager.typifies() is m_provider.__class__


class TestLocator(unittest.TestCase):

    def test_locator_initialization_should_use_providerLoader(self):
        providerLoader = mock(locator.ProviderLoader)
        when(providerLoader).load().thenReturn([])
        locator.Locator(providerLoader)
        verify(providerLoader, times=1).load()

    def test_get_without_params_should_return_all_providers(self):
        providerLoader = mock(locator.ProviderLoader)
        l_providerMocks = [Mock1(), Mock2(), Mock3()]
        when(providerLoader).load().thenReturn(l_providerMocks)

        c_locator = locator.Locator(providerLoader)
        l_providers = c_locator.get()

        verify(providerLoader, times=1).load()
        assert len(l_providers) == 3
        for l_mock in l_providerMocks:
            assert l_mock.__class__ in l_providers

    def test_get_with_provider_class_as_param_should_return_all_providers(self):
        providerLoader = mock(locator.ProviderLoader)
        l_providerMocks = [Mock1(), Mock2(), Mock3()]
        when(providerLoader).load().thenReturn(l_providerMocks)

        c_locator = locator.Locator(providerLoader)
        for l_mock in l_providerMocks:
            assert l_mock is c_locator.get(l_mock.__class__)
            assert c_locator.get(l_mock.__class__) is not None


class Mock1(base.RawProvider):
    pass


class Mock2(base.RawProvider):
    pass


class Mock3(base.RawProvider):
    pass
