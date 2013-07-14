# -*- coding: utf-8 -*-


import os
import datetime


def _determine_data_dir():
    data_dir = os.path.abspath('sources/data')
    return data_dir if not 'ipy-notebooks' in data_dir else os.path.abspath('../stockExperiments/sources/data')


START_DATE = datetime.date(2000, 1, 1)
DATA_DIR = _determine_data_dir()
NORMALIZATION_PCT_CHANGE_LIMIT = 0.35
