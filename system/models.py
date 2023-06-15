from django.db import models
from django.conf import settings
from django.contrib.auth.models import User

class Profile(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL,
                                on_delete=models.CASCADE)
    date_of_birth = models.DateField(null=True, blank=True, default=None)
    username = models.CharField(max_length=50, default="")
    phone_number = models.CharField(max_length=20)
    # photo = models.ImageField(upload_to='user/%Y/%m/%d/', blank=True)
    
    
    def __str__(self):
        return f'Profile of {self.user.username}'
    
class Child(models.Model):
    GENDER_CHOICES =(
        ('M', 'Male'),
        ('F', 'Female'),
    )
    
    parent = models.ForeignKey(User, on_delete=models.CASCADE)
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    date_of_birth = models.DateField()
    vaccinations = models.ManyToManyField('Vaccination')
    gender = models.CharField(max_length=1, choices=GENDER_CHOICES, default='M')

    def __str__(self):
        return f'{self.first_name} {self.last_name}'

class Appointment(models.Model):
    child = models.ForeignKey(Child, on_delete=models.CASCADE, related_name='appointments')
    parent = models.ForeignKey(User, on_delete=models.CASCADE)
    date = models.DateField()
    time = models.TimeField()
    doctor = models.ForeignKey('Doctor', on_delete=models.CASCADE)
    status = models.CharField(max_length=100, default="Pending")

    def __str__(self):
         return f'Appointment for {self.child}'

class Vaccination(models.Model):
    name = models.CharField(max_length=100)
    date = models.DateField()
    status = models.CharField(max_length=100)

    def __str__(self):
        return self.name

class Doctor(models.Model):
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    appointments = models.ManyToManyField(Appointment,related_name='doctors', blank=True)
    # vaccination = models.ForeignKey(Vaccination, on_delete=models.CASCADE)

    def __str__(self):
        return f'Dr. {self.first_name} {self.last_name}'
    

# class Parent(models.Model):
#     first_name = models.CharField(max_length=100)
#     last_name = models.CharField(max_length=100)
#     username = models.CharField(max_length=100)
#     password = models.CharField(max_length=100)
#     email = models.EmailField()

#     def __str__(self):
#         return f'{self.first_name} {self.last_name}'
