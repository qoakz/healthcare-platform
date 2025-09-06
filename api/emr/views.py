from rest_framework import generics, status, permissions
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from django.shortcuts import get_object_or_404
from django.db.models import Q
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import filters
from django.http import HttpResponse
from datetime import datetime

from .models import MedicalRecord, Prescription, LabResult, VitalSign, Allergy
from .serializers import (
    MedicalRecordSerializer, MedicalRecordCreateSerializer,
    PrescriptionSerializer, PrescriptionCreateSerializer,
    LabResultSerializer, LabResultCreateSerializer,
    VitalSignSerializer, VitalSignCreateSerializer,
    AllergySerializer, AllergyCreateSerializer
)
from .pdf_generator import generate_prescription_response
from .medical_record_pdf import generate_medical_record_pdf
from users.permissions import IsDoctor, IsPatient, IsAdmin

class MedicalRecordListView(generics.ListCreateAPIView):
    """List and create medical records"""
    permission_classes = [permissions.IsAuthenticated]
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = ['patient', 'doctor', 'is_active']
    search_fields = ['chief_complaint', 'diagnosis', 'patient__first_name', 'patient__last_name']
    ordering_fields = ['created_at', 'updated_at']
    ordering = ['-created_at']
    
    def get_queryset(self):
        user = self.request.user
        if user.role == 'doctor':
            return MedicalRecord.objects.filter(doctor=user)
        elif user.role == 'patient':
            return MedicalRecord.objects.filter(patient=user)
        elif user.role == 'admin':
            return MedicalRecord.objects.all()
        return MedicalRecord.objects.none()
    
    def get_serializer_class(self):
        if self.request.method == 'POST':
            return MedicalRecordCreateSerializer
        return MedicalRecordSerializer

class MedicalRecordDetailView(generics.RetrieveUpdateDestroyAPIView):
    """Retrieve, update, or delete a medical record"""
    permission_classes = [permissions.IsAuthenticated]
    
    def get_queryset(self):
        user = self.request.user
        if user.role == 'doctor':
            return MedicalRecord.objects.filter(doctor=user)
        elif user.role == 'patient':
            return MedicalRecord.objects.filter(patient=user)
        elif user.role == 'admin':
            return MedicalRecord.objects.all()
        return MedicalRecord.objects.none()
    
    def get_serializer_class(self):
        if self.request.method in ['PUT', 'PATCH']:
            return MedicalRecordCreateSerializer
        return MedicalRecordSerializer

class PrescriptionListView(generics.ListCreateAPIView):
    """List and create prescriptions"""
    permission_classes = [permissions.IsAuthenticated, IsDoctor]
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = ['patient', 'doctor', 'status', 'medical_record']
    search_fields = ['medication_name', 'generic_name', 'patient__first_name', 'patient__last_name']
    ordering_fields = ['created_at', 'medication_name']
    ordering = ['-created_at']
    
    def get_queryset(self):
        user = self.request.user
        if user.role == 'doctor':
            return Prescription.objects.filter(doctor=user)
        elif user.role == 'patient':
            return Prescription.objects.filter(patient=user)
        elif user.role == 'admin':
            return Prescription.objects.all()
        return Prescription.objects.none()
    
    def get_serializer_class(self):
        if self.request.method == 'POST':
            return PrescriptionCreateSerializer
        return PrescriptionSerializer

class PrescriptionDetailView(generics.RetrieveUpdateDestroyAPIView):
    """Retrieve, update, or delete a prescription"""
    permission_classes = [permissions.IsAuthenticated]
    
    def get_queryset(self):
        user = self.request.user
        if user.role == 'doctor':
            return Prescription.objects.filter(doctor=user)
        elif user.role == 'patient':
            return Prescription.objects.filter(patient=user)
        elif user.role == 'admin':
            return Prescription.objects.all()
        return MedicalRecord.objects.none()
    
    def get_serializer_class(self):
        if self.request.method in ['PUT', 'PATCH']:
            return PrescriptionCreateSerializer
        return PrescriptionSerializer

class LabResultListView(generics.ListCreateAPIView):
    """List and create lab results"""
    permission_classes = [permissions.IsAuthenticated]
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = ['patient', 'doctor', 'status', 'medical_record', 'test_type']
    search_fields = ['test_name', 'patient__first_name', 'patient__last_name']
    ordering_fields = ['test_date', 'created_at']
    ordering = ['-test_date']
    
    def get_queryset(self):
        user = self.request.user
        if user.role == 'doctor':
            return LabResult.objects.filter(doctor=user)
        elif user.role == 'patient':
            return LabResult.objects.filter(patient=user)
        elif user.role == 'admin':
            return LabResult.objects.all()
        return LabResult.objects.none()
    
    def get_serializer_class(self):
        if self.request.method == 'POST':
            return LabResultCreateSerializer
        return LabResultSerializer

class LabResultDetailView(generics.RetrieveUpdateDestroyAPIView):
    """Retrieve, update, or delete a lab result"""
    permission_classes = [permissions.IsAuthenticated]
    
    def get_queryset(self):
        user = self.request.user
        if user.role == 'doctor':
            return LabResult.objects.filter(doctor=user)
        elif user.role == 'patient':
            return LabResult.objects.filter(patient=user)
        elif user.role == 'admin':
            return LabResult.objects.all()
        return LabResult.objects.none()
    
    def get_serializer_class(self):
        if self.request.method in ['PUT', 'PATCH']:
            return LabResultCreateSerializer
        return LabResultSerializer

class VitalSignListView(generics.ListCreateAPIView):
    """List and create vital signs"""
    permission_classes = [permissions.IsAuthenticated]
    filter_backends = [DjangoFilterBackend, filters.OrderingFilter]
    filterset_fields = ['patient', 'recorded_by', 'medical_record']
    ordering_fields = ['recorded_at']
    ordering = ['-recorded_at']
    
    def get_queryset(self):
        user = self.request.user
        if user.role == 'doctor':
            return VitalSign.objects.filter(recorded_by=user)
        elif user.role == 'patient':
            return VitalSign.objects.filter(patient=user)
        elif user.role == 'admin':
            return VitalSign.objects.all()
        return VitalSign.objects.none()
    
    def get_serializer_class(self):
        if self.request.method == 'POST':
            return VitalSignCreateSerializer
        return VitalSignSerializer

class VitalSignDetailView(generics.RetrieveUpdateDestroyAPIView):
    """Retrieve, update, or delete vital signs"""
    permission_classes = [permissions.IsAuthenticated]
    
    def get_queryset(self):
        user = self.request.user
        if user.role == 'doctor':
            return VitalSign.objects.filter(recorded_by=user)
        elif user.role == 'patient':
            return VitalSign.objects.filter(patient=user)
        elif user.role == 'admin':
            return VitalSign.objects.all()
        return VitalSign.objects.none()
    
    def get_serializer_class(self):
        if self.request.method in ['PUT', 'PATCH']:
            return VitalSignCreateSerializer
        return VitalSignSerializer

class AllergyListView(generics.ListCreateAPIView):
    """List and create allergies"""
    permission_classes = [permissions.IsAuthenticated]
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = ['patient', 'recorded_by', 'allergy_type', 'severity', 'is_active']
    search_fields = ['allergen', 'patient__first_name', 'patient__last_name']
    ordering_fields = ['confirmed_date', 'created_at']
    ordering = ['-confirmed_date']
    
    def get_queryset(self):
        user = self.request.user
        if user.role == 'doctor':
            return Allergy.objects.filter(recorded_by=user)
        elif user.role == 'patient':
            return Allergy.objects.filter(patient=user)
        elif user.role == 'admin':
            return Allergy.objects.all()
        return Allergy.objects.none()
    
    def get_serializer_class(self):
        if self.request.method == 'POST':
            return AllergyCreateSerializer
        return AllergySerializer

class AllergyDetailView(generics.RetrieveUpdateDestroyAPIView):
    """Retrieve, update, or delete an allergy"""
    permission_classes = [permissions.IsAuthenticated]
    
    def get_queryset(self):
        user = self.request.user
        if user.role == 'doctor':
            return Allergy.objects.filter(recorded_by=user)
        elif user.role == 'patient':
            return Allergy.objects.filter(patient=user)
        elif user.role == 'admin':
            return Allergy.objects.all()
        return Allergy.objects.none()
    
    def get_serializer_class(self):
        if self.request.method in ['PUT', 'PATCH']:
            return AllergyCreateSerializer
        return AllergySerializer

# PDF Generation Views
@api_view(['GET'])
@permission_classes([permissions.IsAuthenticated])
def download_prescription_pdf(request, prescription_id):
    """Download prescription as PDF"""
    prescription = get_object_or_404(Prescription, id=prescription_id)
    
    # Check permissions
    user = request.user
    if user.role == 'patient' and prescription.patient != user:
        return Response({'error': 'Access denied'}, status=status.HTTP_403_FORBIDDEN)
    elif user.role == 'doctor' and prescription.doctor != user:
        return Response({'error': 'Access denied'}, status=status.HTTP_403_FORBIDDEN)
    elif user.role not in ['admin', 'doctor', 'patient']:
        return Response({'error': 'Access denied'}, status=status.HTTP_403_FORBIDDEN)
    
    return generate_prescription_response(prescription, request)

@api_view(['GET'])
@permission_classes([permissions.IsAuthenticated])
def download_medical_record_pdf(request, medical_record_id):
    """Download medical record as PDF"""
    medical_record = get_object_or_404(MedicalRecord, id=medical_record_id)
    
    # Check permissions
    user = request.user
    if user.role == 'patient' and medical_record.patient != user:
        return Response({'error': 'Access denied'}, status=status.HTTP_403_FORBIDDEN)
    elif user.role == 'doctor' and medical_record.doctor != user:
        return Response({'error': 'Access denied'}, status=status.HTTP_403_FORBIDDEN)
    elif user.role not in ['admin', 'doctor', 'patient']:
        return Response({'error': 'Access denied'}, status=status.HTTP_403_FORBIDDEN)
    
    pdf_bytes = generate_medical_record_pdf(medical_record, request)
    filename = f"medical_record_{medical_record.id}_{datetime.now().strftime('%Y%m%d_%H%M%S')}.pdf"
    
    response = HttpResponse(pdf_bytes, content_type='application/pdf')
    response['Content-Disposition'] = f'attachment; filename="{filename}"'
    return response

# Statistics and Analytics
@api_view(['GET'])
@permission_classes([permissions.IsAuthenticated, IsDoctor])
def doctor_emr_stats(request):
    """Get EMR statistics for a doctor"""
    doctor = request.user
    
    stats = {
        'total_records': MedicalRecord.objects.filter(doctor=doctor).count(),
        'total_prescriptions': Prescription.objects.filter(doctor=doctor).count(),
        'total_lab_results': LabResult.objects.filter(doctor=doctor).count(),
        'active_prescriptions': Prescription.objects.filter(doctor=doctor, status='pending').count(),
        'completed_lab_results': LabResult.objects.filter(doctor=doctor, status='completed').count(),
        'recent_records': MedicalRecord.objects.filter(doctor=doctor).order_by('-created_at')[:5].values(
            'id', 'patient__first_name', 'patient__last_name', 'created_at', 'diagnosis'
        )
    }
    
    return Response(stats)

@api_view(['GET'])
@permission_classes([permissions.IsAuthenticated, IsPatient])
def patient_emr_summary(request):
    """Get EMR summary for a patient"""
    patient = request.user
    
    # Get latest medical record
    latest_record = MedicalRecord.objects.filter(patient=patient).order_by('-created_at').first()
    
    # Get active prescriptions
    active_prescriptions = Prescription.objects.filter(
        patient=patient, 
        status='pending'
    ).order_by('-created_at')
    
    # Get recent lab results
    recent_lab_results = LabResult.objects.filter(
        patient=patient, 
        status='completed'
    ).order_by('-result_date')[:5]
    
    # Get allergies
    allergies = Allergy.objects.filter(patient=patient, is_active=True)
    
    # Get latest vital signs
    latest_vitals = VitalSign.objects.filter(patient=patient).order_by('-recorded_at').first()
    
    summary = {
        'latest_record': MedicalRecordSerializer(latest_record).data if latest_record else None,
        'active_prescriptions': PrescriptionSerializer(active_prescriptions, many=True).data,
        'recent_lab_results': LabResultSerializer(recent_lab_results, many=True).data,
        'allergies': AllergySerializer(allergies, many=True).data,
        'latest_vitals': VitalSignSerializer(latest_vitals).data if latest_vitals else None,
        'total_records': MedicalRecord.objects.filter(patient=patient).count(),
        'total_prescriptions': Prescription.objects.filter(patient=patient).count(),
    }
    
    return Response(summary)