from bigtempo.tagselection import TagSelector as TagSelector
import bigtempo.defaults as defaults


class DatasourceEngine(object):

    def __init__(self, builder=defaults.builder, processingtask_factory=defaults.processingtask_factory, tag_declarator=defaults.tag_declarator):
        self._factory_manager = FactoryManager()
        self._registrations = {}
        self._instances = {}
        self._tag_selector = TagSelector(self.get)
        self._tag_declarator = tag_declarator
        self._processingtask_factory = processingtask_factory
        self._builder = builder

    def datasource_factory(self, selection):
        def wrapper(factory):
            self._factory_manager.register(factory, selection)
            return factory
        return wrapper

    def datasource(self, reference, dependencies=None, lookback=0, tags=None):
        def wrapper(cls):
            self._register_datasource(reference, cls, dependencies=dependencies, lookback=lookback, declared_tags=tags)
            return cls
        return wrapper

    def _register_datasource(self, reference, cls, dependencies=None, lookback=0, declared_tags=None):
        infered_tags = self._tag_declarator(reference, cls, dependencies, lookback)
        tags = _assure_is_valid_set(declared_tags) | _assure_is_valid_set(infered_tags)

        self._instances[reference] = None
        self._registrations[reference] = {
            'class': cls,
            'lookback': lookback,
            'dependencies': dependencies if dependencies else set(),
            'tags': tags
        }
        self._tag_selector.register(reference, tags)
        self._factory_manager.evaluate_new_candidate(reference)

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


class FactoryManager(object):

    def __init__(self):
        self.mappings = []

    def register(self, factory, selection):
        self.mappings.append((factory, selection))
        self._evaluate_current_selection(factory, selection)

    def evaluate_new_candidate(self, reference):
        for factory, selection in self.mappings:
            if selection.is_elegible(reference):
                self._execute_factory(factory, reference)

    def _evaluate_current_selection(self, factory, selection):
        for reference in selection:
            self._execute_factory(factory, reference)

    def _execute_factory(self, factory, reference):
        factory(reference)
