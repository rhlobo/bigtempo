import pandas

from instances import data_engine


'''
3 problems to be solved:
========================
- Slice (sync) the start date of the dependencies
- Each datasource must specify its period
- Lookback period should take in account datasource period when calculating dependencies
- Point register should receive which date it is on

Other things to be done:
========================
- Use the point context
- Organize the point implementation
- Extract abstraction that handle context slicing to point context
'''


def point(reference, base_reference, dependencies=None, lookback=1, tags=None):
    def wrapper(cls):

        _point_datasource(reference,
                          cls,
                          base_reference,
                          dependencies,
                          lookback,
                          [] if not tags else tags)

        return cls
    return wrapper


def _point_datasource(reference, cls, base_reference, dependencies, lookback, declared_tags):

    @data_engine.datasource(reference,
                            dependencies=[base_reference] + dependencies,
                            lookback=lookback,
                            tags=['POINT'] + declared_tags)
    class PointDatasource(object):

        def evaluate(self, context, symbol, start, end):
            registor = _PointRegistror()
            point_context_provider = _PointContextProvider(context, base_reference, lookback)

            for point_context in point_context_provider.available_contexts():
                registor.set_context(point_context)
                cls().evaluate(point_context, registor)

            return registor.get()


class _PointRegistror(object):

    def __init__(self):
        self._points = []
        self._current_context = None

    def set_context(self, point_context):
        self._current_context = point_context

    def add(self, value):
        if self._current_context is None:
            raise NotImplementedError

        date = self._current_context.base_index()

        current_values = self._current_context.base_reference_values()
        if value < current_values['low'] or value > current_values['high']:
            raise NotImplementedError

        self._points.append((date, value))

    def get(self):
        if len(self._points) == 0:
            return pandas.DataFrame({'value': {}})

        index, data = zip(*self._points)
        return pandas.DataFrame({'value': data}, index=index)


class _PointContextProvider(object):

    def __init__(self, context, base_reference, lookback):
        self._lookback = lookback
        self._base_reference = base_reference
        self._dependencies = {}
        self._init_dependencies(context.dependencies())

    def _init_dependencies(self, dependencies):
        start_slice_index = self._calculate_start_slice_index(dependencies)
        for key, value in dependencies.items():
            self._dependencies[key] = dependencies[key][start_slice_index:]

    def _calculate_start_slice_index(self, dependencies):
        start_indexes = []
        for value in dependencies.values():
            if len(value) > 0:
                start_indexes.append(value.ix[0].name)
        return max(start_indexes)

    def available_contexts(self):
        df_base = self._dependencies[self._base_reference]

        for i in range(self._lookback + 1, len(df_base)):
            yield _PointContext(self._base_reference, df_base.ix[i].name, self._dependencies, self._lookback)


class _PointContext(object):

    def __init__(self, base_reference, base_index, dependencies, lookback):
        self._lookback = lookback + 1
        self._dependencies = {}
        for key in dependencies.keys():
            self._dependencies[key] = dependencies[key].ix[:base_index][-self._lookback:]
        self._dependencies['base'] = self._dependencies[base_reference]

        self._base_reference = base_reference
        self._end_index = base_index

    def base_index(self):
        return self._end_index

    def base_reference_values(self):
        return self._dependencies['base'].ix[-1]

    def dependencies(self, reference):
        return self._dependencies.get(reference)

    def __getitem__(self, key):
        return self.dependencies(key)
