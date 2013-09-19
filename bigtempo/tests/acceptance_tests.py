# -*- coding: utf-8 -*-


import os
import sys
import pandas
import datetime
import bigtempo.core as core
import bigtempo.auditor as auditor


dt = datetime.datetime
cities = ['CITY_A', 'CITY_B']
engine = core.DatasourceEngine()


def _get_test_data_dir():
    return os.path.abspath(os.path.join('tests', 'acceptance_tests_data'))


def _get_test_data_filename(reference, symbol=None):
    symbol_part = '' if not symbol else '{%s}' % symbol
    return '%s%s.csv' % (reference, symbol_part)


def _get_test_data_filepath(reference, symbol=None):
    return os.path.join(_get_test_data_dir(), _get_test_data_filename(reference, symbol))


@engine.datasource('SAMPLE',
                   tags=['SAMPLE_IN', 'DAILY'],
                   frequency='B')
class Sample(object):

    def evaluate(self, context, symbol, start=None, end=None):
        return pandas.DataFrame.from_csv(_get_test_data_filepath('SAMPLE', symbol))


@engine.datasource('WEEKLY_SAMPLE',
                   dependencies=['SAMPLE'],
                   tags=['SAMPLE_IN', 'WEEKLY'],
                   frequency='W-FRI')
class Weekly(object):

    def evaluate(self, context, symbol, start=None, end=None):
        return context.dependencies('SAMPLE').resample('W-FRI', how=lambda x: x[-1])


@engine.for_each(engine.select('SAMPLE_IN'))
def _rolling_mean_factory(source_reference):

    @engine.datasource('ROLLING_MEAN:%s' % source_reference,
                       dependencies=[source_reference],
                       lookback=7,
                       tags=['ROLLING_MEAN'])
    class RollingMean(object):

        def evaluate(self, context, symbol, start=None, end=None):
            input_ds = context.dependencies(source_reference)
            return pandas.rolling_mean(input_ds, 7)


@engine.datasource('MONTHLY_SAMPLE',
                   dependencies=['SAMPLE'],
                   tags=['SAMPLE_IN', 'MONTHLY'],
                   frequency='M')
class Monthly(object):

    def evaluate(self, context, symbol, start=None, end=None):
        return context.dependencies('SAMPLE').resample('M', how=lambda x: x[-1])


@engine.for_each(engine.select('SAMPLE_IN').union('ROLLING_MEAN'))
def _percentual_change_factory(source_reference):

    @engine.datasource('PERCENTUALT_CHANGE:%s' % source_reference,
                       dependencies=[source_reference],
                       lookback=1,
                       tags=['PERCENTUALT_CHANGE'])
    class PctChange(object):

        def evaluate(self, context, symbol, start=None, end=None):
            return context.dependencies(source_reference).pct_change()


for city in cities:
    auditor.generate_multiple(engine,
                              engine.select().all().difference('SAMPLE'),
                              city,
                              None,
                              None,
                              _get_test_data_filepath,
                              sys.modules[__name__])
    auditor.generate_multiple(engine,
                              engine.select().all().difference('SAMPLE'),
                              city,
                              dt(2001, 1, 1),
                              dt(2002, 1, 1),
                              _get_test_data_filepath,
                              sys.modules[__name__])


def test_all_test_methods_are_being_generated():
    result = []
    for city in cities:
        result.extend(list(auditor.generate_multiple(engine,
                                                     engine.select().all().difference('SAMPLE'),
                                                     city,
                                                     None,
                                                     None,
                                                     _get_test_data_filepath)))
    assert len(result) == 22
