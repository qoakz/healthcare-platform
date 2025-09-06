from rest_framework import serializers
from django.contrib.auth import get_user_model
from .models import MedicalRecord, Prescription, LabResult, VitalSign, Allergy

User = get_user_model()

class VitalSignSerializer(serializers.ModelSerializer):
    recorded_by_name = serializers.CharField(source='recorded_by.get_full_name', read_only=True)
    
    class Meta:
        model = VitalSign
        fields = [
            'id', 'patient', 'recorded_by', 'recorded_by_name', 'medical_record',
            'blood_pressure_systolic', 'blood_pressure_diastolic', 'heart_rate',
            'temperature', 'respiratory_rate', 'oxygen_saturation', 'weight',
            'height', 'bmi', 'pain_level', 'recorded_at', 'notes'
        ]
        read_only_fields = ['id', 'recorded_at', 'bmi']

class AllergySerializer(serializers.ModelSerializer):
    recorded_by_name = serializers.CharField(source='recorded_by.get_full_name', read_only=True)
    
    class Meta:
        model = Allergy
        fields = [
            'id', 'patient', 'recorded_by', 'recorded_by_name', 'allergen',
            'allergy_type', 'severity', 'reaction', 'notes', 'is_active',
            'confirmed_date', 'created_at', 'updated_at'
        ]
        read_only_fields = ['id', 'created_at', 'updated_at']

class PrescriptionSerializer(serializers.ModelSerializer):
    doctor_name = serializers.CharField(source='doctor.get_full_name', read_only=True)
    patient_name = serializers.CharField(source='patient.get_full_name', read_only=True)
    is_expired = serializers.BooleanField(read_only=True)
    
    class Meta:
        model = Prescription
        fields = [
            'id', 'medical_record', 'patient', 'patient_name', 'doctor', 'doctor_name',
            'medication_name', 'generic_name', 'dosage', 'frequency', 'duration',
            'quantity', 'instructions', 'status', 'refills_allowed', 'refills_used',
            'expiry_date', 'is_expired', 'created_at', 'updated_at'
        ]
        read_only_fields = ['id', 'created_at', 'updated_at', 'is_expired']

class LabResultSerializer(serializers.ModelSerializer):
    doctor_name = serializers.CharField(source='doctor.get_full_name', read_only=True)
    patient_name = serializers.CharField(source='patient.get_full_name', read_only=True)
    result_file_url = serializers.SerializerMethodField()
    
    class Meta:
        model = LabResult
        fields = [
            'id', 'medical_record', 'patient', 'patient_name', 'doctor', 'doctor_name',
            'test_name', 'test_type', 'lab_name', 'test_date', 'result_date',
            'results', 'normal_range', 'interpretation', 'notes', 'result_file',
            'result_file_url', 'status', 'created_at', 'updated_at'
        ]
        read_only_fields = ['id', 'created_at', 'updated_at']
    
    def get_result_file_url(self, obj):
        if obj.result_file:
            request = self.context.get('request')
            if request:
                return request.build_absolute_uri(obj.result_file.url)
        return None

class MedicalRecordSerializer(serializers.ModelSerializer):
    doctor_name = serializers.CharField(source='doctor.get_full_name', read_only=True)
    patient_name = serializers.CharField(source='patient.get_full_name', read_only=True)
    prescriptions = PrescriptionSerializer(many=True, read_only=True)
    lab_results = LabResultSerializer(many=True, read_only=True)
    record_vital_signs = VitalSignSerializer(many=True, read_only=True)
    
    class Meta:
        model = MedicalRecord
        fields = [
            'id', 'patient', 'patient_name', 'doctor', 'doctor_name', 'appointment',
            'chief_complaint', 'history_of_present_illness', 'past_medical_history',
            'family_history', 'social_history', 'record_vital_signs', 'physical_examination',
            'diagnosis', 'treatment_plan', 'notes', 'follow_up_required',
            'follow_up_date', 'prescriptions', 'lab_results', 'is_active',
            'created_at', 'updated_at'
        ]
        read_only_fields = ['id', 'created_at', 'updated_at']

class MedicalRecordCreateSerializer(serializers.ModelSerializer):
    """Serializer for creating medical records with prescriptions"""
    prescriptions = PrescriptionSerializer(many=True, required=False)
    lab_results = LabResultSerializer(many=True, required=False)
    
    class Meta:
        model = MedicalRecord
        fields = [
            'patient', 'appointment', 'chief_complaint', 'history_of_present_illness',
            'past_medical_history', 'family_history', 'social_history', 'vital_signs',
            'physical_examination', 'diagnosis', 'treatment_plan', 'notes',
            'follow_up_required', 'follow_up_date', 'prescriptions', 'lab_results'
        ]
    
    def create(self, validated_data):
        prescriptions_data = validated_data.pop('prescriptions', [])
        lab_results_data = validated_data.pop('lab_results', [])
        
        # Set doctor from request user
        validated_data['doctor'] = self.context['request'].user
        
        medical_record = MedicalRecord.objects.create(**validated_data)
        
        # Create prescriptions
        for prescription_data in prescriptions_data:
            prescription_data['patient'] = medical_record.patient
            prescription_data['doctor'] = medical_record.doctor
            Prescription.objects.create(medical_record=medical_record, **prescription_data)
        
        # Create lab results
        for lab_result_data in lab_results_data:
            lab_result_data['patient'] = medical_record.patient
            lab_result_data['doctor'] = medical_record.doctor
            LabResult.objects.create(medical_record=medical_record, **lab_result_data)
        
        return medical_record

class PrescriptionCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Prescription
        fields = [
            'medical_record', 'medication_name', 'generic_name', 'dosage',
            'frequency', 'duration', 'quantity', 'instructions', 'refills_allowed',
            'expiry_date'
        ]
    
    def create(self, validated_data):
        # Set patient and doctor from medical record
        medical_record = validated_data['medical_record']
        validated_data['patient'] = medical_record.patient
        validated_data['doctor'] = medical_record.doctor
        
        return Prescription.objects.create(**validated_data)

class LabResultCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = LabResult
        fields = [
            'medical_record', 'test_name', 'test_type', 'lab_name', 'test_date',
            'result_date', 'results', 'normal_range', 'interpretation', 'notes',
            'result_file', 'status'
        ]
    
    def create(self, validated_data):
        # Set patient and doctor from medical record
        medical_record = validated_data['medical_record']
        validated_data['patient'] = medical_record.patient
        validated_data['doctor'] = medical_record.doctor
        
        return LabResult.objects.create(**validated_data)

class VitalSignCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = VitalSign
        fields = [
            'patient', 'medical_record', 'blood_pressure_systolic', 'blood_pressure_diastolic',
            'heart_rate', 'temperature', 'respiratory_rate', 'oxygen_saturation',
            'weight', 'height', 'pain_level', 'notes'
        ]
    
    def create(self, validated_data):
        # Set recorded_by from request user
        validated_data['recorded_by'] = self.context['request'].user
        return VitalSign.objects.create(**validated_data)

class AllergyCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Allergy
        fields = [
            'patient', 'allergen', 'allergy_type', 'severity', 'reaction',
            'notes', 'confirmed_date'
        ]
    
    def create(self, validated_data):
        # Set recorded_by from request user
        validated_data['recorded_by'] = self.context['request'].user
        return Allergy.objects.create(**validated_data)