from ipyghstocks.chart import *
from ipyghstocks.options import *


def candlestick(df_quote, s_name=''):
    return plot(Options(s_name).add(Axis('')).add(Series(s_name, df_quote)))
