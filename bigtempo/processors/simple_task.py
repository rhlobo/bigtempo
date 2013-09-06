# -*- coding: utf-8 -*-


def factory(instance, registration, dependencies, *args, **kwargs):
    return SimpleDatasourceTask(instance, registration, dependencies)


class SimpleDatasourceTask(object):

    def __init__(self, instance, registration, dependencies):
        self._instance = instance
        self._dependencies = dependencies

    def process(self, **kwargs):
        context = self._evaluate_datasource_dependencies(**kwargs)
        return self._instance.evaluate(context, **kwargs)

    def _evaluate_datasource_dependencies(self, **kwargs):
        return dict((reference, dependency.process(**kwargs)) for reference, dependency in self._dependencies.iteritems())
