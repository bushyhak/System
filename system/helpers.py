from django.utils import timezone
import datetime
from datetime import datetime as dt
import zoneinfo

# The local timezone
local_tz = zoneinfo.ZoneInfo("Africa/Nairobi")


def get_local_now(utc_now=timezone.now()):
    """Convert the UTC time to local time"""
    return utc_now.astimezone(local_tz)


def combine_date_time(date: datetime.date, time: datetime.time):
    """Combine separate date and time fields into a datetime object"""
    return dt.combine(date, time)


def datetime_less_than_now(datetime: dt):
    """Check if the datetime object provided is less than now"""
    datetime = datetime.replace(second=0, microsecond=0)
    now = dt.now().replace(second=0, microsecond=0)
    if datetime < now:
        return True
    return False


def datetime_equals_now(datetime: dt):
    """Check if the datetime object provided is equal to now"""
    datetime = datetime.replace(second=0, microsecond=0)
    now = dt.now().replace(second=0, microsecond=0)
    if datetime == now:
        return True
    return False


def datetime_greater_than_now(datetime: dt):
    """Check if the datetime object provided is greater than now"""
    datetime = datetime.replace(second=0, microsecond=0)
    now = dt.now().replace(second=0, microsecond=0)
    if datetime > now:
        return True
    return False


def date_less_than_today(date: datetime.date):
    """Check if the given date is less than the date today"""
    if date < datetime.date.today():
        return True
    return False


def date_greater_than_today(date: datetime.date):
    """Check if the given date is greater than the date today"""
    if date > datetime.date.today():
        return True
    return False


def time_less_than_now(time: datetime.time):
    """Check if the given time is less than now"""
    time = time.replace(second=0, microsecond=0)
    now = dt.now().time().replace(second=0, microsecond=0)
    if time < now:
        return True
    return False


def time_greater_than_now(time: datetime.time):
    """Check if the given time is greater than now"""
    time = time.replace(second=0, microsecond=0)
    now = dt.now().time().replace(second=0, microsecond=0)
    if time > now:
        return True
    return False
