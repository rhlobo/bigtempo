from providers.base import *
from providers.raw import *


def get():
    c_dataMapFactory = SymbolMapFactory()
    return (Provider(CachedProvider(c_dataMapFactory.get()),
                         CotahistProvider(c_dataMapFactory.get())))
