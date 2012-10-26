#!/usr/bin/python2.7 -tt


import data.providers as providers
from matplotlib import pyplot
from matplotlib.dates import date2num


def plotstockdata(stockdata, stockticker, dates, col):
    pyplot.plot_date(stockdata[0], stockdata[1], '-', xdate=True)
    pyplot.title('%s - %s / %s' % (stockticker, col, dates))
    pyplot.xlabel(dates)
    pyplot.ylabel(col)
    pyplot.savefig('output/%s.png' % stockticker)
    pyplot.show()


if __name__ == '__main__':
    s_symbol = "PETR4"
    d = providers.get().load(s_symbol)

    l_date = sorted(d)
    quotes = []
    dates = []
    for date in l_date:
        i_date = date2num(date)
        dates.append(i_date)
        quotes.append(d[date][4])
        print (i_date, d[date][4])
    data = [dates, quotes]
    plotstockdata(data, s_symbol, "Date", s_symbol)


# TODO Logging
# TODO Remove AbstractProvider ?
# TODO Write tests
