from instances import data_engine


@data_engine.datasource_factory(data_engine.select('RAW_PCT_CHANGE'))
def _create_datasource(source_reference):
    reference = 'SPLITS:%s' % (source_reference)

    @data_engine.datasource(reference,
                            dependencies=[source_reference],
                            tags=['RAW_SPLITS'])
    class RawSplits(object):
        def evaluate(self, context, symbol, start=None, end=None):
            return context.dependencies(source_reference).pct_change()
