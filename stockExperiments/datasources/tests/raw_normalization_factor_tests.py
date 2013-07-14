import util.testutils as testutils


class TestSplitInformationDatasource(testutils.DatasourceTestCase):

    def test_should_return_correct_normalization_factor_using_mocked_data(self):
        testutils.assert_datasource_correctness_using_datafiles(self,
                                                                'PETR4',
                                                                'NORMALIZATION_FACTOR:SPLITS:PCT_CHANGE(1):RAW_BOVESPA',
                                                                'normalizationfactor_PETR4.csv',
                                                                ('SPLITS:PCT_CHANGE(1):RAW_BOVESPA', 'splits_PETR4.csv'))

    def test_should_return_correct_normalization_factor_using_mocked_data_no_splits(self):
        testutils.assert_datasource_correctness_using_datafiles(self,
                                                                'NO-SPLITS',
                                                                'NORMALIZATION_FACTOR:SPLITS:PCT_CHANGE(1):RAW_BOVESPA',
                                                                'normalizationfactor_NO-SPLITS.csv',
                                                                ('SPLITS:PCT_CHANGE(1):RAW_BOVESPA', 'splits_NO-SPLITS.csv'))

    def test_should_return_correct_normalization_factor_using_mocked_data_with_splits(self):
        testutils.assert_datasource_correctness_using_datafiles(self,
                                                                'WITH-SPLITS',
                                                                'NORMALIZATION_FACTOR:SPLITS:PCT_CHANGE(1):RAW_BOVESPA',
                                                                'normalizationfactor_WITH-SPLITS.csv',
                                                                ('SPLITS:PCT_CHANGE(1):RAW_BOVESPA', 'splits_WITH-SPLITS.csv'))
