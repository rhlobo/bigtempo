import util.dateutils as dateutils


def _ds_builder(cls):
    return cls()


def _ds_processor_factory():
    pass


class TagSelectorFactory(object):

    def __init__(self, factory, selection, callable_visitor):
        self.factory = factory
        self.selection = selection
        self.callable_visitor = callable_visitor
        self.tag_mappings = None

    def __call__(self, *selectors):
        return _TagSelector(self, self.tag_mappings, self.callable_visitor).select(*selectors)


class _TagSelector(object):

    def __init__(self, factory, tag_mappings, callable_visitor, selection=None):
        self.factory = factory
        self.tag_mappings = tag_mappings
        self.callable_visitor = callable_visitor
        self.selection = selection if selection else set()

    def select(self, *selectors):
        for selector in selectors:
            self.selection.union(self.tag_mappings.get(selector))
        return self

    def filter(self, *filters):
        for selector in selectors:
            self.selection.difference(self.tag_mappings.get(selector))
        return self

    def each(self, callable_visitor):
        for selected in self.selection:
            callable_visitor(self.factory(selected))


class DatasourceEngine(object):

    registrations = {}
    instances = {}

    def __init__(self, builder=_ds_builder, processor_factory=_ds_processor_factory):
        self.builder = builder
        self.processor_factory = processor_factory
        self.tag_selector_factory = TagSelectorFactory()

    def register(self, reference, cls, dependencies=None, lookback=0, tags=None):
        self.instances[reference] = None
        self.registrations[reference] = {
            'class': cls,
            'dependencies': dependencies if dependencies else set(),
            'lookback': lookback,
            'tags': tags if tags else set()
        }

    def get(self, reference):
        instance = self._lazyload_datasource(reference)
        dependencies = map(self.get, self.registrations[reference]['dependencies'])
        lookback_period = self.registrations[reference]['class']
        return self.processor_factory(instance, dependencies, lookback_period)

    def select(self, *selectors):
        return self.tag_selector_factory()

    def _lazyload_datasource(self, reference):
        if not self.instances.get(reference):
            if not self.registrations.get(reference):
                raise KeyError()
            self.instances[reference] = self.builder(self.registrations[reference]['class'])
        return self.instances[reference]


class DatasourceEvaluator(object):

    def evaluate(self, reference, symbol, start=None, end=None):
        context = self._create_datasource_context(reference, symbol, start, end)
        result = self._get_datasource(reference).evaluate(context, symbol, start, end)
        return slice_dataframe(result, start, end)


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


def datasource(name, dependencies=[]):
    def wrapper(cls):
        engine.register(name, cls, dependencies)
        return cls
    return wrapper


engine = DatasourceEngine(DatasourceBuilder())

def slice_dataframe(dataframe, start, end):
    if start and end:
        return dataframe[start:end]
    if start:
        return dataframe[start:]
    if end:
        return dataframe[:end]
    return dataframe