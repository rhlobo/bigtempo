#!/usr/bin/env python
#
#  Copyright (c) 2012, Abraham Haskins (abeisgreat@abeisgreat.com)
#  Copyright (c) 2007-2008, Corey Goldberg (corey@goldb.org)
#
#  license: GNU LGPL
#
#  This library is free software; you can redistribute it and/or
#  modify it under the terms of the GNU Lesser General Public
#  License as published by the Free Software Foundation; either
#  version 2.1 of the License, or (at your option) any later version.


import urllib
import datetime


"""
This is the "ystockquote" module.

This module provides a Python API for retrieving stock data from Yahoo Finance.

sample usage:
>>> import ystockquote
>>> print ystockquote.get_price('GOOG')
529.46
"""

yahoo_keys = {
    'price': 'l1',
    'change': 'c1',
    'volume': 'v',
    'average_daily_volume': 'a2',
    'stock_exchange': 'x',
    'market_cap': 'j1',
    'book_value': 'b4',
    'ebitda': 'j4',
    'dividend_per_share': 'd',
    'dividend_yield': 'y',
    'earnings_per_share': 'e',
    '52_week_high': 'k',
    '52_week_low': 'j',
    'price_earnings_ratio': 'r',
    'price_earnings_growth_ratio': 'r5',
    'get_price_sales_ratio': 'p5',
    'price_book_ratio': 'p6',
    'short_ratio': 's7'
}

technical_keys = {
    'moving_average': 'sma',
    'exponential_moving_average': 'ema',
    'money_flow_index': 'mfi',
    'rate_of_change': 'roc',
    'relative_strength_index': 'rfi',
}


def __request(symbol, stat):
    url = 'http://finance.yahoo.com/d/quotes.csv?s=%s&f=%s' % (symbol, stat)
    return urllib.urlopen(url).read().strip().strip('"')


def __build_get(st):
    def __get(sy):
        return __request(sy, st)
    return __get


def __build_get_technical(technical):
    def __get_technical(symbol, points):
        url = "http://chartapi.finance.yahoo.com/instrument/1.0/%s/chartdata;type=%s/csv?period=%i" % (symbol, technical, points)
        csv = urllib.urlopen(url).readlines()
        return float(csv[-1:][0].split(',')[1])
    return __get_technical


def get_all(symbol):
    """
    Get all available quote data for the given ticker symbol.

    Returns a dictionary.
    """
    values = __request(symbol, ''.join(yahoo_keys.values())).split(',')
    data = {}
    for x, key in enumerate(yahoo_keys):
        data[key] = values[x]
    return data


def get_historical_prices(symbol, start_datetime, end_datetime):
    """
    Get the historical prices for a given ticker symbol.
    Date, Open, High, Low, Close, Volume, Adj

    Returns a nested list.
    """
    # Convert our nice Datetimes into Yahoo's date format
    start_date = start_datetime.strftime("%Y%m%d")
    end_date = end_datetime.strftime("%Y%m%d")

    request_data = {
        'a': str(int(start_date[4:6]) - 1),
        'b': start_date[6:8],
        'c': start_date[0:4],
        'd': str(int(end_date[4:6]) - 1),
        'e': end_date[6:8],
        'f': end_date[0:4],
    }

    url = 'http://ichart.yahoo.com/table.csv?s=%s&g=d&ignore=.csv' % symbol
    for key in request_data:
        # Create the URL based on request_data
        url += '&%s=%s' % (key, request_data[key])

    # Load the CSV
    days = urllib.urlopen(url).readlines()
    # Split the CSV sheet
    data = [day[:-2].split(',') for day in days]

    # Type'd Data version of Data
    tdata = []
    # Reverse and loop through our data
    for row in sorted(data[1:]):
        # Convert everything to the right types
        tdata.append([
                     datetime.datetime(
                                       int(row[0][0:4]),
                                       int(row[0][5:7]),
                                       int(row[0][8:10])
                                       ),
                     float(row[1]),
                     float(row[2]),
                     float(row[3]),
                     float(row[4]),
                     int(row[5]),
                     float(row[6])
                     ])

    return tdata


def main():
    for key in yahoo_keys:
        st = yahoo_keys[key]
        # Build new global functions for all the individual symbol attributes
        globals()['get_%s' % key] = __build_get(st)

    for key in technical_keys:
        technical = technical_keys[key]
        # Build new global functions for all the individual symbol attributes
        globals()['get_%s' % key] = __build_get_technical(technical)


main()
