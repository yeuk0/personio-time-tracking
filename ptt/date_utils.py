import calendar

from datetime import datetime


def get_today_date():
    return datetime.today()


def get_days_range_from_date_month(date):
    return range(calendar.monthrange(date.year, date.month)[1])


def str_to_date(date_str, date_format='%Y-%m-%d'):
    return datetime.strptime(date_str, date_format)


def is_valid_day(date_str):
    try:
        return str_to_date(date_str).weekday() < 5
    except ValueError:
        return False


def is_friday(date_str):
    return str_to_date(date_str).weekday() == 4
