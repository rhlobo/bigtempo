# -*- coding: utf-8 -*-


import pandas
import datetime

import bigtempo.utils as utils


def builder(cls):
    return cls()


def processingtask_factory(instance, dependencies, *args, **kwargs):
    return DataFrameDatasourceTask(instance, dependencies, *args, **kwargs)


class SimpleDatasourceTask(object):

    def __init__(self, instance, dependencies):
        self._instance = instance
        self._dependencies = dependencies

    def process(self, **kwargs):
        context = self._evaluate_datasource_dependencies(**kwargs)
        return self._instance.evaluate(context, **kwargs)

    def _evaluate_datasource_dependencies(self, **kwargs):
        return dict((reference, dependency.process(**kwargs)) for reference, dependency in self._dependencies.iteritems())


class DataFrameDatasourceTask(object):

    def __init__(self, instance, dependencies, lookback_period=0):
        self._instance = instance
        self._dependencies = dependencies
        # TODO: Remove lookback period from this object, read it from the instance instead
        self._lookback_period = lookback_period

    def process(self, symbol, start=None, end=None):
        context = self._create_context_for(symbol, start, end)
        result = self._instance.evaluate(context, symbol, start, end)
        return utils.slice(result, start, end)

    def _create_context_for(self, symbol, start=None, end=None):
        evaluated_dependencies = self._evaluate_datasource_dependencies(symbol, start, end)
        return DatasourceContext(evaluated_dependencies)

    def _evaluate_datasource_dependencies(self, symbol, start=None, end=None):
        result = {}
        for reference, dependency in self._dependencies.iteritems():
            # TODO: Pass freq on to this object, read it from the instance instead
            new_start = None if not start else evaluate_loopback_period(self._lookback_period, start)
            result[reference] = dependency.process(symbol, new_start, end)
        return result


class DatasourceContext(object):

    def __init__(self, dependencies):
        self._dependencies = dependencies

    def dependencies(self, reference=None):
        return self._dependencies.get(reference) if reference else self._dependencies


def evaluate_loopback_period(lookback_period, date, freq='B'):
    if freq == 'B':
        lookback_period = int(lookback_period * 1.05)
    lookback_period += 1

    return relative_period(-lookback_period, date, freq)


def relative_period(periods, date=None, freq='B'):
    business_day = equivalent_business_day() if not date else equivalent_business_day(date)
    #return business_day + (periods * pandas.tseries.offsets.BDay())
    return (pandas.Period(business_day, freq=freq) + periods).to_timestamp()


def equivalent_business_day(date=None):
    if not date:
        date = datetime.datetime.today().replace(hour=0,
                                                 minute=0,
                                                 second=0,
                                                 microsecond=0)

    isoweekday = date.isoweekday()
    return date if isoweekday <= 5 else date - datetime.timedelta(isoweekday - 5)
