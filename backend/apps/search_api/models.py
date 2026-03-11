from django.conf import settings
from django.db import models


class SearchLog(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, null=True, blank=True, on_delete=models.SET_NULL)
    state = models.CharField(max_length=100)
    district = models.CharField(max_length=100)
    village_name = models.CharField(max_length=150)
    survey_number = models.CharField(max_length=50)
    filters = models.JSONField(default=dict, blank=True)
    result_count = models.IntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)


class BulkSearchJob(models.Model):
    STATUS_CHOICES = [('queued', 'Queued'), ('completed', 'Completed')]

    requested_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    payload = models.JSONField(default=dict)
    output = models.JSONField(default=dict, blank=True)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='queued')
    created_at = models.DateTimeField(auto_now_add=True)
