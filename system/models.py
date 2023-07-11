import random
from django.db import models
from django.contrib.auth.models import User
from datetime import date, datetime, time, timedelta

from system.helpers import get_age


VACCINE_STATUS_CHOICES = (
    ("pending", "Pending"),
    ("completed", "Completed"),
)

GENDER_CHOICES = (
    ("M", "Male"),
    ("F", "Female"),
)


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, unique=True)
    date_of_birth = models.DateField(null=True, blank=True, default=None)
    phone_number = models.CharField(max_length=20, null=True, blank=True)

    def __str__(self):
        return f"Profile of {self.user.username}"


class Child(models.Model):
    parent = models.ForeignKey(User, on_delete=models.CASCADE)
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    date_of_birth = models.DateField()
    gender = models.CharField(
        max_length=1, choices=GENDER_CHOICES, default=GENDER_CHOICES[0][0]
    )

    class Meta:
        verbose_name_plural = "Children"

    def __str__(self):
        return f"{self.first_name} {self.last_name}"

    def has_appointment_on(self, date: date, time: time):
        """Check if a child has an appointment on the given date and time"""
        if self.appointments.filter(date=date, time=time, cancelled=False).exists():
            return True
        return False

    @property
    def administered_vaccines(self):
        vaccines = []
        appointments = Appointment.objects.filter(
            child=self, cancelled=False, completed=True
        )
        for appointment in appointments:
            vaccine = appointment.vaccine
            setattr(
                vaccine,
                "datetime",
                datetime.combine(appointment.date, appointment.time),
            )
            vaccines.append(vaccine)
        return vaccines

    @property
    def vaccines(self):
        return self.administered_vaccines

    @property
    def age_in_days(self):
        """Returns the age in days as an integer"""
        today = date.today()
        days = (today - self.date_of_birth).days
        return days

    @property
    def age_in_weeks(self):
        """Returns the age in weeks as an integer"""
        weeks = self.age_in_days // 7
        return weeks

    @property
    def age_in_weeks_or_days(self):
        """Returns the age as a string stating in weeks or days"""
        weeks = self.age_in_weeks
        if weeks > 0:
            suffix = "s" if weeks > 1 else ""
            return "%d week%s old" % (weeks, suffix)
        else:
            days = self.age_in_days
            suffix = "s" if days > 1 else ""
            return "%d day%s old" % (days, suffix)

    @property
    def age_in_months(self):
        """Returns the age in months as an integer"""
        today = date.today()
        months = (today.year - self.date_of_birth.year) * 12 + (
            today.month - self.date_of_birth.month
        )
        if today.day < self.date_of_birth.day:
            months -= 1
        return months

    @staticmethod
    def get_age(date_of_birth: date):
        """Returns the age in terms of days, weeks, months, and years"""
        today = date.today()
        age = (
            today.year
            - date_of_birth.year
            - ((today.month, today.day) < (date_of_birth.month, date_of_birth.day))
        )
        if today.month == date_of_birth.month:
            if today.day < date_of_birth.day:
                age -= 1
        elif today.month < date_of_birth.month:
            age -= 1
        months = (today.month - date_of_birth.month) % 12
        days = (today - date_of_birth.replace(year=today.year)).days
        weeks = days // 7
        days %= 7
        age_string = ""
        if age > 0:
            age_string += f"{age} yr{'s' if age > 1 else ''}, "
        if months > 0:
            age_string += f"{months} month{'s' if months > 1 else ''}, "
        if weeks > 0:
            age_string += f"{weeks} wk{'s' if weeks > 1 else ''}, "
        if days > 0:
            age_string += f"{days} day{'s' if days > 1 else ''}"
        else:
            age_string += "0 days"
        return age_string.strip(", ")

    @property
    def age(self):
        return get_age(self.date_of_birth)

    @property
    def full_name(self):
        return "%s %s" % (self.first_name, self.last_name)


class Appointment(models.Model):
    child = models.ForeignKey(
        Child, on_delete=models.SET_NULL, related_name="appointments", null=True
    )
    date = models.DateField()
    time = models.TimeField()
    doctor = models.ForeignKey(
        "Doctor", related_name="appointments", on_delete=models.SET_NULL, null=True
    )
    vaccine = models.ForeignKey(
        "Vaccines", related_name="appointments", on_delete=models.SET_NULL, null=True
    )
    completed = models.BooleanField(default=False)
    cancelled = models.BooleanField(default=False)

    def __str__(self):
        if self.child and self.vaccine:
            return "%d) %s -> %s" % (self.pk, self.child.full_name, self.vaccine.name)
        return "%d" % (self.pk)

    def set_complete(self):
        """Set an appointment to completed and free the doctor handling it"""
        self.completed = True
        self.doctor.available = True
        self.save()
        self.doctor.save()

    def check_complete(self):
        """Check if an appointment is complete and set it to completed if so,
        then free the doctor handling the appointment"""
        if self.completed:
            return True
        else:
            # appointment start date and time
            start = datetime.combine(self.date, self.time)
            # appointment stop date and time
            stop = start + timedelta(minutes=45)
            if stop < datetime.now():
                self.set_complete()
                return True
            else:
                return False


class Vaccines(models.Model):
    name = models.CharField(max_length=50)
    weeks_minimum_age = models.IntegerField(null=True, blank=True)
    weeks_maximum_age = models.IntegerField(null=True, blank=True)

    class Meta:
        verbose_name_plural = "Vaccines"

    def __str__(self):
        return "%s" % self.name


class Doctor(models.Model):
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    license_no = models.CharField(max_length=10)
    available = models.BooleanField(default=True)

    def __str__(self):
        return f"Dr. {self.first_name} {self.last_name}"

    @property
    def full_name(self):
        return "%s %s" % (self.first_name, self.last_name)

    def is_available_on(self, date: date, time: time):
        """Check if, at the given date and time, the Doctor has an appointment"""
        if self.appointments.filter(date=date, time=time).exists():
            return False  # not available
        return True

    @staticmethod
    def get_available_doctor(date: date, time: time):
        """From the Doctors in the system, select one who is free
        on the given date and time
        """
        doctors = Doctor.objects.filter()  # TODO: Maybe add available=True filter later
        doctors = [doctor for doctor in doctors if doctor.is_available_on(date, time)]
        if len(doctors) > 0:
            return random.choice(doctors)
        return None


class Feedback(models.Model):
    title = models.TextField(
        max_length=500, null=False, blank=False, verbose_name="Feedback"
    )
    parent = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=False)
    appointment = models.ForeignKey(Appointment, on_delete=models.CASCADE)

    def __str__(self):
        return "%s" % self.title
