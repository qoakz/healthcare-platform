from rest_framework import serializers
from .models import Notification


class NotificationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Notification
        fields = [
            'id', 'notification_type', 'channel', 'status', 'title', 'message',
            'external_id', 'metadata', 'scheduled_at', 'sent_at', 'read_at',
            'created_at', 'updated_at'
        ]
        read_only_fields = [
            'id', 'external_id', 'sent_at', 'read_at', 'created_at', 'updated_at'
        ]


class NotificationCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Notification
        fields = [
            'user', 'notification_type', 'channel', 'title', 'message',
            'metadata', 'scheduled_at'
        ]
    
    def create(self, validated_data):
        return super().create(validated_data)


class NotificationListSerializer(serializers.ModelSerializer):
    """
    Simplified serializer for notification listing
    """
    class Meta:
        model = Notification
        fields = [
            'id', 'notification_type', 'channel', 'status', 'title', 'message',
            'read_at', 'created_at'
        ]
        read_only_fields = ['id', 'read_at', 'created_at']
