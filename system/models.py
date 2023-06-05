from django.db import models
from django.conf import settings

from django.contrib.auth import get_user_model

User = get_user_model()

class Profile(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL,
                                on_delete=models.CASCADE)
    photo = models.ImageField(upload_to='user/%Y/%m/%d/',
                              blank=True)
    
    def __str__(self):
        return f'Profile of {self.user.username}'

