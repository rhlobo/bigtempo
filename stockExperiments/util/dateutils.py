import pandas
import datetime
import time
import configurations as config


def working_day_range(start_date=None, end_date=None):
    da_start = start_date if start_date else config.START_DATE
    da_end = end_date if end_date else last_working_day()
    return pandas.bdate_range(da_start, da_end, normalize=True)


def week_range(start_date=None, end_date=None):
    da_start = start_date if start_date else config.START_DATE
    da_end = end_date if end_date else last_working_day()
    return pandas.bdate_range(da_start, da_end, normalize=True, freq='W-FRI')


def relative_working_day(days, date=None):
    wday = last_working_day() if not date else last_working_day(date)
    return to_date(to_datetime(wday) + days * pandas.tseries.offsets.BDay())


def last_working_day(date=None):
    if not date:
        date = datetime.date.today()
    wday = date.weekday()
    return date if wday <= 4 else date - datetime.timedelta(wday - 4)


def next_working_day(date=None):
    if not date:
        date = datetime.date.today()
    wday = date.weekday()
    return date if wday <= 4 else date + datetime.timedelta(7 - wday)


def to_date(date_time):
    return date_time.date()


def to_datetime(date):
    return datetime.datetime(date.year, date.month, date.day)


def date_to_timestamp(date):
    return time.mktime(date.timetuple()) * 1000


def timestamp_to_datetime(millis):
    return datetime.datetime.fromtimestamp(millis // 1000)
