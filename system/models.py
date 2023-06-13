from django.db import models
from django.conf import settings



class Profile(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL,
                                on_delete=models.CASCADE)
    date_of_birth = models.DateField(null=True, blank=True, default=None)
    username = models.CharField(max_length=50, default="")
    phone_number = models.CharField(max_length=20,blank=False)
    photo = models.ImageField(upload_to='user/%Y/%m/%d/',
                              blank=True)
    
    def __str__(self):
        return f'Profile of {self.user.username}'

