from rest_framework import serializers

from .models import AlertSubscription


class AlertSubscriptionSerializer(serializers.ModelSerializer):
    class Meta:
        model = AlertSubscription
        fields = ['id', 'cnr_number', 'channel', 'destination', 'active', 'created_at']
