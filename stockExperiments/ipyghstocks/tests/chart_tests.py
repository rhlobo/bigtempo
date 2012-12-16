import unittest
import ipyghstocks.chart as chart


class TestIpyghstocksChartModuleGenerateIdFunction(unittest.TestCase):

    def test_generate_id_function_should_always_return_different_ids(self):
        ids = {}
        for i in range(100):
            generated = chart._generate_id()
            assert ids.get(generated) is None
            ids[generated] = generated
