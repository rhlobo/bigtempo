import talib
import pandas
import configurations as config
import util.dateutils as dateutils
import providers.base as base
import providers.raw as raw


class PercentualChangeProvider(base.ByproductProvider):

    def load(self, s_symbol, da_start=None, da_end=None):
        da_newStart = None if not da_start else dateutils.relative_working_day(-1, da_start)
        provider = self.locator.get(raw.CotahistProvider)
        return provider.load(s_symbol, da_newStart, da_end).pct_change()[1:]


class SplitInformationProvider(base.ByproductProvider):

    def load(self, s_symbol, da_start=None, da_end=None):
        #TODO: self.locator.clear(s_symbol)
        df_pct_change = self.locator.get(PercentualChangeProvider).load(s_symbol, da_start, None)
        limit = config.NORMALIZATION_PCT_CHANGE_LIMIT

        def _calculateAfter(x):
            return 1 if x >= 0 else (1 / (1 - abs(x))).round(decimals=0)

        def _calculateBefore(x):
            return 1 if x <= 0 else (abs(x) + 1).round(decimals=0)

        df_split_join = df_pct_change[(abs(df_pct_change['open']) > limit) & (abs(df_pct_change['high']) > limit) & (abs(df_pct_change['low']) > limit) & (abs(df_pct_change['close']) > limit)]

        split_info = pandas.DataFrame(index=df_split_join.index, columns=['factor'])
        if len(df_split_join) != 0:
            df_split_join['average'] = (df_split_join['open'] + df_split_join['high'] + df_split_join['low'] + df_split_join['close']) / 4
            df_split_join['before'] = df_split_join['average'].apply(_calculateBefore)
            df_split_join['after'] = df_split_join['average'].apply(_calculateAfter)
            split_info['factor'] = df_split_join['before'] / df_split_join['after']

        return split_info


class NormalizationFactorProvider(base.ByproductProvider):

    def load(self, s_symbol, da_start=None, da_end=None):
        df_split_info = self.locator.get(SplitInformationProvider).load(s_symbol, da_start, da_end)
        df_normalization = pandas.DataFrame(index=dateutils.working_day_range(da_start, da_end))

        for column in ['open', 'high', 'low', 'close']:
            df_normalization[column] = 1

        for i in range(len(df_split_info)):
            row = df_split_info.ix[i]
            day = dateutils.relative_working_day(-1, row.name)
            df_normalization.update(df_normalization[:day] * row['factor'])
        df_normalization['volume'] = 1 / df_normalization['close']

        return df_normalization


class NormalizedCotationProvider(base.ByproductProvider):

    def load(self, s_symbol, da_start=None, da_end=None):
        df_raw = self.locator.get(raw.CotahistProvider).load(s_symbol, da_start, da_end)
        df_factor = self.locator.get(NormalizationFactorProvider).load(s_symbol, da_start, da_end)
        return (df_raw * df_factor).dropna()


class MACDProvider(base.ByproductProvider):

    column = 'close'
    fast_period = 12
    slow_period = 26
    signal_period = 9
    lookback_period = 40

    def load(self, s_symbol, da_start=None, da_end=None):
        da_newStart = None if not da_start else dateutils.relative_working_day(-self.lookback_period, da_start)
        df_norm = self.locator.get(NormalizedCotationProvider).load(s_symbol, da_newStart, da_end)

        macd, macdsignal, macdhist = talib.MACD(
                                                df_norm[self.column],
                                                fastperiod=self.fast_period,
                                                slowperiod=self.slow_period,
                                                signalperiod=self.signal_period
                                                )
        return pandas.DataFrame(
                                {
                                    "macd": macd,
                                    "macdsignal": macdsignal,
                                    "macdhist": macdhist
                                },
                                df_norm.index
                                )
