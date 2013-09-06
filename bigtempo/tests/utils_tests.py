# -*- coding: utf-8 -*-


import pandas
import unittest

import bigtempo.utils as utils


class TestDatasourceLogger(unittest.TestCase):

    def test_log_should_not_break_given_empty_dataframe(self):
        logger = utils.DatasourceLogger()
        logger.log('Description', pandas.DataFrame())
        logger.print_summary()


class TestModuleFunctions(unittest.TestCase):

    def test_slice_given_start_and_end(self):
        data = [0, 1, 2, 3, 4, 5, 6, 7, 8, 9]

        result = utils.slice(data, 2, 8)
        assert result == data[2:8]

    def test_slice_given_start(self):
        data = [0, 1, 2, 3, 4, 5, 6, 7, 8, 9]

        result = utils.slice(data, 2)
        assert result == data[2:]

    def test_slice_given_end(self):
        data = [0, 1, 2, 3, 4, 5, 6, 7, 8, 9]

        result = utils.slice(data, end=8)
        assert result == data[:8]

    def test_slice_given_nothing(self):
        data = [0, 1, 2, 3, 4, 5, 6, 7, 8, 9]

        result = utils.slice(data)
        assert result == data

    def test_assure_is_valid_set_should_return_empty_set_when_invalid_object(self):
        result = utils.assure_is_valid_set(object())
        assert isinstance(result, set)
        assert len(result) is 0
