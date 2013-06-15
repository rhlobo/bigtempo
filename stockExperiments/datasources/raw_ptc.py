from instances import data_engine


@data_engine.for_each(data_engine.select('RAW'))
def _create_datasource(source_reference, pct_periods=1):

    @data_engine.datasource('PCT_CHANGE(%i):%s' % (pct_periods, source_reference),
                            dependencies=[source_reference],
                            lookback=pct_periods,
                            tags=['RAW_PCT_CHANGE'])
    class RawPctChange(object):

        def evaluate(self, context, symbol, start=None, end=None):
            return context.dependencies(source_reference).pct_change()
