import bigtempo.tagselection as tagselection
import bigtempo.defaults as defaults


class DatasourceEngine(object):

    def __init__(self, builder=defaults._builder, processing_task_factory=defaults._processing_task_factory):
        self.registrations = {}
        self.instances = {}
        self.builder = builder
        self.tag_selector = tagselection.TagSelector(self.get)
        self.processing_task_factory = processing_task_factory

    def datasource(self, reference, dependencies=None, lookback=0, tags=None):
        def wrapper(cls):
            self._register(reference, cls, dependencies=dependencies, lookback=lookback, tags=tags)
            return cls
        return wrapper

    def select(self, *selectors):
        return self.tag_selector.get(*selectors)

    def get(self, reference):
        return self._create_processor(reference)

    def _register(self, reference, cls, dependencies=None, lookback=0, tags=None):
        tags = tags if tags else set()

        self.instances[reference] = None
        self.registrations[reference] = {
            'class': cls,
            'lookback': lookback,
            'dependencies': dependencies if dependencies else set(),
            'tags': tags
        }
        self.tag_selector.register(reference, tags)

    def _create_processor(self, reference):
        instance = self._lazyload_datasource(reference)
        dependencies = map(self._create_processor, self.registrations[reference]['dependencies'])
        lookback_period = self.registrations[reference]['class']
        return self.processing_task_factory(instance, dependencies, lookback_period)

    def _lazyload_datasource(self, reference):
        if not self.instances.get(reference):
            if not self.registrations.get(reference):
                raise KeyError()
            self.instances[reference] = self.builder(self.registrations[reference]['class'])
        return self.instances[reference]
