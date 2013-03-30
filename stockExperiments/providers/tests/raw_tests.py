import unittest
import numpy
import pandas
from datetime import *
import util.testutils as testutils
import util.classutils as classutils
import util.fileutils as fileutils
import sources.cotahist as cotahist
import providers.base as base
import providers.raw as raw


@unittest.skipIf(testutils.should_skip_provider_deep_tests(), testutils.get_providers_deep_tests_skip_reason())
def test_raw_providers_load_PETR4_should_return_dataFrame_object():
    def assert_raw_providers_load_PETR4_should_return_dataFrame_object(cls):
        provider = cls()
        result = provider.load('PETR4', date(2011, 11, 17), date(2011, 11, 17))
        assert isinstance(result, pandas.DataFrame)

    for rawCls in _getScenarios():
        yield assert_raw_providers_load_PETR4_should_return_dataFrame_object, rawCls


class TestYahooCotationProvider(unittest.TestCase):

    @unittest.skip("Skipping: Yahoo provides incorrect data.")
    def test_should_return_dataFrame_object_with_correct_columns(self):
        assert False
        provider = raw.YahooCotationProvider()
        data = provider.load('PETR4', date(2013, 3, 1), date(2013, 3, 26))
        expected_data = _get_expected_dataframe_from_csv('petr4-2013-03.csv')
        numpy.testing.assert_approx_equal(numpy.array(data), numpy.array(expected_data), significant=5, verbose=True)


class TestCotahistProvider(unittest.TestCase):

    @unittest.skipIf(testutils.should_skip_provider_deep_tests(), testutils.get_providers_deep_tests_skip_reason())
    def test_should_return_dataFrame_object_with_correct_columns(self):
        provider = raw.CotahistProvider()
        data = provider.load('PETR4', date(2013, 3, 1), date(2013, 3, 26))
        expected_data = _get_expected_dataframe_from_csv('petr4-2013-03.csv')
        numpy.testing.assert_array_equal(data, expected_data)


class TestCotahistProvider_load_data_selection(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        cls.importer = cotahist.CotahistImporter
        cotahist.CotahistImporter = _CotahistImporterMock

    @classmethod
    def tearDownClass(cls):
        cotahist.CotahistImporter = cls.importer

    def test_should_return_empty_dataFrame_when_period_not_available(self):
        provider = raw.CotahistProvider()
        data = provider.load('PETR4', date(2114, 3, 10), date(2114, 4, 26))
        assert len(data) == 0

    def test_should_return_dataFrame_subset_when_period_is_contained_in_available_data(self):
        provider = raw.CotahistProvider()
        data = provider.load('PETR4', date(2013, 3, 8), date(2013, 3, 12))
        assert len(data) == 3
        assert data.ix[0].name == datetime(2013, 3, 8)
        assert data.ix[1].name == datetime(2013, 3, 11)
        assert data.ix[2].name == datetime(2013, 3, 12)

    def test_should_return_whole_dataFrame_when_no_startdate_and_enddate_is_given(self):
        provider = raw.CotahistProvider()
        data = provider.load('PETR4')
        assert len(data) == 18
        assert data.ix[0].name == datetime(2013, 3, 1)
        assert data.ix[17].name == datetime(2013, 3, 26)

    def test_should_return_dataFrame_begining_on_1st_record_when_no_startdate_is_given(self):
        provider = raw.CotahistProvider()
        data = provider.load('PETR4', da_end=date(2013, 3, 12))
        assert len(data) == 8
        assert data.ix[0].name == datetime(2013, 3, 1)
        assert data.ix[7].name == datetime(2013, 3, 12)

    def test_should_return_dataFrame_records_until_last_when_no_enddate_is_given(self):
        provider = raw.CotahistProvider()
        data = provider.load('PETR4', da_start=date(2013, 3, 23))
        assert len(data) == 2
        assert data.ix[0].name == datetime(2013, 3, 25)
        assert data.ix[1].name == datetime(2013, 3, 26)


def _getScenarios():
    return classutils.get_all_subclasses(base.RawProvider, r'^[^_]+.*')


def _get_expected_dataframe_from_csv(filename):
    filepath = fileutils.get_test_data_file_path(__file__, filename)
    return pandas.DataFrame.from_csv(filepath)


class _CotahistImporterMock(object):

    def __init__(self, s_data_dir):
        self.d_dataFrame = {}
        self.d_dataFrame['PETR4'] = _get_expected_dataframe_from_csv('petr4-2013-03.csv')

    def getDataFrameMap(self):
        return self.d_dataFrame
