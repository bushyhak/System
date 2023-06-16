from django.contrib import admin

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


    
