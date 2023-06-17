from time import localtime
from django.contrib import admin
from django.contrib.admin.models import LogEntry
from django.utils.html import format_html
admin.site.register(LogEntry)
from django.utils import timezone
from django.utils.formats import localize

from .models import Profile, Child, Appointment, Vaccines, Doctor


@admin.register(Profile)
class ProfileAdmin(admin.ModelAdmin):
    list_display = ['user', 'date_of_birth','username','phone_number']
    raw_id_fields = ['user']

@admin.register(Child)
class ChildAdmin(admin.ModelAdmin):
    list_display = ['first_name', 'last_name', 'date_of_birth', 'parent']
    raw_id_fields = ['parent']

@admin.register(Appointment)
class AppointmentAdmin(admin.ModelAdmin):
    list_display = ('child', 'parent', 'date', 'time', 'doctor', 'status')
    raw_id_fields = ('child', 'parent', 'doctor')

@admin.register(Vaccines)
class VaccinesAdmin(admin.ModelAdmin):
    list_display = ('name','maximum_age','minimum_age')

@admin.register(Doctor)
class DoctorAdmin(admin.ModelAdmin):
    list_display = ('first_name', 'last_name')





class CustomLogEntry(LogEntry):
    class Meta:
        proxy = True

    def __str__(self):
        if self.change_message == 'Appointment rescheduled by user':
            appointment = Appointment.objects.get(id=self.object_id)
            child_id = appointment.child.id
            vaccine = appointment.vaccines
            return f"Appointment rescheduled by {self.user} to {appointment.date} {appointment.time} for Child ID: {child_id}, Vaccine: {vaccine}"
        else:
            return super().__str__()

class CustomLogEntryAdmin(admin.ModelAdmin):
    list_display = ['action_time', 'user', 'content_type', 'get_appointment_details', 'change_message']
    list_filter = ['action_time', 'user', 'content_type']
    search_fields = ['user__username', 'change_message']

    def get_appointment_details(self, obj):
        if obj.change_message == 'Appointment rescheduled by user':
            appointment = Appointment.objects.get(id=obj.object_id)
            child_id = appointment.child.id
            initial_vaccine = appointment.vaccines
            scheduled_time = appointment.time
            scheduled_date = appointment.date
            rescheduled_time = obj.action_time.time()
            rescheduled_date = obj.action_time.date()
            return format_html(
                "Child ID: {}, Initial Vaccine: {}, Scheduled Time: {} on {}, Rescheduled Time: {} on {}",
                child_id, initial_vaccine, scheduled_time, scheduled_date, rescheduled_time, rescheduled_date
            )
        return ''

    get_appointment_details.short_description = 'Appointment Details'
  

admin.site.unregister(LogEntry)
admin.site.register(CustomLogEntry, CustomLogEntryAdmin)

