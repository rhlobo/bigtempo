import unittest

import bigtempo.utils as utils


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
