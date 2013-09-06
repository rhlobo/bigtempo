# -*- coding: utf-8 -*-


import pandas
import datetime

import bigtempo.utils as utils


def factory(instance, registration, dependencies, *args, **kwargs):
    return DataFrameDatasourceTask(instance, registration, dependencies)


class DataFrameDatasourceTask(object):

    def __init__(self, instance, registration, dependencies):
        self._instance = instance
        self._registration = registration
        self._dependencies = dependencies

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
            new_start = None if not start else evaluate_loopback_period(self._registration['lookback'],
                                                                        self._registration['frequency'],
                                                                        start)
            result[reference] = dependency.process(symbol, new_start, end)
        return result


class DatasourceContext(object):

    def __init__(self, dependencies):
        self._dependencies = dependencies

    def dependencies(self, reference=None):
        return self._dependencies.get(reference) if reference else self._dependencies


def evaluate_loopback_period(lookback, frequency, date):
    if frequency == 'B':
        lookback = int(lookback * 1.05)
    lookback += 2

    return relative_period(-lookback, frequency, date)


def relative_period(periods, frequency, date=None):
    business_day = equivalent_business_day() if not date else equivalent_business_day(date)
    return (pandas.Period(business_day, freq=frequency) + periods).to_timestamp()


def equivalent_business_day(date=None):
    if not date:
        date = datetime.datetime.today().replace(hour=0,
                                                 minute=0,
                                                 second=0,
                                                 microsecond=0)

    isoweekday = date.isoweekday()
    return date if isoweekday <= 5 else date - datetime.timedelta(isoweekday - 5)
