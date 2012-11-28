
from providers.base import *
from providers.rawdata import *


def get():
    c_dataMapFactory = SymbolMapFactory()
    return (Provider(CachedProvider(c_dataMapFactory.get()),
                         CotahistProvider(c_dataMapFactory.get())))
