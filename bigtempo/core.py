# -*- coding: utf-8 -*-


import bigtempo.utils as utils
import bigtempo.defaults as defaults
import bigtempo.tagselection as tagselection


class DatasourceEngine(object):

    def __init__(self,
                 datasource_factory=defaults.datasource_factory,
                 processing_task_factory=defaults.task_factory):

        self._registrations = {}
        self._instances = {}
        self._tag_selector = tagselection.TagSelector(self.get)
        self._tag_iteration_manager = tagselection.TagManager(self._registrations)
        self._processing_task_factory = processing_task_factory
        self._datasource_factory = datasource_factory

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

    def datasource(self, reference, dependencies=None, tags=None, lookback=0, frequency=None):
        def wrapper(cls):
            self._register_datasource(reference,
                                      cls,
                                      dependencies=dependencies,
                                      tags=tags,
                                      lookback=lookback,
                                      frequency=frequency)
            return cls
        return wrapper

    def _register_datasource(self, reference, cls, dependencies=None, tags=None, lookback=0, frequency=None):
        self._instances[reference] = None
        self._registrations[reference] = {
            'class': cls,
            'lookback': lookback,
            'frequency': frequency,
            'dependencies': set(dependencies) if dependencies else set()
        }

        infered_tags = self._tag_iteration_manager.infere_tags(reference)
        all_tags = utils.assure_is_valid_set(tags) | utils.assure_is_valid_set(infered_tags)

        self._registrations[reference]['tags'] = all_tags
        self._tag_selector.register(reference, all_tags)
        self._tag_iteration_manager.evaluate_new_candidate(reference)

    def select(self, *selectors):
        return self._tag_selector.get(*selectors)

    def tags(self, *references):
        return self._tag_selector.tags(*references)

    def get(self, reference):
        return self._create_processor(reference)

    def _create_processor(self, reference):
        instance = self._lazyload_datasource(reference)
        registration = self._registrations[reference]
        dependencies = dict((dependency, self._create_processor(dependency)) for dependency in registration['dependencies'])
        return self._processing_task_factory(instance, registration, dependencies)

    def _lazyload_datasource(self, reference):
        if not self._instances.get(reference):
            if not self._registrations.get(reference):
                raise KeyError()
            self._instances[reference] = self._datasource_factory(self._registrations[reference]['class'])
        return self._instances[reference]
