from bigtempo.tagselection import TagSelector as TagSelector
import bigtempo.defaults as defaults


class DatasourceEngine(object):

    def __init__(self, builder=defaults.builder, processingtask_factory=defaults.processingtask_factory):
        self._registrations = {}
        self._instances = {}
        self._builder = builder
        self._tag_selector = TagSelector(self.get)
        self._processingtask_factory = processingtask_factory

    def datasource(self, reference, dependencies=None, lookback=0, tags=None):
        def wrapper(cls):
            self._register_datasource(reference, cls, dependencies=dependencies, lookback=lookback, tags=tags)
            return cls
        return wrapper

    def _register_datasource(self, reference, cls, dependencies=None, lookback=0, tags=None):
        if not tags:
            tags = set()
        if not isinstance(tags, set):
            tags = set(tags)

        self._instances[reference] = None
        self._registrations[reference] = {
            'class': cls,
            'lookback': lookback,
            'dependencies': dependencies if dependencies else set(),
            'tags': tags
        }
        self._tag_selector.register(reference, tags)

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
