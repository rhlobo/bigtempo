# -*- coding: utf-8 -*-


import pandas
import datetime

import bigtempo.utils as utils


_DEFAULT_FREQUENCY = 'B'
_KNOWN_FREQUENCIES = ['U', 'L', 'S', 'T', 'H', 'B', 'W', 'BMS', 'BM', 'MS', 'M', 'BQS', 'BQ', 'QS', 'Q', 'BAS', 'BA', 'AS', 'A']
_FREQUENCY_ENUMERATION_DICT = dict((y, x) for x, y in enumerate(_KNOWN_FREQUENCIES))


def factory(instance, registration, dependency_dict, *args, **kwargs):
    return DataFrameDatasourceTask(instance, registration, dependency_dict)


class DataFrameDatasourceTask(object):

    def __init__(self, instance, registration, dependency_dict):
        self._instance = instance
        self._dependency_dict = dependency_dict
        self._registration = registration

    def process(self, symbol, start=None, end=None):
        context = self._create_context_for(symbol, start, end)
        result = self._instance.evaluate(context, symbol, start, end)
        return utils.slice(result, start, end)

    def _create_context_for(self, symbol, start=None, end=None):
        evaluated_dependencies = self._evaluate_datasource_dependencies(symbol, start, end)
        return DatasourceContext(evaluated_dependencies)

    def _evaluate_datasource_dependencies(self, symbol, start=None, end=None):
        result = {}

        new_start = None if not start else evaluate_loopback_period(self._registration,
                                                                    self._dependency_dict.values(),
                                                                    start)

        for reference, dependency in self._dependency_dict.iteritems():
            result[reference] = dependency.process(symbol, new_start, end)
        return result


class DatasourceContext(object):

    def __init__(self, dependencies):
        self._dependencies = dependencies

    def dependencies(self, reference=None):
        return self._dependencies.get(reference) if reference else self._dependencies


def evaluate_loopback_period(datasource_registration, dependencies, date):
    lookback = datasource_registration['lookback']
    frequency = determine_frequency(datasource_registration.get('frequency'), dependencies)

    # Holiday workaround
    if frequency in ['B', 'C']:
        lookback = 1 + int(lookback * 1.08)

    lookback += 1

    return relative_period(-lookback, frequency, date)


def determine_frequency(datasource_frequency=None, dependencies=None):
    if not datasource_frequency is None:
        return datasource_frequency

    if dependencies is None or len(dependencies) is 0:
        return _DEFAULT_FREQUENCY

    dependencies_frequencies = []
    for dependency in dependencies:
        dependency_frequency = dependency._registration.get('frequency')
        dependency_dependencies = dependency._dependency_dict.values()
        dependencies_frequencies.append(determine_frequency(dependency_frequency, dependency_dependencies))

    return max(dependencies_frequencies, key=_frequency_sort_key)


def _frequency_sort_key(value):
    frequency = value.split('-')[0]
    if not frequency in _FREQUENCY_ENUMERATION_DICT:
        return 0

    return _FREQUENCY_ENUMERATION_DICT[frequency]


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
