import util.dateutils as dateutils
import bigtempo.utils as utils


def _builder(cls):
    return cls()


def _processing_task_factory(instance, dependencies, lookback_period):
    return ProcessingTask(instance, dependencies, lookback_period)


class ProcessingTask(object):

    def __init__(self, instance, dependencies, lookback_period):
        self.instance = instance
        self.dependencies = dependencies
        self.lookback_period = lookback_period

    def process(self, **kwargs):
        context = self._evaluate_datasource_dependencies(**kwargs)
        return self.instance.process(context, **kwargs)

    def _evaluate_datasource_dependencies(self, **kwargs):
        result = {}
        for reference, dependency in self.dependencies.iteritems():
            result[reference] = dependency.process(**kwargs)
        return result


class DataFrameDatasourceTask(object):

    def __init__(self, instance, dependencies, lookback_period):
        self.instance = instance
        self.dependencies = dependencies
        self.lookback_period = lookback_period

    def process(self, symbol, start=None, end=None):
        context = self._evaluate_datasource_dependencies(symbol, start, end)
        result = self.instance.process(context, symbol, start, end)
        return utils.slice_dataframe(result, start, end)

    def _evaluate_datasource_dependencies(self, reference, symbol, start=None, end=None):
        result = {}
        for reference, dependency in self.dependencies.iteritems():
            newStart = None if not start else dateutils.relative_working_day(-self.lookback_period, start)
            result[reference] = dependency.process(symbol, newStart, end)
        return result


class DatasourceContext(object):

    def __init__(self, dependencies):
        self.dependencies = dependencies

    def deps(self, reference=None):
        return self.dependencies.get(reference) if reference else self.dependencies
