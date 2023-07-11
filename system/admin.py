from datetime import datetime
from django.contrib import admin
from django.utils.html import format_html
from django.contrib.auth.models import User
from django.templatetags.static import static
from django.contrib.auth.admin import UserAdmin
from django.contrib.admin.filters import BooleanFieldListFilter
from .models import Feedback, Profile, Child, Appointment, Vaccines, Doctor

# from django.utils.translation import gettext_lazy as _
# from django.contrib.admin.filters import DateFieldListFilter


def boolean_display(field_value: bool, options=("True", "False")):
    """Return HTML code with a True/False text and
    success/error icon based a boolean field value"""
    if field_value:
        icon_url = static("admin/img/icon-yes.svg")
        return format_html(f'{options[0]} <img src="{icon_url}" alt="{options[0]}">')
    else:
        icon_url = static("admin/img/icon-no.svg")
        return format_html(f'{options[1]} <img src="{icon_url}" alt="{options[1]}">')


admin.site.unregister(User)


@admin.register(User)
class MyUserAdmin(UserAdmin):
    list_display = ("username", "email", "first_name", "last_name", "is_staff_display")

    @admin.display(description="Staff status")
    def is_staff_display(self, obj):
        return boolean_display(obj.is_staff, ("Staff", "Not Staff"))


@admin.register(Profile)
class ProfileAdmin(admin.ModelAdmin):
    list_display = ["user", "date_of_birth", "phone_number"]
    raw_id_fields = ["user"]


@admin.register(Child)
class ChildAdmin(admin.ModelAdmin):
    list_display = ["first_name", "last_name", "date_of_birth", "parent", "gender"]
    raw_id_fields = ["parent"]


# @admin.register(Appointment)
# class AppointmentAdmin(admin.ModelAdmin):
#     list_display = (
#         "id",
#         "date_and_time",
#         "child",
#         "doctor",
#         "vaccine",
#         "completed_display",
#         "cancelled_display",
#     )
#     list_display_links = ("id", "date_and_time")
#     list_filter = (
#         ("completed", BooleanFieldListFilter),
#         ("cancelled", BooleanFieldListFilter),
#         ("date_and_time", DateFieldListFilter),
#     )

#     def date_and_time_ordering(self, obj):
#         return datetime.combine(obj.date, obj.time)

#     @admin.display(description="Date and Time", ordering=date_and_time_ordering)
#     def date_and_time(self, obj):
#         return datetime.combine(obj.date, obj.time).strftime("%d-%b-%Y, %I:%M %p")

#     @admin.display(description="Completed")
#     def completed_display(self, obj):
#         return boolean_display(obj.completed)

#     @admin.display(description="Cancelled")
#     def cancelled_display(self, obj):
#         return boolean_display(obj.cancelled)


@admin.register(Appointment)
class AppointmentAdmin(admin.ModelAdmin):
    list_display = (
        "id",
        "date_and_time",
        "child",
        "doctor",
        "vaccine",
        "completed_display",
        "cancelled_display",
    )
    list_display_links = ("id", "date_and_time")
    list_filter = (
        ("completed", BooleanFieldListFilter),
        ("cancelled", BooleanFieldListFilter),
        "date",
    )

    def date_and_time_ordering(self, obj):
        return datetime.combine(obj.date, obj.time)

    @admin.display(description="Date and Time", ordering=date_and_time_ordering)
    def date_and_time(self, obj):
        return datetime.combine(obj.date, obj.time).strftime("%d-%b-%Y, %I:%M %p")

    @admin.display(description="Completed")
    def completed_display(self, obj):
        return boolean_display(obj.completed)

    @admin.display(description="Cancelled")
    def cancelled_display(self, obj):
        return boolean_display(obj.cancelled)


@admin.register(Vaccines)
class VaccinesAdmin(admin.ModelAdmin):
    list_display = ("name", "weeks_minimum_age", "weeks_maximum_age")


@admin.register(Doctor)
class DoctorAdmin(admin.ModelAdmin):
    list_display = ("first_name", "last_name", "license_no")
    list_display_links = ("first_name", "last_name")


@admin.register(Feedback)
class FeedbackAdmin(admin.ModelAdmin):
    list_display = ("id", "title", "parent", "appointment")
    list_display_links = ("id", "title")
