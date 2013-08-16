# -*- coding: utf-8 -*-


import bigtempo.utils as utils
import bigtempo.defaults as defaults
import bigtempo.tagselection as tagselection


class DatasourceEngine(object):

    def __init__(self,
                 builder=defaults.builder,
                 processingtask_factory=defaults.processingtask_factory):
        self._registrations = {}
        self._instances = {}
        self._tag_selector = tagselection.TagSelector(self.get)
        self._tag_iteration_manager = tagselection.TagManager(self._registrations)
        self._processingtask_factory = processingtask_factory
        self._builder = builder

    def for_each(self, *selection):
        def wrapper(fn):
            self._tag_iteration_manager.register(fn, *selection)
            return fn
        return wrapper

    def for_synched(self, *selection):
        def wrapper(fn):
            self._tag_iteration_manager.register_synched(fn, selection)
            return fn
        return wrapper

    def datasource(self, reference, dependencies=None, lookback=0, tags=None):
        def wrapper(cls):
            self._register_datasource(reference, cls, dependencies=dependencies, lookback=lookback, declared_tags=tags)
            return cls
        return wrapper

    def _register_datasource(self, reference, cls, dependencies=None, lookback=0, declared_tags=None):
        self._instances[reference] = None
        self._registrations[reference] = {
            'class': cls,
            'lookback': lookback,
            'dependencies': set(dependencies) if dependencies else set()
        }

        infered_tags = self._tag_iteration_manager.infere_tags(reference)
        tags = utils.assure_is_valid_set(declared_tags) | utils.assure_is_valid_set(infered_tags)

        self._registrations[reference]['tags'] = tags
        self._tag_selector.register(reference, tags)
        self._tag_iteration_manager.evaluate_new_candidate(reference)

    def select(self, *selectors):
        return self._tag_selector.get(*selectors)

    def tags(self, *references):
        return self._tag_selector.tags(*references)

    def get(self, reference):
        return self._create_processor(reference)

    def _create_processor(self, reference):
        instance = self._lazyload_datasource(reference)
        dependencies = dict((dependency, self._create_processor(dependency)) for dependency in self._registrations[reference]['dependencies'])
        lookback_period = self._registrations[reference]['lookback']
        return self._processingtask_factory(instance, dependencies, lookback_period)

    def _lazyload_datasource(self, reference):
        if not self._instances.get(reference):
            if not self._registrations.get(reference):
                raise KeyError()
            self._instances[reference] = self._builder(self._registrations[reference]['class'])
        return self._instances[reference]
