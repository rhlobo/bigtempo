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
        testutils.assert_provider_correctness_using_datafiles(__file__, 'PETR4', byproduct.PercentualChangeProvider, 'percentual_PETR4.csv', (raw.CotahistProvider, 'raw_PETR4.csv'))


class TestSplitInformationProvider(unittest.TestCase):

    def test_should_return_correct_split_and_join_data_using_mock_data(self):
        testutils.assert_provider_correctness_using_datafiles(__file__, 'PETR4', byproduct.SplitInformationProvider, 'splits_PETR4.csv', (byproduct.PercentualChangeProvider, 'percentual_PETR4.csv'))


class TestNormalizationFactorProvider(unittest.TestCase):

    def test_should_return_correct_normalization_factor_using_mock_data(self):
        testutils.assert_provider_correctness_using_datafiles(__file__, 'PETR4', byproduct.NormalizationFactorProvider, 'normalizationfactor_PETR4.csv', (byproduct.SplitInformationProvider, 'splits_PETR4.csv'))


class TestNormalizatedCotationProvider(unittest.TestCase):

    def test_should_return_correct_normalizated_cotation_using_mock_data(self):
        testutils.assert_provider_correctness_using_datafiles(__file__, 'PETR4', byproduct.NormalizedCotationProvider, 'normalized_PETR4.csv', (byproduct.NormalizationFactorProvider, 'normalizationfactor_PETR4.csv'), (raw.CotahistProvider, 'raw_PETR4.csv'))
