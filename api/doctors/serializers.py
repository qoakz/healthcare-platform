from rest_framework import serializers
from .models import Doctor, DoctorAvailability, DoctorReview
from users.serializers import UserSerializer


class DoctorAvailabilitySerializer(serializers.ModelSerializer):
    class Meta:
        model = DoctorAvailability
        fields = ['id', 'day_of_week', 'start_time', 'end_time', 'is_available', 'break_times']


class DoctorReviewSerializer(serializers.ModelSerializer):
    patient_name = serializers.CharField(source='patient.get_full_name', read_only=True)
    
    class Meta:
        model = DoctorReview
        fields = [
            'id', 'patient_name', 'rating', 'comment', 'communication_rating',
            'treatment_rating', 'punctuality_rating', 'is_anonymous', 'created_at'
        ]
        read_only_fields = ['id', 'patient_name', 'created_at']


class DoctorSerializer(serializers.ModelSerializer):
    user = UserSerializer(read_only=True)
    availability = DoctorAvailabilitySerializer(many=True, read_only=True)
    reviews = DoctorReviewSerializer(many=True, read_only=True)
    
    class Meta:
        model = Doctor
        fields = [
            'id', 'user', 'registration_number', 'years_of_experience', 'specialties',
            'clinic_name', 'clinic_address', 'consultation_fee', 'kyc_status',
            'is_available_for_consultation', 'max_patients_per_day', 'average_rating',
            'total_reviews', 'availability', 'reviews', 'created_at'
        ]
        read_only_fields = ['id', 'average_rating', 'total_reviews', 'created_at']


class DoctorListSerializer(serializers.ModelSerializer):
    """
    Simplified serializer for doctor listing
    """
    full_name = serializers.CharField(source='user.get_full_name', read_only=True)
    specialties_display = serializers.SerializerMethodField()
    
    class Meta:
        model = Doctor
        fields = [
            'id', 'full_name', 'specialties', 'specialties_display', 'years_of_experience',
            'clinic_name', 'consultation_fee', 'average_rating', 'total_reviews',
            'is_available_for_consultation'
        ]
    
    def get_specialties_display(self, obj):
        return ', '.join(obj.specialties)


class DoctorRegistrationSerializer(serializers.ModelSerializer):
    """
    Serializer for doctor registration
    """
    user_id = serializers.IntegerField(write_only=True)
    
    class Meta:
        model = Doctor
        fields = [
            'user_id', 'registration_number', 'years_of_experience', 'specialties',
            'clinic_name', 'clinic_address', 'consultation_fee', 'medical_license_url',
            'degree_certificates'
        ]
    
    def create(self, validated_data):
        user_id = validated_data.pop('user_id')
        doctor = Doctor.objects.create(**validated_data)
        return doctor


class DoctorAvailabilityUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = DoctorAvailability
        fields = ['day_of_week', 'start_time', 'end_time', 'is_available', 'break_times']


class DoctorReviewCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = DoctorReview
        fields = [
            'rating', 'comment', 'communication_rating', 'treatment_rating',
            'punctuality_rating', 'is_anonymous'
        ]
    
    def create(self, validated_data):
        # Get doctor and patient from context
        doctor = self.context['doctor']
        patient = self.context['patient']
        appointment = self.context['appointment']
        
        review = DoctorReview.objects.create(
            doctor=doctor,
            patient=patient,
            appointment=appointment,
            **validated_data
        )
        
        # Update doctor's average rating
        doctor.update_rating()
        
        return review
