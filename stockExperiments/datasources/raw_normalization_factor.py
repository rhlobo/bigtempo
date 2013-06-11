import pandas

import util.dateutils as dateutils

from instances import data_engine


@data_engine.for_each(data_engine.select('RAW_SPLITS'))
def _create_datasource(source_reference):

    @data_engine.datasource('NORMALIZATION_FACTOR:%s' % (source_reference),
                            dependencies=[source_reference],
                            tags=['RAW_NORMALIZATION_FACTOR'])
    class RawNormalizationFactor(object):
        def evaluate(self, context, symbol, start=None, end=None):
            df_split = context.dependencies(source_reference)
            df_normalization = pandas.DataFrame(index=dateutils.working_day_range(start, end))

            for column in ['open', 'high', 'low', 'close']:
                df_normalization[column] = 1

            for i in range(len(df_split)):
                row = df_split.ix[i]
                day = dateutils.relative_working_day(-1, row.name)
                df_normalization.update(df_normalization[:day] * row['factor'])
            df_normalization['volume'] = 1 / df_normalization['close']

            return df_normalization
