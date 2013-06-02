import util.dateutils as dateutils
import bigtempo.utils as utils


def builder(cls):
    return cls()


def processingtask_factory(instance, dependencies, **kwargs):
    return DatasourceTask(instance, dependencies)


class DatasourceTask(object):

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
            newStart = None if not start else dateutils.relative_working_day(-self._lookback_period, start)
            result[reference] = dependency.process(symbol, newStart, end)
        return result


class DatasourceContext(object):

    def __init__(self, dependencies):
        self._dependencies = dependencies

    def dependencies(self, reference=None):
        return self._dependencies.get(reference) if reference else self._dependencies
