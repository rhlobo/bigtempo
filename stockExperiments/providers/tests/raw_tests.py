import unittest
import pandas
from datetime import date as date
import util.classutils as classutils
import providers.base as base
import providers.raw as raw


def test_raw_providers_load_PETR4_should_return_dataFrame_object():
    def assert_raw_providers_load_PETR4_should_return_dataFrame_object(cls):
        provider = cls()
        result = provider.load('PETR4', date(2011, 11, 17), date(2011, 11, 17))
        assert isinstance(result, pandas.DataFrame)

    for rawCls in _getScenarios():
        yield assert_raw_providers_load_PETR4_should_return_dataFrame_object, rawCls


class TestRawProviderSubclasses(unittest.TestCase):
    pass


class TestYahooCotationProvider(unittest.TestCase):

    def test_should_return_dataFrame_object_with_correct_columns(self):
        assert False


class TestCotahistProvider(unittest.TestCase):

    def test_should_return_dataFrame_object_with_correct_columns(self):
        assert False


def _getScenarios():
    return classutils.get_all_subclasses(base.RawProvider, r'^[^_]+.*')
