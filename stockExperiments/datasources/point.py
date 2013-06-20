import pandas

from instances import data_engine


# TODO: Point register should receive price as input
# for new point, date should be recevered from
# somewhere else for security. Price should be
# verifyed if compatible with date's price range.


def point(self, reference, dependencies=None, lookback=0, tags=None):
    def wrapper(cls):

        @data_engine.for_synched(data_engine.select('NORMALIZED'))
        def _point_datasource_factory(normalization_reference):
            _point_datasource(reference,
                              cls,
                              normalization_reference,
                              dependencies,
                              lookback,
                              tags)

        return cls
    return wrapper


def _point_datasource(reference, cls, normalization_reference, dependencies, lookback, declared_tags):

    @data_engine.datasource('POINT_%s:%s' % (reference, normalization_reference),
                            dependencies=[normalization_reference] + dependencies,
                            lookback=lookback,
                            tags=['POINT'] + declared_tags)
    class PointDatasource(object):

        def evaluate(self, context, symbol, start, end):
            registor = _PointRegistror()
            df_source = context.dependencies(normalization_reference)

            for i in range(lookback + 1, len(df_source)):
                sub_context = {}
                dependencies = context.dependencies()
                for key in dependencies.keys():
                    sub_context[key] = dependencies[key].ix[i - lookback - 1: i]
                cls().evaluate(registor, sub_context)

            return registor.get()


class _PointRegistror(object):

    def __init__(self):
        self.points = []

    def add(self, date, value):
        self.points.append((date, value))

    def get(self):
        index, data = zip(*self.points)
        return pandas.DataFrame({'value': data}, index=index)
