from rest_framework import serializers
from .models import RTCRoom, RTCSignal, RTCJoinToken
from appointments.serializers import AppointmentSerializer
from users.serializers import UserSerializer


class RTCRoomSerializer(serializers.ModelSerializer):
    appointment = AppointmentSerializer(read_only=True)
    duration_minutes = serializers.SerializerMethodField()
    
    class Meta:
        model = RTCRoom
        fields = [
            'id', 'appointment', 'room_id', 'status', 'max_participants',
            'recording_enabled', 'created_at', 'started_at', 'ended_at',
            'expires_at', 'duration_minutes'
        ]
        read_only_fields = [
            'id', 'room_id', 'created_at', 'started_at', 'ended_at', 'duration_minutes'
        ]
    
    def get_duration_minutes(self, obj):
        if obj.started_at and obj.ended_at:
            duration = obj.ended_at - obj.started_at
            return int(duration.total_seconds() / 60)
        return None


class RTCRoomCreateSerializer(serializers.ModelSerializer):
    appointment_id = serializers.IntegerField(write_only=True)
    
    class Meta:
        model = RTCRoom
        fields = [
            'appointment_id', 'max_participants', 'recording_enabled', 'expires_at'
        ]
    
    def create(self, validated_data):
        appointment_id = validated_data.pop('appointment_id')
        
        # Get appointment
        from appointments.models import Appointment
        try:
            appointment = Appointment.objects.get(id=appointment_id)
        except Appointment.DoesNotExist:
            raise serializers.ValidationError("Appointment not found")
        
        # Generate unique room ID
        import uuid
        room_id = f"room_{uuid.uuid4().hex[:12]}"
        
        # Create RTC room
        room = RTCRoom.objects.create(
            appointment=appointment,
            room_id=room_id,
            **validated_data
        )
        
        return room


class RTCSignalSerializer(serializers.ModelSerializer):
    sender_name = serializers.CharField(source='sender.get_full_name', read_only=True)
    
    class Meta:
        model = RTCSignal
        fields = [
            'id', 'room', 'sender', 'sender_name', 'signal_type', 'payload', 'created_at'
        ]
        read_only_fields = ['id', 'sender_name', 'created_at']


class RTCSignalCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = RTCSignal
        fields = ['room', 'signal_type', 'payload']
    
    def create(self, validated_data):
        validated_data['sender'] = self.context['request'].user
        return super().create(validated_data)


class RTCJoinTokenSerializer(serializers.ModelSerializer):
    user_name = serializers.CharField(source='user.get_full_name', read_only=True)
    
    class Meta:
        model = RTCJoinToken
        fields = [
            'id', 'room', 'user', 'user_name', 'token', 'expires_at', 'created_at'
        ]
        read_only_fields = ['id', 'user_name', 'token', 'created_at']


class RTCJoinTokenCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = RTCJoinToken
        fields = ['room', 'expires_at']
    
    def create(self, validated_data):
        validated_data['user'] = self.context['request'].user
        
        # Generate JWT token
        import jwt
        from datetime import datetime, timedelta
        from django.conf import settings
        
        payload = {
            'user_id': validated_data['user'].id,
            'room_id': validated_data['room'].room_id,
            'exp': validated_data['expires_at']
        }
        
        token = jwt.encode(payload, settings.SECRET_KEY, algorithm='HS256')
        validated_data['token'] = token
        
        return super().create(validated_data)
