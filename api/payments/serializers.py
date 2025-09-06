from rest_framework import serializers
from .models import PaymentTransaction, Refund, DoctorPayout
from appointments.serializers import AppointmentSerializer
from users.serializers import UserSerializer
from doctors.serializers import DoctorSerializer


class PaymentTransactionSerializer(serializers.ModelSerializer):
    patient_name = serializers.CharField(source='patient.get_full_name', read_only=True)
    appointment = AppointmentSerializer(read_only=True)
    
    class Meta:
        model = PaymentTransaction
        fields = [
            'id', 'provider', 'amount', 'currency', 'status', 'external_id',
            'client_secret', 'appointment', 'patient', 'patient_name', 'description',
            'metadata', 'created_at', 'updated_at', 'completed_at'
        ]
        read_only_fields = [
            'id', 'patient_name', 'external_id', 'client_secret', 'created_at',
            'updated_at', 'completed_at'
        ]


class PaymentTransactionCreateSerializer(serializers.ModelSerializer):
    appointment_id = serializers.IntegerField(write_only=True)
    
    class Meta:
        model = PaymentTransaction
        fields = [
            'appointment_id', 'provider', 'amount', 'currency', 'description'
        ]
    
    def create(self, validated_data):
        appointment_id = validated_data.pop('appointment_id')
        patient = self.context['request'].user
        
        # Get appointment
        from appointments.models import Appointment
        try:
            appointment = Appointment.objects.get(id=appointment_id, patient=patient)
        except Appointment.DoesNotExist:
            raise serializers.ValidationError("Appointment not found")
        
        # Create payment transaction
        payment = PaymentTransaction.objects.create(
            appointment=appointment,
            patient=patient,
            **validated_data
        )
        
        return payment


class RefundSerializer(serializers.ModelSerializer):
    payment = PaymentTransactionSerializer(read_only=True)
    processed_by_name = serializers.CharField(source='processed_by.get_full_name', read_only=True)
    
    class Meta:
        model = Refund
        fields = [
            'id', 'payment', 'amount', 'reason', 'status', 'external_refund_id',
            'processed_by_name', 'created_at', 'updated_at'
        ]
        read_only_fields = [
            'id', 'processed_by_name', 'external_refund_id', 'created_at', 'updated_at'
        ]


class RefundCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Refund
        fields = ['payment', 'amount', 'reason']
    
    def create(self, validated_data):
        validated_data['processed_by'] = self.context['request'].user
        return super().create(validated_data)


class DoctorPayoutSerializer(serializers.ModelSerializer):
    doctor = DoctorSerializer(read_only=True)
    doctor_name = serializers.CharField(source='doctor.full_name', read_only=True)
    appointments_count = serializers.SerializerMethodField()
    
    class Meta:
        model = DoctorPayout
        fields = [
            'id', 'doctor', 'doctor_name', 'amount', 'status', 'period_start',
            'period_end', 'appointments_count', 'external_payout_id',
            'processed_at', 'created_at', 'updated_at'
        ]
        read_only_fields = [
            'id', 'doctor_name', 'appointments_count', 'external_payout_id',
            'processed_at', 'created_at', 'updated_at'
        ]
    
    def get_appointments_count(self, obj):
        return obj.appointments.count()


class DoctorPayoutCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = DoctorPayout
        fields = [
            'doctor', 'amount', 'period_start', 'period_end', 'appointments'
        ]
