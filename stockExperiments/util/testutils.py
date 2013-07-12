import os
import pandas
import inspect
import unittest
from mockito import mock, when, any as _any, unstub

import instances
import bigtempo.core as core
import util.fileutils as fileutils
import util.moduleutils as moduleutils
import providers.locator as locator


def assert_datasource_correctness_using_datafiles(test_instance, symbol, tested_reference, expected_result_file, *mock_infos):
    test_file = inspect.getfile(test_instance.__class__)

    def _create_mock_datasource(data_file):
        data = get_dataframe_from_csv(test_file, mock_data_file, test_filename_to_data_dir_function=fileutils.get_commum_test_data_dir)

        class DatasourceMock(object):

            def evaluate(self, context, symbol, start=None, end=None):
                return data

        return DatasourceMock

    for mock_reference, mock_data_file in mock_infos:
        datasource_mock_cls = _create_mock_datasource(mock_data_file)

        instances.data_engine._instances[mock_reference] = None
        new_registration = {
            'class': datasource_mock_cls,
            'lookback': 0,
            'dependencies': set()
        }

        if not instances.data_engine._registrations.get(mock_reference):
            instances.data_engine._registrations[mock_reference] = {}
        instances.data_engine._registrations[mock_reference].update(new_registration)

    actual = instances.data_engine.get(tested_reference).process(symbol)
    expected = get_dataframe_from_csv(test_file, expected_result_file, test_filename_to_data_dir_function=fileutils.get_commum_test_data_dir)
    assert_dataframe_almost_equal(expected, actual)


class DatasourceTestCase(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        cls.data_engine = instances.data_engine

        testing_builder_mock = mock()

        def testing_builder(cls):
            mock_result = testing_builder_mock.build(cls)
            if mock_result:
                return mock_result
            return cls()

        engine = core.DatasourceEngine(builder=testing_builder)

        instances.data_engine = engine
        cls.testing_builder_mock = testing_builder_mock

        moduleutils.reload_modules(r'datasources\..*')

    @classmethod
    def tearDownClass(cls):
        instances.data_engine = cls.data_engine

    def setUp(self):
        pass

    def tearDown(self):
        unstub()


def get_dataframe_from_csv(test_file, filename, test_filename_to_data_dir_function=None):
    filepath = fileutils.get_test_data_file_path(test_file, filename, test_filename_to_data_dir_function)
    return pandas.DataFrame.from_csv(filepath)


class CallableMock(object):
    def __init__(self, mock):
        self.mock = mock

    def __call__(self, *args, **kwargs):
        return self.mock.__call__(*args, **kwargs)

    def __getattr__(self, method_name):
        return self.mock.__getattr__(method_name)


class IterableMock(object):
    def __init__(self, mock):
        self.mock = mock

    def __iter__(self, *args, **kwargs):
        return self.mock.__iter__(*args, **kwargs)

    def __getattr__(self, method_name):
        return self.mock.__getattr__(method_name)


def should_skip_provider_deep_tests():
    return os.environ.get('TESTTYPE') == 'fast'


def get_providers_deep_tests_skip_reason():
    if os.environ.get('TESTTYPE') == 'fast':
        return 'Fast test execution requested through environment variable.'
    return 'Providers deep tests are disabled.'


def assert_data_index_is_ordered(data):
    lastDate = data.ix[0].name
    for row in data.iterrows():
        currDate = row[0]
        assert currDate >= lastDate
        lastDate = currDate


def assert_dataframe_almost_equal(expected, actual, margin=0.0000000001):
    tmp = ((expected.dropna() - actual.dropna()).abs() < margin)
    assert tmp.all().all() == True


def assert_provider_correctness_using_datafiles(test_file, s_symbol, c_provider, s_expecteddata_filename, *locator_mock_infos):
    locator_mock = prepare_locator_using_datafile(test_file, s_symbol, *locator_mock_infos)

    expected = pandas.DataFrame.from_csv(fileutils.get_test_data_file_path(test_file, s_expecteddata_filename))
    if len(expected) != 0:
        actual = c_provider(locator_mock).load(s_symbol, expected.ix[0].name, expected.ix[-1].name)
    else:
        actual = c_provider(locator_mock).load(s_symbol)

    assert_dataframe_almost_equal(expected, actual)


def prepare_locator_using_datafile(test_file, s_symbol, *locator_mock_infos):
    locator_mock = mock(locator.Locator)

    for c_mocked_provider, s_data_filename in locator_mock_infos:
        provider_mock = mock(c_mocked_provider)
        df_from_file = pandas.DataFrame.from_csv(fileutils.get_test_data_file_path(test_file, s_data_filename))

        when(provider_mock).load(s_symbol, _any(), _any()).thenReturn(df_from_file)
        when(locator_mock).get(c_mocked_provider).thenReturn(provider_mock)

    return locator_mock
