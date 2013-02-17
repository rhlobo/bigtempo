import unittest
from datetime import date, datetime, timedelta
import configurations as config
import util.dateutils as util


class TestWorkingDayRangeFunction(unittest.TestCase):

    def test_should_return_week_working_days(self):
        result = util.working_day_range(date(2012, 12, 9), date(2012, 12, 15))
        assert len(result) is 5

        i = 0
        for day in result:
            assert day == datetime(2012, 12, 10 + i)
            i += 1

    def test_should_return_only_working_days(self):
        result = util.working_day_range(date(2012, 11, 29), date(2012, 12, 3))
        assert len(result) is 3
        assert result[0] == datetime(2012, 11, 29)
        assert result[1] == datetime(2012, 11, 30)
        assert result[2] == datetime(2012, 12, 03)

    def test_should_use_config_start_date_when_argument_is_not_pased(self):
        result = util.working_day_range()
        assert result[0].date() == util.next_working_day(config.START_DATE)

    def test_should_use_today_date_when_argument_is_not_pased(self):
        result = util.working_day_range()
        assert result[-1].date() == util.last_working_day()

    def test_should_use_config_start_date_til_today_when_no_arg_is_pased(self):
        result = util.working_day_range()
        assert result[0].date() == util.next_working_day(config.START_DATE)
        assert result[-1].date() == util.last_working_day()

    def test_return_should_be_list_of_date_instances(self):
        result = util.working_day_range()
        assert isinstance(result[-1], date)


class TestRelativeWorkingDayFunction(unittest.TestCase):

    def test_should_return_negative_relative_day(self):
        assert util.relative_working_day(-20, date(2012, 12, 17)) == date(2012, 11, 19)

    def test_should_return_positive_relative_day(self):
        assert util.relative_working_day(20, date(2012, 12, 17)) == date(2013, 1, 14)

    def test_should_return_date_1_working_day_ago(self):
        dt_today = date.today()
        assert util.relative_working_day(-1) == util.last_working_day(util.last_working_day(dt_today) - timedelta(1))

    def test_should_use_today_if_no_argument_is_given(self):
        assert util.relative_working_day(0) == util.last_working_day(date.today())

    def test_should_return_friday_date_if_weekend_and_0_as_arg(self):
        d = date(2012, 12, 16)
        assert util.relative_working_day(0, d) == util.last_working_day(d)

    def test_should_consider_last_working_day_if_weekend_date_was_given(self):
        assert util.relative_working_day(-2, date(2012, 12, 16)) == date(2012, 12, 12)

    def test_should_consider_last_working_day_if_weekend_date_was_given2(self):
        assert util.relative_working_day(2, date(2012, 12, 15)) == date(2012, 12, 18)

    def test_return_should_be_instance_of_date(self):
        assert isinstance(util.relative_working_day(0), date)


class TestLastWorkingDayFunction(unittest.TestCase):

    def test_should_return_date_if_working_day(self):
        d = date(2012, 12, 07)
        assert util.last_working_day(d) == d

    def test_should_return_friday_date_if_date_is_saturday(self):
        assert util.last_working_day(date(2012, 12, 8)) == date(2012, 12, 7)

    def test_should_return_friday_date_if_date_is_sunday(self):
        assert util.last_working_day(date(2012, 12, 9)) == date(2012, 12, 7)

    def test_should_use_today_if_no_argument_is_given(self):
        d = date.today()
        w = d.weekday()
        assert util.last_working_day() == d if w <= 4 else d - timedelta(w - 4)

    def test_return_should_be_instance_of_date(self):
        assert isinstance(util.last_working_day(), date)


class TestNextWorkingDayFunction(unittest.TestCase):

    def test_should_return_date_if_working_day(self):
        d = date(2012, 12, 07)
        assert util.next_working_day(d) == d

    def test_should_return_monday_date_if_date_is_saturday(self):
        assert util.next_working_day(date(2012, 12, 8)) == date(2012, 12, 10)

    def test_should_return_monday_date_if_date_is_sunday(self):
        assert util.next_working_day(date(2012, 12, 9)) == date(2012, 12, 10)

    def test_should_use_today_if_no_argument_is_given(self):
        d = date.today()
        w = d.weekday()
        assert util.next_working_day() == d if w <= 4 else d + timedelta(7 - w)

    def test_return_should_be_instance_of_date(self):
        assert isinstance(util.next_working_day(), date)


class TestToDate(unittest.TestCase):

    def test_should_return_equivalent_date_object(self):
        result = util.to_date(datetime(2012, 12, 12))
        assert result.year == 2012
        assert result.month == 12
        assert result.day == 12

    def test_return_should_be_instance_of_date(self):
        result = util.to_date(datetime(2012, 12, 12))
        assert isinstance(result, date)


class TestToDatetime(unittest.TestCase):

    def test_should_return_equivalent_datetime_object(self):
        result = util.to_datetime(date(2012, 12, 12))
        assert result.year == 2012
        assert result.month == 12
        assert result.day == 12

    def test_return_should_be_instance_of_datetime(self):
        result = util.to_datetime(date(2012, 12, 12))
        assert isinstance(result, datetime)


class TestDateToTimestamp(unittest.TestCase):

    def test_should_return_int_or_float_value(self):
        result = util.date_to_timestamp(date(2000, 1, 1))
        assert isinstance(result, int) or isinstance(result, float)

    def test_epoch_should_define_initial_timestamp_count(self):
        result = util.date_to_timestamp(date(1970, 1, 1))
        assert result == 10800000

    def test_should_return_correct_millis_for_year_2k(self):
        result = util.date_to_timestamp(date(2000, 1, 1))
        assert result == 946692000000

    def test_should_each_day_add_correct_millis(self):
        result = util.date_to_timestamp(date(2000, 1, 2))
        assert result == 946692000000 + 24 * 3600 * 1000

    def test_should_accept_date_object_as_input(self):
        result = util.date_to_timestamp(date(2000, 1, 1))
        assert result == 946692000000

    def test_should_accept_datetime_object_as_input(self):
        result = util.date_to_timestamp(datetime(2000, 1, 1))
        assert result == 946692000000


class TestTimestampToDate(unittest.TestCase):

    def test_should_return_datetime_object(self):
        result = util.timestamp_to_datetime(0)
        assert isinstance(result, datetime)

    def test_should_equivalent_to_epoch(self):
        result = util.timestamp_to_datetime(10800000)
        assert result == datetime(1970, 1, 1)

    def test_should_return_equivalent_to_year2k(self):
        result = util.timestamp_to_datetime(946692000000)
        assert result == datetime(2000, 1, 1)
