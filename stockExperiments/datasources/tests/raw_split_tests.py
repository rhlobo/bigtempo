import util.testutils as testutils


class TestSplitInformationDatasource(testutils.DatasourceTestCase):

    def test_should_return_correct_split_and_join_data_using_mocked_data(self):
        testutils.assert_datasource_correctness_using_datafiles(self,
                                                                'PETR4',
                                                                'SPLITS:PCT_CHANGE(1):RAW_BOVESPA',
                                                                'splits_PETR4.csv',
                                                                ('PCT_CHANGE(1):RAW_BOVESPA', 'percentual_PETR4.csv'))

    def test_should_return_correct_split_and_join_data_using_mocked_data_no_splits(self):
        testutils.assert_datasource_correctness_using_datafiles(self,
                                                                'NO-SPLITS',
                                                                'SPLITS:PCT_CHANGE(1):RAW_BOVESPA',
                                                                'splits_NO-SPLITS.csv',
                                                                ('PCT_CHANGE(1):RAW_BOVESPA', 'percentual_NO-SPLITS.csv'))

    def test_should_return_correct_split_and_join_data_using_mocked_data_with_splits(self):
        testutils.assert_datasource_correctness_using_datafiles(self,
                                                                'PETR4',
                                                                'SPLITS:PCT_CHANGE(1):RAW_BOVESPA',
                                                                'splits_WITH-SPLITS.csv',
                                                                ('PCT_CHANGE(1):RAW_BOVESPA', 'percentual_WITH-SPLITS.csv'))
