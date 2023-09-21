from rest_framework import serializers

from .models import NotificationPreferences

class NotificationPreferencesSerializer(serializers.ModelSerializer):
    class Meta:
        model = NotificationPreferences
        exclude = ['id', 'user_id']