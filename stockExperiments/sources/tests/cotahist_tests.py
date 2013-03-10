import unittest
import os
import pandas
import datetime
import sources.cotahist as cotahist


class TestCotahistModuleFunctions(unittest.TestCase):

    def test_function_getCotahistFilePaths_should_return_list_of_paths(self):
        result = cotahist._get_cotahist_file_paths(_get_test_data_dir())
        assert isinstance(result, list)

    def test_function_getCotahistFilePaths_should_return_valid_paths(self):
        result = cotahist._get_cotahist_file_paths(_get_test_data_dir())
        for path in result:
            assert os.path.exists(path)

    def test_function_getCotahistFilePaths_should_return_correct_file_paths(self):
        result = cotahist._get_cotahist_file_paths(_get_test_data_dir())
        assert len(result) == 2
        assert result == _get_test_data_file_path(['COTAHIST_A0001.txt', 'COTAHIST_A0002.txt'])

    def test_function_importData_should_ignore_non_regural_stock_data(self):
        data1 = cotahist._import_data(_get_test_data_file_path(['COTAHIST_A2007_PETR_1.txt']))
        data2 = cotahist._import_data(_get_test_data_file_path(['COTAHIST_A2007_PETR_2.txt']))
        assert len(data1) == len(data2)

    def test_function_importData_should_import_all_stock_data_in_files(self):
        data = cotahist._import_data(_get_test_data_file_path(['COTAHIST_A2007_PETR_2.txt']))
        assert len(data) == 490

    def test_function_importData_should_import_correct_stock_data_from_file(self):
        data = cotahist._import_data(_get_test_data_file_path(['COTAHIST_A0001.txt']))
        assert len(data) == 4
        assert data[0] == ['PETR3', datetime.date(2007, 1, 2), 54.59, 54.59, 55.75, 55.75, 4005841900L]
        assert data[1] == ['PETR4', datetime.date(2007, 1, 2), 50.0, 49.76, 50.45, 50.45, 25611540900L]
        assert data[2] == ['PETR3', datetime.date(2007, 1, 3), 55.0, 53.09, 55.6, 53.6, 18035053900L]
        assert data[3] == ['PETR4', datetime.date(2007, 1, 3), 50.16, 48.01, 50.4, 48.7, 49259125600L]

    def test_function_importData_should_import_correct_stock_data_from_multiple_files(self):
        ls_files = ['COTAHIST_A0001.txt', 'COTAHIST_A0002.txt']
        data = cotahist._import_data(_get_test_data_file_path(ls_files))
        assert len(data) == 6
        assert data[0] == ['PETR3', datetime.date(2007, 1, 2), 54.59, 54.59, 55.75, 55.75, 4005841900L]
        assert data[2] == ['PETR3', datetime.date(2007, 1, 3), 55.0, 53.09, 55.6, 53.6, 18035053900L]
        assert data[4] == ['PETR3', datetime.date(2007, 12, 28), 103.7, 102.7, 105.0, 105.0, 19191030700L]
        assert data[1] == ['PETR4', datetime.date(2007, 1, 2), 50.0, 49.76, 50.45, 50.45, 25611540900L]
        assert data[3] == ['PETR4', datetime.date(2007, 1, 3), 50.16, 48.01, 50.4, 48.7, 49259125600L]
        assert data[5] == ['PETR4', datetime.date(2007, 12, 28), 86.2, 85.87, 88.4, 88.4, 114741063300L]


class TestCotahistImporter(unittest.TestCase):

    def test_should_load_a_map_with_each_stock_paper_as_keys(self):
        d_dataFrame = cotahist.CotahistImporter(_get_test_data_dir()).getDataFrameMap()
        assert len(d_dataFrame.keys()) == 2
        for s_stock in ['PETR3', 'PETR4']:
            assert s_stock in d_dataFrame.keys()

    def test_should_load_maps_with_dataFrames(self):
        d_dataFrame = cotahist.CotahistImporter(_get_test_data_dir()).getDataFrameMap()
        for value in [d_dataFrame[key] for key in d_dataFrame]:
            assert isinstance(value, pandas.DataFrame)

    def test_should_load_each_dataFrame_with_all_data(self):
        d_dataFrame = cotahist.CotahistImporter(_get_test_data_dir()).getDataFrameMap()
        for s_stock in ['PETR3', 'PETR4']:
            assert len(d_dataFrame[s_stock]) == 3

    def test_should_load_each_dataFrame_with_5_columns(self):
        d_dataFrame = cotahist.CotahistImporter(_get_test_data_dir()).getDataFrameMap()
        for s_stock in ['PETR3', 'PETR4']:
            assert len(d_dataFrame[s_stock].columns) == 5

    def test_should_load_each_dataFrame_with_correct_columns(self):
        expectedColumns = ['open', 'high', 'low', 'close', 'volume']
        d_dataFrame = cotahist.CotahistImporter(_get_test_data_dir()).getDataFrameMap()
        for s_stock in ['PETR3', 'PETR4']:
            columns = d_dataFrame[s_stock].columns
            for i in range(len(columns)):
                assert columns[i] == expectedColumns[i]

    def test_should_load_each_dataFrame_with_correct_data(self):
        d_dataFrame = cotahist.CotahistImporter(_get_test_data_dir()).getDataFrameMap()

        df_petr4 = d_dataFrame['PETR4']
        self._assert_column_values(df_petr4['open'], [50.0, 50.16, 86.2])
        self._assert_column_values(df_petr4['high'], [50.45, 50.4, 88.4])
        self._assert_column_values(df_petr4['low'], [49.76, 48.01, 85.87])
        self._assert_column_values(df_petr4['close'], [50.45, 48.7, 88.4])
        self._assert_column_values(df_petr4['volume'], [25611540900, 49259125600, 114741063300])

    def _assert_column_values(self, timeSeries, l_values):
        for i in range(len(l_values)):
            assert timeSeries[i] == l_values[i]


def _get_test_data_dir():
    test_data_dir_name = 'cotahist_tests_data'
    test_dir = os.path.split(__file__)[0]
    return os.path.abspath(os.path.join(test_dir, test_data_dir_name))


def _get_test_data_file_path(ls_filenames):
    result = []
    for s_filename in ls_filenames:
        result.append(os.path.abspath(os.path.join(_get_test_data_dir(), s_filename)))
    return result
