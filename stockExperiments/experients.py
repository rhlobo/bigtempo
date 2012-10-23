#!/usr/bin/python2.7 -tt


import data.providers as providers
import datetime
from matplotlib import pyplot
from matplotlib.dates import date2num


def plotstockdata(stockdata, stockticker, dates, col):
    pyplot.plot_date(stockdata[0], stockdata[1], '-', xdate=True)
    pyplot.title('%s - %s / %s' % (stockticker, col, dates))
    pyplot.xlabel(dates)
    pyplot.ylabel(col)
    pyplot.savefig('%s.png' % stockticker)
    pyplot.show()


if __name__ == '__main__':
    s_symbol = "PETR4"
    d = providers.get().load(s_symbol)

    ls_date = sorted(d)
    quotes = []
    dates = []
    for s_date in ls_date:
        date = datetime.date(int(s_date[0:4]),int(s_date[4:6]),int(s_date[6:8]))
        print date
        d_date = date2num(date)
        dates.append(d_date)
        quotes.append(d[s_date][4])
        print (d_date, d[s_date][4])
    data = [dates, quotes]
    plotstockdata(data, s_symbol, "Date", s_symbol)


# TODO Logging
# TODO Remove AbstractProvider ?
# TODO Write tests
