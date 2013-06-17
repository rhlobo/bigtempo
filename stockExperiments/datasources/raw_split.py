import pandas

import configurations as config

from instances import data_engine


@data_engine.for_each(data_engine.select('RAW_PCT_CHANGE'))
def _datasource_factory(source_reference):

    @data_engine.datasource('SPLITS:%s' % (source_reference),
                            dependencies=[source_reference],
                            tags=['RAW_SPLITS'])
    class RawSplits(object):

        def evaluate(self, context, symbol, start=None, end=None):
            df_pct_change = context.dependencies(source_reference)
            limit = config.NORMALIZATION_PCT_CHANGE_LIMIT

            def _calculateAfter(x):
                return 1 if x >= 0 else (1 / (1 - abs(x))).round(decimals=0)

            def _calculateBefore(x):
                return 1 if x <= 0 else (abs(x) + 1).round(decimals=0)

            df_split_join = (df_pct_change[(abs(df_pct_change['open']) > limit) &
                             (abs(df_pct_change['high']) > limit) &
                             (abs(df_pct_change['low']) > limit) &
                             (abs(df_pct_change['close']) > limit)])

            split_info = pandas.DataFrame(index=df_split_join.index, columns=['factor'])
            if len(df_split_join) != 0:
                df_split_join['average'] = (df_split_join['open'] + df_split_join['high'] + df_split_join['low'] + df_split_join['close']) / 4
                df_split_join['before'] = df_split_join['average'].apply(_calculateBefore)
                df_split_join['after'] = df_split_join['average'].apply(_calculateAfter)
                split_info['factor'] = df_split_join['before'] / df_split_join['after']

            return split_info
