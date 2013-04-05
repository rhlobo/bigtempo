from datetime import timedelta
import providers.base as base
import providers.raw as raw


class PercentualChangeProvider(base.ByProductProvider):

    def __init__(self):
        self.provider = raw.CotahistProvider()

    def load(self, s_symbol, da_start=None, da_end=None):
        da_newStart = (da_start - timedelta(days=1)) if da_start else None
        return self.provider.load(s_symbol, da_newStart, da_end).pct_change()
