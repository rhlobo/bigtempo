from instances import data_engine


@data_engine.for_each(data_engine.select('RAW'),
                      data_engine.select('RAW_NORMALIZATION_FACTOR'),
                      sync_by='RAW')
def _create_datasource(raw_reference, normalization_reference):

    reference = 'NORMALIZATION:(%s, %s)' % (raw_reference, normalization_reference)

    @data_engine.datasource(reference,
                            dependencies=[raw_reference, normalization_reference],
                            tags=['NORMALIZATED'])
    class RawNormalizationFactor(object):
        def evaluate(self, context, symbol, start=None, end=None):
            df_raw = context.dependencies(raw_reference)
            df_factor = context.dependencies(normalization_reference)
            return (df_raw * df_factor).dropna()
