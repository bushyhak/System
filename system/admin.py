from django.contrib import admin
from .models import Feedback, Profile, Child, Appointment, Vaccines, Doctor


@admin.register(Profile)
class ProfileAdmin(admin.ModelAdmin):
    list_display = ["user", "date_of_birth", "phone_number"]
    raw_id_fields = ["user"]


@admin.register(Child)
class ChildAdmin(admin.ModelAdmin):
    list_display = ["first_name", "last_name", "date_of_birth", "parent", "gender"]
    raw_id_fields = ["parent"]


@admin.register(Appointment)
class AppointmentAdmin(admin.ModelAdmin):
    list_display = ("child", "date", "time", "doctor", "vaccine")
    raw_id_fields = ["child"]


@admin.register(Vaccines)
class VaccinesAdmin(admin.ModelAdmin):
    list_display = ("name", "weeks_maximum_age", "weeks_minimum_age")


@admin.register(Doctor)
class DoctorAdmin(admin.ModelAdmin):
    list_display = ("first_name", "last_name", "license_no")


admin.site.register(Feedback)
