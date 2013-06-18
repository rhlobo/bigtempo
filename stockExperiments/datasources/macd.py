import talib
import pandas

from instances import data_engine


@data_engine.for_synched(data_engine.select('CLOSE'))
def _datasource_factory(source_reference):

    period_profiles = [(12, 26, 9), (5, 35, 5), (12, 26, 3)]

    for profile in period_profiles:
        _generate_for_profile(source_reference, *profile)


def _generate_for_profile(source_reference, fast_period, slow_period, signal_period):

    @data_engine.datasource('MACD(%i,%i,%i):%s' % (fast_period, slow_period, signal_period, source_reference),
                            dependencies=[source_reference],
                            lookback=slow_period*2,
                            tags=['MACD'])
    class MACD(object):

        def evaluate(self, context, symbol, start=None, end=None):
            df_source = context.dependencies(source_reference)
            macd, macdsignal, macdhist = talib.MACD(df_source['value'],
                                                    fastperiod=fast_period,
                                                    slowperiod=slow_period,
                                                    signalperiod=signal_period)
            return pandas.DataFrame({
                "macd": macd,
                "macdsignal": macdsignal,
                "macdhist": macdhist
            }, index=df_source.index).dropna()
