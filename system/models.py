from django.db import models
from django.contrib.auth.models import User
from datetime import date, datetime, timedelta


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

    def __str__(self):
        return f"{self.first_name} {self.last_name}"

    @property
    def administered_vaccines(self):
        vaccines = []
        for appointment in Appointment.objects.filter(child=self):
            vaccines.append(appointment.vaccine)
        return vaccines

    @property
    def vaccines(self):
        return self.administered_vaccines

    @property
    def age_in_weeks(self):
        """Returns the age in weeks as an integer"""
        today = date.today()
        days = (today - self.date_of_birth).days
        weeks = days // 7
        return weeks

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
        return self.get_age(self.date_of_birth)

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
        return f"Appointment for {self.child}"

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
