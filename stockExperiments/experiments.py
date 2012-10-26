#!/usr/bin/python2.7 -tt


import data.providers as providers
from matplotlib import pyplot
from matplotlib.dates import date2num


def main():
    s_symbol = "PETR4"
    plot(loadData(s_symbol), s_symbol, "Date", "Cotation")


def loadData(s_symbol):
    d_data = providers.get().load(s_symbol)
    quotes, dates = [[], []]
    for date in sorted(d_data):
        dates.append(date2num(date))
        quotes.append(d_data[date][4])
    return [dates, quotes]


def plot(ll_data, s_symbol, s_xAxDesc, s_yAxDesc):
    pyplot.plot_date(ll_data[0], ll_data[1], '-', xdate=True)

    pyplot.title('%s - %s / %s' % (s_symbol, s_yAxDesc, s_xAxDesc))
    pyplot.xlabel(s_xAxDesc)
    pyplot.ylabel(s_yAxDesc)
    pyplot.savefig('output/%s.png' % s_symbol)
    pyplot.show()


if __name__ == '__main__':
    main()

# TODO Logging
# TODO Remove AbstractProvider ?
# TODO Write tests
