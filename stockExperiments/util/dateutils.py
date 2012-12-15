import pandas
import datetime
import configurations as config


def working_day_range(start_date=config.START_DATE, end_date=None):
    if not end_date:
        end_date = last_working_day()
    return pandas.bdate_range(start_date, end_date, normalize=True)


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
