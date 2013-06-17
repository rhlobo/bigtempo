import pandas

import util.dateutils as dateutils
from instances import data_engine


@data_engine.for_synched(data_engine.select('NORMALIZED'))
def _datasource_factory(source_reference):

    @data_engine.datasource('WEEKLY:%s' % (source_reference),
                            dependencies=[source_reference],
                            lookback=6,
                            tags=['WEEKLY'])
    class Weekly(object):

        def evaluate(self, context, symbol, start=None, end=None):
            df_norm = context.dependencies(source_reference)
            df_index = dateutils.week_range(start, end)

            result = pandas.DataFrame(columns=df_norm.columns, index=df_index)

            result['open'] = df_norm['open'].resample('W-FRI', how='first')
            result['high'] = df_norm['high'].resample('W-FRI', how='max')
            result['low'] = df_norm['low'].resample('W-FRI', how='min')
            result['close'] = df_norm['close'].resample('W-FRI', how='last')
            result['volume'] = df_norm['volume'].resample('W-FRI', how='sum')

            return result.dropna()
