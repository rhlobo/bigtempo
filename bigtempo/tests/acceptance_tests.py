# -*- coding: utf-8 -*-


import sys
import pandas
import bigtempo.core as core
import bigtempo.tester as tester


engine = core.DatasourceEngine()
symbols = ['CITY_A', 'CITY_B']


def _get_test_data_dir():
    return ''


def _get_test_data_file(reference, symbol):
    return ''


@engine.datasource('SAMPLE_SOURCE_1',
                   tags=['SAMPLE_INPUT'])
class Sample1(object):

    def evaluate(self, context, symbol, start=None, end=None):
        return pandas.read_csv(_get_test_data_file('SAMPLE_SOURCE_1', symbol))


@engine.datasource('SAMPLE_SOURCE_2',
                   tags=['SAMPLE_INPUT'])
class Sample2(object):

    def evaluate(self, context, symbol, start=None, end=None):
        return pandas.read_csv(_get_test_data_file('SAMPLE_SOURCE_2', symbol))


for symbol in symbols:
    tester.generate_for_references(engine,
                                   engine.select().all().difference('SAMPLE_INPUT'),
                                   symbol,
                                   None,
                                   None,
                                   _get_test_data_dir(),
                                   sys.modules[__name__])
