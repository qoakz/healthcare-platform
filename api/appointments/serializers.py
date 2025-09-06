from rest_framework import serializers
from .models import Appointment, ScheduleSlot, AppointmentReminder, AppointmentReschedule
from users.serializers import UserSerializer
from doctors.serializers import DoctorSerializer


class ScheduleSlotSerializer(serializers.ModelSerializer):
    doctor_name = serializers.CharField(source='doctor.full_name', read_only=True)
    
    class Meta:
        model = ScheduleSlot
        fields = [
            'id', 'doctor', 'doctor_name', 'start_time', 'end_time', 'status',
            'duration_minutes', 'notes', 'is_available'
        ]
        read_only_fields = ['id', 'doctor_name', 'is_available']


class AppointmentSerializer(serializers.ModelSerializer):
    patient = UserSerializer(read_only=True)
    doctor = DoctorSerializer(read_only=True)
    slot = ScheduleSlotSerializer(read_only=True)
    duration_minutes = serializers.ReadOnlyField()
    is_upcoming = serializers.ReadOnlyField()
    can_be_cancelled = serializers.ReadOnlyField()
    can_be_rescheduled = serializers.ReadOnlyField()
    
    class Meta:
        model = Appointment
        fields = [
            'id', 'patient', 'doctor', 'slot', 'appointment_type', 'status',
            'reason', 'symptoms', 'medical_history', 'video_room_id',
            'consultation_fee', 'payment_status', 'scheduled_at', 'started_at',
            'ended_at', 'doctor_notes', 'patient_feedback', 'requires_follow_up',
            'follow_up_date', 'duration_minutes', 'is_upcoming', 'can_be_cancelled',
            'can_be_rescheduled', 'created_at'
        ]
        read_only_fields = [
            'id', 'patient', 'doctor', 'slot', 'video_room_id', 'consultation_fee',
            'payment_status', 'started_at', 'ended_at', 'duration_minutes',
            'is_upcoming', 'can_be_cancelled', 'can_be_rescheduled', 'created_at'
        ]


class AppointmentCreateSerializer(serializers.ModelSerializer):
    slot_id = serializers.IntegerField(write_only=True)
    
    class Meta:
        model = Appointment
        fields = [
            'slot_id', 'appointment_type', 'reason', 'symptoms', 'medical_history'
        ]
    
    def create(self, validated_data):
        slot_id = validated_data.pop('slot_id')
        patient = self.context['request'].user
        
        try:
            slot = ScheduleSlot.objects.get(id=slot_id, status='open')
        except ScheduleSlot.DoesNotExist:
            raise serializers.ValidationError("Selected slot is not available")
        
        # Create appointment
        appointment = Appointment.objects.create(
            patient=patient,
            doctor=slot.doctor,
            slot=slot,
            consultation_fee=slot.doctor.consultation_fee,
            scheduled_at=slot.start_time,
            **validated_data
        )
        
        # Mark slot as booked
        slot.status = 'booked'
        slot.save()
        
        return appointment


class AppointmentUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Appointment
        fields = ['status', 'doctor_notes', 'patient_feedback', 'requires_follow_up', 'follow_up_date']
    
    def update(self, instance, validated_data):
        # Only allow certain status transitions
        if 'status' in validated_data:
            new_status = validated_data['status']
            if not self._is_valid_status_transition(instance.status, new_status):
                raise serializers.ValidationError(f"Invalid status transition from {instance.status} to {new_status}")
        
        return super().update(instance, validated_data)
    
    def _is_valid_status_transition(self, current_status, new_status):
        valid_transitions = {
            'pending': ['confirmed', 'cancelled'],
            'confirmed': ['in_progress', 'cancelled', 'no_show'],
            'in_progress': ['completed', 'cancelled'],
            'completed': ['refunded'],
            'cancelled': ['refunded'],
            'no_show': ['refunded'],
        }
        return new_status in valid_transitions.get(current_status, [])


class AppointmentRescheduleSerializer(serializers.ModelSerializer):
    new_slot_id = serializers.IntegerField(write_only=True)
    
    class Meta:
        model = AppointmentReschedule
        fields = ['new_slot_id', 'reason']
    
    def create(self, validated_data):
        appointment = self.context['appointment']
        new_slot_id = validated_data.pop('new_slot_id')
        requested_by = self.context['request'].user
        
        try:
            new_slot = ScheduleSlot.objects.get(id=new_slot_id, status='open')
        except ScheduleSlot.DoesNotExist:
            raise serializers.ValidationError("Selected slot is not available")
        
        # Create reschedule record
        reschedule = AppointmentReschedule.objects.create(
            appointment=appointment,
            old_slot=appointment.slot,
            new_slot=new_slot,
            requested_by=requested_by,
            **validated_data
        )
        
        # Update appointment
        old_slot = appointment.slot
        appointment.slot = new_slot
        appointment.scheduled_at = new_slot.start_time
        appointment.save()
        
        # Update slot statuses
        old_slot.status = 'open'
        old_slot.save()
        new_slot.status = 'booked'
        new_slot.save()
        
        return reschedule


class AppointmentReminderSerializer(serializers.ModelSerializer):
    class Meta:
        model = AppointmentReminder
        fields = [
            'id', 'reminder_type', 'channel', 'sent_at', 'delivery_status',
            'message_content', 'created_at'
        ]
        read_only_fields = ['id', 'sent_at', 'delivery_status', 'created_at']


class AppointmentListSerializer(serializers.ModelSerializer):
    """
    Simplified serializer for appointment listing
    """
    doctor_name = serializers.CharField(source='doctor.full_name', read_only=True)
    patient_name = serializers.CharField(source='patient.get_full_name', read_only=True)
    
    class Meta:
        model = Appointment
        fields = [
            'id', 'doctor_name', 'patient_name', 'appointment_type', 'status',
            'scheduled_at', 'consultation_fee', 'payment_status', 'is_upcoming'
        ]
