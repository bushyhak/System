import datetime
import zoneinfo
from django.utils import timezone
from datetime import datetime as dt
from django.core.mail import send_mail
from django.utils.html import strip_tags
from django.conf import settings as django_settings
from django.template.loader import render_to_string

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


def get_age(date_of_birth: datetime.date) -> str:
    """Returns the age in terms of days, weeks, months, and years"""
    today = datetime.date.today()
    age = today - date_of_birth
    years = age.days // 365
    months = (age.days - years * 365) // 30
    weeks = (age.days - years * 365 - months * 30) // 7
    days = age.days - years * 365 - months * 30 - weeks * 7
    age_string = ""
    if age.days == 0:
        age_string = "0 days"
    else:
        if years > 0:
            age_string += f"{years} yr{'s' if years > 1 else ''}"
        if months > 0:
            age_string += (
                f"{', ' if age_string else ''}{months} month{'s' if months > 1 else ''}"
            )
        if weeks > 0:
            age_string += (
                f"{', ' if age_string else ''}{weeks} wk{'s' if weeks > 1 else ''}"
            )
        if days > 0:
            age_string += (
                f"{', ' if age_string else ''}{days} day{'s' if days > 1 else ''}"
            )
    return age_string


def send_booking_confirmation_email(appointment):
    """Helper function to send an appointment booking confirmation"""
    subject = "Appointment Booking Notification"
    child = appointment.child
    parent = child.parent
    vaccine = appointment.vaccine
    context = {
        "parent_name": parent.first_name or parent.last_name or parent.username,
        "child_name": child.full_name,
        "vaccine_name": vaccine and vaccine.name,
        "date": appointment.date,
        "time": appointment.time,
    }
    html_message = render_to_string("system/appointments/confirm_booking.html", context)
    plain_message = strip_tags(html_message)
    from_email = django_settings.DEFAULT_FROM_EMAIL
    try:
        send_mail(
            subject,
            plain_message,
            from_email,
            recipient_list=[parent.email],
            html_message=html_message,
        )
    except Exception as e:
        print("Failed to send booking confirmation email: ", e)


def vaccine_in_child_appointments(vaccine, child):
    """Check if a vaccine has been previously booked for a child"""
    for appoinment in child.appointments.filter(cancelled=False):
        if vaccine.pk == appoinment.vaccine.pk:
            return True
    return False


def is_numbers(text: str):
    """Check if the given text string is numbers only

    @example is_numbers("10") returns True
    @example is_numbers("10 20") returns True
    @example is_numbers("hi") returns False
    """
    return text.replace(" ", "").isdigit()
