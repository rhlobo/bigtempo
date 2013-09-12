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


@engine.datasource('SAMPLE',
                   tags=['SAMPLE_IN', 'DAILY'])
class Sample(object):

    def evaluate(self, context, symbol, start=None, end=None):
        return pandas.read_csv(_get_test_data_file('SAMPLE_SOURCE_1', symbol))


@engine.datasource('WEEKLY_SAMPLE',
                   dependencies=['SAMPLE'],
                   tags=['SAMPLE_IN', 'WEEKLY'],
                   frequency='W-FRI')
class Weekly(object):

    def evaluate(self, context, symbol, start=None, end=None):
        return context.dependencies('SAMPLE').resample('W-FRI', how=lambda x: x[-1])


@engine.datasource('MONTHLY_SAMPLE',
                   dependencies=['SAMPLE'],
                   tags=['SAMPLE_IN', 'MONTHLY'],
                   frequency='BM')
class Monthly(object):

    def evaluate(self, context, symbol, start=None, end=None):
        return context.dependencies('SAMPLE').resample('BM', how=lambda x: x[-1])


@engine.for_each(engine.select('SAMPLE_IN'))
def _percentual_change_factory(source_reference):

    @engine.datasource('PERCENTUALT_CHANGE:%s' % source_reference,
                       dependencies=[source_reference],
                       lookback=1,
                       tags=['PERCENTUALT_CHANGE'])
    class PctChange(object):

        def evaluate(self, context, symbol, start=None, end=None):
            return context.dependencies(source_reference).pct_change()


for symbol in symbols:
    tester.generate_for_references(engine,
                                   engine.select().all().difference('SAMPLE_INPUT'),
                                   symbol,
                                   None,
                                   None,
                                   _get_test_data_dir(),
                                   sys.modules[__name__])
