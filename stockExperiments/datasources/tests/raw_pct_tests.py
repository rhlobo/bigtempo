import util.testutils as testutils


class TestRawPctDatasource(testutils.DatasourceTestCase):

    def test_should_return_correct_percentual_change_using_mocked_data(self):
        testutils.assert_datasource_correctness_using_datafiles(self,
                                                                'PETR4',
                                                                'PCT_CHANGE(1):RAW_BOVESPA',
                                                                'percentual_PETR4.csv',
                                                                ('RAW_BOVESPA', 'raw_PETR4.csv'))

    def test_should_return_correct_percentual_change_using_mocked_data_woth_no_splits(self):
        testutils.assert_datasource_correctness_using_datafiles(self,
                                                                'NO-SPLITS',
                                                                'PCT_CHANGE(1):RAW_BOVESPA',
                                                                'percentual_NO-SPLITS.csv',
                                                                ('RAW_BOVESPA', 'raw_NO-SPLITS.csv'))

    def test_should_return_correct_percentual_change_using_mocked_data_woth_with_splits(self):
        testutils.assert_datasource_correctness_using_datafiles(self,
                                                                'WITH-SPLITS',
                                                                'PCT_CHANGE(1):RAW_BOVESPA',
                                                                'percentual_WITH-SPLITS.csv',
                                                                ('RAW_BOVESPA', 'raw_WITH-SPLITS.csv'))
