import unittest
import inspect
import os
import util.fileutils as util


class TestFileutilsModuleFunctions(unittest.TestCase):

    def test_module_should_have_listdir_funciton(self):
        assert 'listdir' in [name for name, method in inspect.getmembers(util, predicate=inspect.isfunction)]

    def test_listdir_method_should_accept_1_args(self):
        util.listdir('.')

    def test_listdir_method_should_accept_2_args(self):
        util.listdir('.', r'.*')

    def test_listdir_method_should_accept_3_args(self):
        util.listdir('.', r'.*', _path_sort)

    def test_listdir_method_should_return_all_files_in_dir_ordered(self):
        expected_files = ['1.1', '1.2', 'a.txt', 'b.txt', 'c.txt', 'arquivo1', 'arquivo2', 'arquivo3', 'data.dat']
        result = util.listdir(_get_test_data_dir())
        assert len(result) == len(expected_files)
        for filepath in result:
            assert os.path.basename(filepath) in expected_files

    def test_listdir_method_should_return_some_files_in_dir_01(self):
        expected_files = ['1.1', '1.2', 'a.txt', 'b.txt', 'c.txt']
        result = util.listdir(_get_test_data_dir(), r'^\w\.\w+$')
        assert len(result) == len(expected_files)
        for filepath in result:
            assert os.path.basename(filepath) in expected_files

    def test_listdir_method_should_return_some_files_in_dir_02(self):
        expected_files = ['data.dat']
        result = util.listdir(_get_test_data_dir(), r'^\w+\.dat$')
        assert len(result) == len(expected_files)
        for filepath in result:
            assert os.path.basename(filepath) in expected_files

    def test_listdir_method_should_return_files_ordered_by_given_function(self):
        expected_files = ['1.1', 'arquivo1', '1.2', 'arquivo2', 'arquivo3', 'data.dat', 'a.txt', 'b.txt', 'c.txt']
        result = util.listdir(_get_test_data_dir(), f_sort=_path_sort)
        assert len(result) == len(expected_files)
        for i in range(len(result)):
            assert os.path.basename(result[i]) == expected_files[i]

    def test_get_test_data_file_path_should_return_test_data_file_path(self):
        filename = 'arquivo1'
        expected_filepath = os.path.abspath(os.path.join(_get_test_data_dir(), filename))
        assert util.get_test_data_file_path(__file__, filename) == expected_filepath

    def test_get_test_data_files_path_should_return_multiple_test_data_file_path(self):
        filenames = ['arquivo1', '1.1']
        for filename in filenames:
            expected_filepath = os.path.abspath(os.path.join(_get_test_data_dir(), filename))
            assert util.get_test_data_file_path(__file__, filename) == expected_filepath


def _get_test_data_dir():
    test_data_dir_name = 'fileutils_tests_data'
    test_dir = os.path.split(__file__)[0]
    return os.path.join(test_dir, test_data_dir_name)


def _path_sort(path):
    return path[::-1]
