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

    def process(self, reference, **kwargs):
        context = self._evaluate_datasource_dependencies(reference, **kwargs)
        return self.instance.evaluate(context, **kwargs)

    def _evaluate_datasource_dependencies(self, reference, symbol, start=None, end=None):
        if not self.registrations.get(reference):
            raise ValueError()

        result = {}
        for dependency in self.dependencies:
            newStart = None if not start else dateutils.relative_working_day(-lookback_period, start)
            result[reference] = self.evaluate(reference, symbol, newStart, end)
        return result


class DataFrameDatasourceTask(object):

    def __init__(self, instance, dependencies, lookback_period):
        self.instance = instance
        self.dependencies = dependencies
        self.lookback_period = lookback_period

    def evaluate(self, reference, symbol, start=None, end=None):
        context = self._evaluate_datasource_dependencies(reference, symbol, start, end)
        result = self._get_datasource(reference).evaluate(context, symbol, start, end)
        return utils.slice_dataframe(result, start, end)

    def _evaluate_datasource_dependencies(self, reference, symbol, start=None, end=None):
        result = {}
        for dependency in self.registrations[reference]['dependencies']:
            reference, lookback_period = (dependency, 0) if isinstance(dependency, str) else (dependency[0], dependency[1])
            newStart = None if not start else dateutils.relative_working_day(-lookback_period, start)
            result[reference] = self.evaluate(reference, symbol, newStart, end)
        return result


class DatasourceContext(object):

    def __init__(self, dependencies):
        self.dependencies = dependencies

    def deps(self, reference=None):
        return self.dependencies.get(reference) if reference else self.dependencies
