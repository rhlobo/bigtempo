import unittest
import pandas
import util.pandasutils as util


class TestDataframeToListOfListsFunction(unittest.TestCase):

    def test_should_accept_DataFrame_and_output_list(self):
        result = util.dataframe_to_list_of_lists(self._createDataframe())
        assert isinstance(result, list)

    def test_should_output_list_of_lists(self):
        result = util.dataframe_to_list_of_lists(self._createDataframe())
        for i in result:
            assert isinstance(i, list)

    def test_output_should_have_correct_values(self):
        result = util.dataframe_to_list_of_lists(self._createDataframe())
        dl_data = self._createMapOfLists()
        i = 0
        for r, d in map(None, result, zip(dl_data['one'], dl_data['two'])):
            assert r[1] == d[0]
            assert r[2] == d[1]
            assert r[0] == i
            i += 1

    def _createMapOfLists(self):
        return {
            'one': [1., 2., 3., 4.],
            'two': [4., 3., 2., 1.]
        }

    def _createDataframe(self):
        return pandas.DataFrame(self._createMapOfLists())
