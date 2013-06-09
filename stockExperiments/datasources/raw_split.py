from instances import data_engine


def _create_datasource(source_reference):
    reference = 'SPLITS:%s' % (source_reference)

    @data_engine.datasource(reference,
                            dependencies=[source_reference],
                            tags=['RAW_SPLITS'])
    class RawSplits(object):
        def evaluate(self, context, symbol, start=None, end=None):
            return context.dependencies(source_reference).pct_change()


for ds_ref in data_engine.select('RAW_PCT_CHANGE'):
    _create_datasource(ds_ref, 1)
