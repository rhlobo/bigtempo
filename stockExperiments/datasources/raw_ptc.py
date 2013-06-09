from instances import data_engine


def _create_datasource(source_reference, pct_periods):
    reference = 'PCT_CHANGE(%i):%s' % (pct_periods, source_reference)

    @data_engine.datasource(reference,
                            dependencies=[source_reference],
                            lookback=pct_periods,
                            tags=['RAW_PCT_CHANGE'])
    class RawPctChange(object):
        def evaluate(self, context, symbol, start=None, end=None):
            return context.dependencies(source_reference).pct_change()


for ds_ref in data_engine.select('RAW'):
    _create_datasource(ds_ref, 1)
