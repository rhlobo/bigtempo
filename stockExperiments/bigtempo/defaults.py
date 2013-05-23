import util.dateutils as dateutils
import bigtempo.utils as utils


def _ds_builder(cls):
    return cls()


def _ds_processor_factory(instance, dependencies, lookback_period):
    pass


class DatasourceEvaluator(object):

    def evaluate(self, reference, symbol, start=None, end=None):
        context = self._create_datasource_context(reference, symbol, start, end)
        result = self._get_datasource(reference).evaluate(context, symbol, start, end)
        return utils.slice_dataframe(result, start, end)

    def _create_datasource_context(self, reference, symbol, start=None, end=None):
        return DatasourceContext(self._evaluate_datasource_dependencies(reference, symbol, start, end))

    def _evaluate_datasource_dependencies(self, reference, symbol, start=None, end=None):
        if not self.registrations.get(reference):
            raise ValueError()

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
