#!/usr/bin/python
# Filename: bovespaparser.py


def parse(fileName="../files/COTAHIST_A2011.TXT"):
    values = []
    with open(fileName) as f:

        for line in f:
            treg = line[0:2]
            if treg == '00' or treg == '99' or line[24:27] == '010':
                continue

            date = line[2:10]
            code = line[12:24].rstrip()
            popen = float(line[56:69]) / 100
            pmax = float(line[69:82]) / 100
            pmin = float(line[82:95]) / 100
            pclose = float(line[108:121]) / 100

            values.append([code, date, popen, pmin, pmax, pclose])
    return values

version = '0.1'
