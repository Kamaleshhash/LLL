from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    ROLE_CHOICES = [
        ('individual', 'Individual'),
        ('professional', 'Professional'),
        ('administrative', 'Administrative'),
        ('institutional', 'Institutional'),
    ]

    phone = models.CharField(max_length=15, blank=True)
    role = models.CharField(max_length=20, choices=ROLE_CHOICES, default='individual')
    preferred_language = models.CharField(max_length=10, default='en')


class OTPRequest(models.Model):
    email = models.EmailField()
    otp = models.CharField(max_length=6)
    created_at = models.DateTimeField(auto_now_add=True)
    is_used = models.BooleanField(default=False)
