from datetime import datetime
from django.contrib import admin
from django.contrib.auth.models import User
from django.contrib.auth.admin import UserAdmin
from rangefilter.filters import DateRangeFilterBuilder
from .filters import StatusFilter, boolean_display
from .models import Feedback, Profile, Child, Appointment, Vaccines, Doctor

# from django.utils.translation import gettext_lazy as _
# from django.contrib.admin.filters import DateFieldListFilter


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
    list_display = [
        "first_name",
        "last_name",
        "date_of_birth",
        "parent__id",
        "parent",
        "gender",
    ]
    raw_id_fields = ["parent"]

    @admin.display(description="Parent ID")
    def parent__id(self, obj):
        return obj.parent.pk


@admin.register(Appointment)
class AppointmentAdmin(admin.ModelAdmin):
    list_display = (
        "id",
        "date_and_time",
        "child",
        "doctor",
        "vaccine",
        "status_display",
    )
    list_display_links = ("id", "date_and_time")
    list_filter = (
        StatusFilter,
        ("date", DateRangeFilterBuilder(title="By Date")),
    )

    def date_and_time_ordering(self, obj):
        return datetime.combine(obj.date, obj.time)

    @admin.display(description="Date and Time", ordering=date_and_time_ordering)
    def date_and_time(self, obj):
        return datetime.combine(obj.date, obj.time).strftime("%d-%b-%Y, %I:%M %p")

    @admin.display(description="Status")
    def status_display(self, obj):
        completed = obj.completed
        cancelled = obj.cancelled

        if cancelled:
            return "Cancelled"
        if completed:
            return "Complete"
        return "Pending"


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
