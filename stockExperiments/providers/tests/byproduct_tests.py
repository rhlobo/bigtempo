import unittest
from mockito import mock, when
import pandas
import util.testutils as testutils
import util.fileutils as fileutils
import providers.locator as locator
import providers.raw as raw
import providers.byproduct as byproduct


class TestPercentualChangeProvider(unittest.TestCase):

    def test_should_return_correct_percentual_change_using_raw_mock_data(self):
        s_symbol = 'PETR4'
        locator_mock = mock(locator.Locator)
        provider_mock = mock(raw.CotahistProvider)
        df_raw = pandas.DataFrame.from_csv(fileutils.get_test_data_file_path(__file__, 'raw_PETR4.csv'))

        when(provider_mock).load(s_symbol, None, None).thenReturn(df_raw)
        when(locator_mock).get(raw.CotahistProvider).thenReturn(provider_mock)

        provider = byproduct.PercentualChangeProvider(locator_mock)
        result = provider.load(s_symbol)

        expected = pandas.DataFrame(index=df_raw.index, columns=df_raw.columns)
        for i in range(1, len(df_raw)):
            pct = ((df_raw.ix[i] - df_raw.ix[i - 1]) / df_raw.ix[i - 1])
            for column in df_raw.columns:
                expected[column][i] = pct[column]

        testutils.assert_dataframe_almost_equal(expected[1:], result)

    def test_should_return_correct_percentual_change_using_mock_data(self):
        s_symbol = 'PETR4'
        s_data_filename = 'raw_PETR4.csv'
        locator_mock = _prepare_locator_mock(s_symbol, raw.CotahistProvider, s_data_filename)

        provider = byproduct.PercentualChangeProvider(locator_mock)
        result = provider.load(s_symbol)
        expected = pandas.DataFrame.from_csv(fileutils.get_test_data_file_path(__file__, 'percentual_PETR4.csv'))

        testutils.assert_dataframe_almost_equal(expected, result)


class TestSplitInformationProvider(unittest.TestCase):

    def test_should_return_correct_split_and_join_data_using_mock_data(self):
        s_symbol = 'PETR4'
        s_data_filename = 'percentual_PETR4.csv'
        locator_mock = _prepare_locator_mock(s_symbol, byproduct.PercentualChangeProvider, s_data_filename)

        provider = byproduct.SplitInformationProvider(locator_mock)
        result = provider.load(s_symbol)
        expected = pandas.DataFrame.from_csv(fileutils.get_test_data_file_path(__file__, 'splits_PETR4.csv'))

        testutils.assert_dataframe_almost_equal(expected, result)


class TestNormalizationFactorProvider(unittest.TestCase):

    def test_should_return_correct_normalization_factor_using_mock_data(self):
        s_symbol = 'PETR4'
        s_data_filename = 'splits_PETR4.csv'
        locator_mock = _prepare_locator_mock(s_symbol, byproduct.SplitInformationProvider, s_data_filename)

        expected = pandas.DataFrame.from_csv(fileutils.get_test_data_file_path(__file__, 'normalizationfactor_PETR4.csv'))
        actual = byproduct.NormalizationFactorProvider(locator_mock).load(s_symbol, expected.ix[0].name, expected.ix[-1].name)

        testutils.assert_dataframe_almost_equal(expected, actual)


def _prepare_locator_mock(s_symbol, c_mocked_provider, s_data_filename):
    locator_mock = mock(locator.Locator)
    provider_mock = mock(c_mocked_provider)
    df_raw = pandas.DataFrame.from_csv(fileutils.get_test_data_file_path(__file__, s_data_filename))

    when(provider_mock).load(s_symbol, None, None).thenReturn(df_raw)
    when(locator_mock).get(c_mocked_provider).thenReturn(provider_mock)

    return locator_mock
