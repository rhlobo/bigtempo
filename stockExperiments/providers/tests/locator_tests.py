import unittest
from mockito import mock, when, verify, any as _any
import itertools
import inspect
import providers.locator as locator
import providers.base as base
import util.classutils as classutils


class TestLocatorModuleFunctions(unittest.TestCase):

    def test_module_should_have_stock_locator_retrieval_method(self):
        assert 'stock' in [name for name, method in inspect.getmembers(locator, predicate=inspect.isfunction)]

    def test_method_should_return_stock_locator(self):
        c_locator = locator.stock()
        assert isinstance(c_locator, locator.Locator)


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


class TestProviderLoader(unittest.TestCase):

    def test_load_should_use_builder_to_assemble_provider_chain(self):
        m_builder = mock(locator.ProviderLazyLoadingChainBuider)
        l_class = classutils.get_all_subclasses(base.RawProvider)
        c_providerLoader = locator.ProviderLoader(m_builder)
        c_providerLoader.load(base.RawProvider)
        verify(m_builder, times=len(l_class)).build(_any())

    def test_load_should_return_every_raw_providers(self):
        l_class_expected = classutils.get_all_subclasses(base.RawProvider)
        c_providerLoader = locator.ProviderLoader(_FakeBuilder())
        l_provider = c_providerLoader.load(base.RawProvider)
        for clazz in l_class_expected:
            assert clazz in [provider.typifies() for provider in l_provider]

    def test_load_should_return_objects_that_need_construction_params(self):
        param1 = "string"
        param2 = 42
        c_providerLoader = locator.ProviderLoader(_FakeBuilder())
        l_provider = c_providerLoader.load(_ProviderMock, param1, param2)
        assert isinstance(l_provider[0], _ProviderMockImpl)
        assert l_provider[0].string_param == param1
        assert l_provider[0].integer_param == param2


class TestLocator(unittest.TestCase):

    def test_locator_initialization_should_use_providerLoader(self):
        c_locator, providerLoader, lm1, lm2 = self._prepare_locator_mock()
        c_locator.add_provider_definition(_AbstractRawMock)
        c_locator.add_provider_definition(_AbstractByProductMock, c_locator)

        verify(providerLoader, times=1).load(_AbstractRawMock)
        verify(providerLoader, times=1).load(_AbstractByProductMock, c_locator)

    def test_get_without_params_should_return_all_providers(self):
        c_locator, providerLoader, lm_rawProviders, lm_byprodProviders = self._prepare_locator_mock()
        c_locator.add_provider_definition(_AbstractRawMock)
        c_locator.add_provider_definition(_AbstractByProductMock, c_locator)
        l_providers = c_locator.get()

        assert len(l_providers) == 4
        for l_mock in itertools.chain(lm_rawProviders, lm_byprodProviders):
            assert l_mock.__class__ in l_providers

    def test_get_with_provider_class_as_param_should_return_provider(self):
        c_locator, providerLoader, lm1, lm2 = self._prepare_locator_mock()
        c_locator.add_provider_definition(_AbstractRawMock)
        c_locator.add_provider_definition(_AbstractByProductMock, c_locator)
        l_providers = c_locator.get()

        for l_mock in l_providers:
            assert c_locator.get(l_mock) is not None
            assert l_mock is c_locator.get(l_mock).__class__

    def _prepare_locator_mock(self):
        providerLoader = mock(locator.ProviderLoader)

        m_mock = mock()
        lm_rawProviders = [_RawMock1(), _RawMock2(), _RawMock3()]
        lm_byprodProviders = [_ByProductMock1(m_mock)]

        when(providerLoader).load(_AbstractRawMock).thenReturn(lm_rawProviders)
        when(providerLoader).load(_AbstractByProductMock, _any()).thenReturn(lm_byprodProviders)

        return (locator.Locator(providerLoader), providerLoader, lm_rawProviders, lm_byprodProviders)


class _FakeBuilder(object):

    def build(self, provider):
        return provider


class _AbstractRawMock(base.RawProvider):
    pass


class _AbstractByProductMock(base.ByproductProvider):
    pass


class _RawMock1(_AbstractRawMock):
    pass


class _RawMock2(_AbstractRawMock):
    pass


class _RawMock3(_AbstractRawMock):
    pass


class _ByProductMock1(_AbstractByProductMock):
    pass


class _ProviderMock(base.AbstractProvider):

    def __init__(self, string_param, integer_param):
        self.string_param = string_param
        self.integer_param = integer_param


class _ProviderMockImpl(_ProviderMock):
    pass
