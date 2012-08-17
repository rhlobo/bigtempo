#!/usr/bin/python
# Filename: bovespaparser.py


TIPREG, DATA, CODBDI, CODNEG, TPMERC, NOMRES, ESPECI, PRAZOT, MODREF, PREABE, PREMAX, PREMIN, PREMED, PREULT, PREOFC, PREOFV, TOTNEG, QUATOT, VOLTOT, PREEXE, INDOPC, DATEN, FATCOT, PTOEXE, CODISI, DISMES = [slice(*i) for i in [(0, 2), (2, 10), (10, 12), (12, 24), (24, 27), (27, 39), (39, 49), (49, 52), (52, 56), (56, 69), (69, 82), (82, 95), (95, 108), (108, 121), (121, 134), (134, 147), (147, 152), (152, 170), (170, 188), (188, 201), (201, 202), (202, 210), (210, 217), (217, 230), (230, 242), (242, 245)]]


def parsestocksdata(data):
    values = []

    for line in data:
        if line[TIPREG] == '00' or line[TPMERC] != '010':
            continue
        if line[TIPREG] == '99':
            break

        date = line[DATA]
        code = line[CODNEG].rstrip()
        popen = float(line[PREABE]) / 100
        pmax = float(line[PREMAX]) / 100
        pmin = float(line[PREMIN]) / 100
        pclose = float(line[PREULT]) / 100
        volume = int(line[VOLTOT])

        values.append([code, date, popen, pmin, pmax, pclose, volume])

    return values


def parsestocksfile(filename):
    with open(filename) as f:
        return parsedata(f)


def parsedata(data, opts=[DATA, CODNEG, PREABE, PREMAX, PREMIN, PREULT, VOLTOT]):
    return [[line[opt] for opt in opts] for line in data if line[TIPREG] == '01']


def parsefile(filename, opts=[DATA, CODNEG, PREABE, PREMAX, PREMIN, PREULT, VOLTOT]):
    with open(filename) as f:
        return parsedata(f, opts)

version = '0.1a'
