import itertools

from bigtempo.tagselection import TagSelector as TagSelector
import bigtempo.defaults as defaults


class DatasourceEngine(object):

    def __init__(self, builder=defaults.builder, processingtask_factory=defaults.processingtask_factory, tag_declarator=defaults.tag_declarator):
        self._registrations = {}
        self._instances = {}
        self._tag_selector = TagSelector(self.get)
        self._tag_declarator = tag_declarator
        self._tag_iteration_manager = TagSelectionIterationManager(self._registrations)
        self._processingtask_factory = processingtask_factory
        self._builder = builder

    def for_each(self, *selection, **kwargs):
        def wrapper(fn):
            self._tag_iteration_manager.register(fn, selection, kwargs.get('sync_by', None))
            return fn
        return wrapper

    def datasource(self, reference, dependencies=None, lookback=0, tags=None):
        def wrapper(cls):
            self._register_datasource(reference, cls, dependencies=dependencies, lookback=lookback, declared_tags=tags)
            return cls
        return wrapper

    def _register_datasource(self, reference, cls, dependencies=None, lookback=0, declared_tags=None):
        infered_tags = self._tag_declarator(reference, self._registrations)
        tags = _assure_is_valid_set(declared_tags) | _assure_is_valid_set(infered_tags)

        self._instances[reference] = None
        self._registrations[reference] = {
            'class': cls,
            'lookback': lookback,
            'dependencies': dependencies if dependencies else set(),
            'tags': tags
        }
        self._tag_selector.register(reference, tags)
        self._tag_iteration_manager.evaluate_new_candidate(reference)

    def select(self, *selectors):
        return self._tag_selector.get(*selectors)

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


def _assure_is_valid_set(obj):
    if not obj:
        obj = set()
    elif not isinstance(obj, set):
        try:
            obj = set(obj)
        except:
            obj = set()
    return obj


class TagSelectionIterationManager(object):

    def __init__(self, registrations):
        self._registrations = registrations
        self._mappings = []

    def register(self, fn, selections, sync_by=None):
        self._mappings.append((fn, selections, sync_by))
        self._evaluate_current_selections(fn, selections, sync_by)

    def evaluate_new_candidate(self, new_reference):
        for fn, selections, sync_by in self._mappings:
            self._evaluate_existing_selections(fn, selections, new_reference, sync_by)

    def _evaluate_existing_selections(self, fn, selections, new_reference, sync_by=None):
        partial_elegible_references_list = []
        current_partial_references_list = []

        for selection in selections:
            partial_references_list_copy = None

            if selection.is_elegible(new_reference):
                partial_references_list_copy = current_partial_references_list[:]
                partial_references_list_copy.append([new_reference])

            references = [reference for reference in selection]
            current_partial_references_list.append(references)
            for partial_elegible_references in partial_elegible_references_list:
                partial_elegible_references.append(references)

            if partial_references_list_copy:
                partial_elegible_references_list.append(partial_references_list_copy)

        for elegible_references_list in partial_elegible_references_list:
            combinations = itertools.product(*elegible_references_list)
            for combination in combinations:
                if sync_by is not None:
                    print 'Sync: ', sync_by
                    for reference in combination:
                        print reference,
                        print ' -> ',
                        print '?'
                    print ''
                self._execute_fn(fn, *combination)

    def _evaluate_current_selections(self, fn, selections, sync_by=None):
        references = [[reference for reference in selection] for selection in selections]
        combinations = itertools.product(*references)
        for combination in combinations:
            self._execute_fn(fn, *combination)

    def _execute_fn(self, fn, *references):
        fn(*references)
