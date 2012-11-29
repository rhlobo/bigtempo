#!/usr/bin/python -tt

import sys
import pstats


def printStats(filename):
    p = pstats.Stats(filename)
    p.strip_dirs()
    p.sort_stats('cumulative').print_stats(20)
    p.sort_stats('time').print_stats(20)


def main():
    argcount = len(sys.argv)
    if argcount != 2:
        print 'usage: ./displayprofilestats.py file'
        sys.exit(1)

    filename = sys.argv[1]
    printStats(filename)


if __name__ == '__main__':
    main()
