#!/usr/bin/python2.7 -tt
# -*- coding: utf-8 -*-


import os
import argparse

import util.dateutils as dateutils
from datasources import *
from instances import data_engine


def process(reference, symbol, start, end, output_path):
    print 'Reference: %s' % reference
    print 'Symbol: %s' % symbol

    result = data_engine.get(reference).process(symbol, start, end)

    if len(result) is 0:
        print 'No data found.'

    filename = '%s(%s)[%s:%s].csv' % (reference,
                                      symbol,
                                      dateutils.datetime_to_string(result.ix[0].name),
                                      dateutils.datetime_to_string(result.ix[-1].name))

    file_path = os.path.join(output_path, filename)

    print 'Start: %s' % start
    print 'End: %s' % end
    print 'Saving results to "%s"' % file_path

    result.to_csv(file_path)


if __name__ == '__main__':
    def _map_process_args(args):
        output_path = args.output_path if args.output_path else os.getcwd()

        symbol = args.symbol
        start = dateutils.string_to_datetime(args.start)
        end = dateutils.string_to_datetime(args.end)

        for reference in args.reference:
            process(reference, symbol, start, end, output_path)

    parser = argparse.ArgumentParser(description='StockExperiments command line interface.')
    subparsers = parser.add_subparsers(dest='subparser', help='Available operations')

    process_parser = subparsers.add_parser('process', help='Process datasources exposing its results')
    process_parser.add_argument('-o', '--output', help='Output directory path', default=None, dest='output_path')
    process_parser.add_argument('-s', '--start', help='Processment start date', default=None, dest='start')
    process_parser.add_argument('-e', '--end', help='Processment end date', default=None, dest='end')
    process_parser.add_argument('symbol', help='Symbol to be processed')
    process_parser.add_argument('reference', help='Processment reference(s)', nargs='+', type=str)
    process_parser.set_defaults(func=_map_process_args)

    args = parser.parse_args()
    args.func(args)
