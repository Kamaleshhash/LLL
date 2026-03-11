from django.conf import settings
from django.db import models


class AlertSubscription(models.Model):
    CHANNEL_CHOICES = [('email', 'Email'), ('sms', 'SMS')]

    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    cnr_number = models.CharField(max_length=32)
    channel = models.CharField(max_length=20, choices=CHANNEL_CHOICES, default='email')
    destination = models.CharField(max_length=255)
    active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
