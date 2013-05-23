import bigtempo.tagselection as tagselection
import bigtempo.defaults as defaults


class DatasourceEngine(object):

    registrations = {}
    instances = {}

    def __init__(self, builder=defaults._ds_builder, processor_factory=defaults._ds_processor_factory):
        self.builder = builder
        self.processor_factory = processor_factory
        self.tag_selector = tagselection.TagSelector(self.get)

    def datasource(self, name, dependencies=[]):
        def wrapper(cls):
            self.register(name, cls, dependencies)
            return cls
        return wrapper

    def register(self, reference, cls, dependencies=None, lookback=0, tags=None):
        self.instances[reference] = None
        self.registrations[reference] = {
            'class': cls,
            'lookback': lookback,
            'dependencies': dependencies if dependencies else set(),
            'tags': tags if tags else set()
        }
        self.tag_selector.register(reference, tags)

    def select(self, *selectors):
        return self.tag_selector.get(*selectors)

    def get(self, reference):
        return self._create_processor(reference)

    def _create_processor(self, reference):
        instance = self._lazyload_datasource(reference)
        dependencies = map(self._create_processor, self.registrations[reference]['dependencies'])
        lookback_period = self.registrations[reference]['class']
        return self.processor_factory(instance, dependencies, lookback_period)

    def _lazyload_datasource(self, reference):
        if not self.instances.get(reference):
            if not self.registrations.get(reference):
                raise KeyError()
            self.instances[reference] = self.builder(self.registrations[reference]['class'])
        return self.instances[reference]


def datasource(name, dependencies=[]):
    def wrapper(cls):
        engine.register(name, cls, dependencies)
        return cls
    return wrapper


engine = DatasourceEngine(DatasourceBuilder())
