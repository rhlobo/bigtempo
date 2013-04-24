from mockito import mock, when, any as _any
import os
import pandas
import util.fileutils as fileutils
import providers.locator as locator


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
    tmp = (expected - actual).abs() < margin
    assert tmp.all().all() == True


def assert_provider_correctness_using_datafiles(test_file, s_symbol, c_provider, s_expecteddata_filename, *locator_mock_infos):
    locator_mock = prepare_locator_using_datafile(test_file, s_symbol, *locator_mock_infos)

    expected = pandas.DataFrame.from_csv(fileutils.get_test_data_file_path(test_file, s_expecteddata_filename))
    actual = c_provider(locator_mock).load(s_symbol, expected.ix[0].name, expected.ix[-1].name)

    assert_dataframe_almost_equal(expected, actual)


def prepare_locator_using_datafile(test_file, s_symbol, *locator_mock_infos):
    locator_mock = mock(locator.Locator)

    for c_mocked_provider, s_data_filename in locator_mock_infos:
        provider_mock = mock(c_mocked_provider)
        df_from_file = pandas.DataFrame.from_csv(fileutils.get_test_data_file_path(test_file, s_data_filename))

        when(provider_mock).load(s_symbol, _any(), _any()).thenReturn(df_from_file)
        when(locator_mock).get(c_mocked_provider).thenReturn(provider_mock)

    return locator_mock
