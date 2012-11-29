import unittest
from mockito import mock
from providers.base import AbstractProvider, SymbolMap
from providers.raw import CotahistProvider


class TestCotahistProvider(unittest.TestCase):

    def test_should_subclass_abstractProvider(self):
        provider = CotahistProvider(mock(SymbolMap()))
        assert isinstance(provider, AbstractProvider)
