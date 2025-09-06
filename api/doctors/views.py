from rest_framework import generics, status, permissions, filters
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from django_filters.rest_framework import DjangoFilterBackend
from django.db.models import Q
from .models import Doctor, DoctorAvailability, DoctorReview
from .serializers import (
    DoctorSerializer, DoctorListSerializer, DoctorRegistrationSerializer,
    DoctorAvailabilitySerializer, DoctorReviewSerializer, DoctorReviewCreateSerializer
)
from users.permissions import IsDoctor, IsPatient


class DoctorListView(generics.ListAPIView):
    """
    List all doctors with filtering and search
    """
    queryset = Doctor.objects.filter(is_available_for_consultation=True, kyc_status='verified')
    serializer_class = DoctorListSerializer
    permission_classes = [permissions.AllowAny]
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = ['specialties', 'consultation_fee']
    search_fields = ['user__first_name', 'user__last_name', 'clinic_name', 'specialties']
    ordering_fields = ['average_rating', 'consultation_fee', 'years_of_experience']
    ordering = ['-average_rating']


class DoctorDetailView(generics.RetrieveAPIView):
    """
    Get doctor details
    """
    queryset = Doctor.objects.all()
    serializer_class = DoctorSerializer
    permission_classes = [permissions.AllowAny]


class DoctorRegistrationView(generics.CreateAPIView):
    """
    Doctor registration endpoint
    """
    queryset = Doctor.objects.all()
    serializer_class = DoctorRegistrationSerializer
    permission_classes = [permissions.IsAuthenticated]


class DoctorProfileView(generics.RetrieveUpdateAPIView):
    """
    Get and update doctor's own profile
    """
    serializer_class = DoctorSerializer
    permission_classes = [permissions.IsAuthenticated, IsDoctor]
    
    def get_object(self):
        return self.request.user.doctor_profile


class DoctorAvailabilityView(generics.ListCreateAPIView):
    """
    Manage doctor's availability schedule
    """
    serializer_class = DoctorAvailabilitySerializer
    permission_classes = [permissions.IsAuthenticated, IsDoctor]
    
    def get_queryset(self):
        return DoctorAvailability.objects.filter(doctor=self.request.user.doctor_profile)
    
    def perform_create(self, serializer):
        serializer.save(doctor=self.request.user.doctor_profile)


class DoctorAvailabilityDetailView(generics.RetrieveUpdateDestroyAPIView):
    """
    Update specific availability slot
    """
    serializer_class = DoctorAvailabilitySerializer
    permission_classes = [permissions.IsAuthenticated, IsDoctor]
    
    def get_queryset(self):
        return DoctorAvailability.objects.filter(doctor=self.request.user.doctor_profile)


class DoctorReviewsView(generics.ListAPIView):
    """
    Get reviews for a specific doctor
    """
    serializer_class = DoctorReviewSerializer
    permission_classes = [permissions.AllowAny]
    
    def get_queryset(self):
        doctor_id = self.kwargs['doctor_id']
        return DoctorReview.objects.filter(doctor_id=doctor_id).order_by('-created_at')


class CreateDoctorReviewView(generics.CreateAPIView):
    """
    Create a review for a doctor
    """
    serializer_class = DoctorReviewCreateSerializer
    permission_classes = [permissions.IsAuthenticated, IsPatient]
    
    def create(self, request, *args, **kwargs):
        doctor_id = kwargs['doctor_id']
        appointment_id = request.data.get('appointment_id')
        
        try:
            doctor = Doctor.objects.get(id=doctor_id)
            appointment = request.user.appointments.get(id=appointment_id)
            
            # Check if review already exists
            if DoctorReview.objects.filter(doctor=doctor, patient=request.user, appointment=appointment).exists():
                return Response(
                    {'error': 'Review already exists for this appointment'},
                    status=status.HTTP_400_BAD_REQUEST
                )
            
            serializer = self.get_serializer(data=request.data)
            serializer.is_valid(raise_exception=True)
            
            # Add context for serializer
            serializer.context.update({
                'doctor': doctor,
                'patient': request.user,
                'appointment': appointment
            })
            
            review = serializer.save()
            return Response(DoctorReviewSerializer(review).data, status=status.HTTP_201_CREATED)
            
        except Doctor.DoesNotExist:
            return Response({'error': 'Doctor not found'}, status=status.HTTP_404_NOT_FOUND)
        except Exception as e:
            return Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)


@api_view(['GET'])
@permission_classes([permissions.AllowAny])
def doctor_availability_slots(request, doctor_id):
    """
    Get available time slots for a doctor on a specific date
    """
    date = request.GET.get('date')
    if not date:
        return Response({'error': 'Date parameter is required'}, status=status.HTTP_400_BAD_REQUEST)
    
    try:
        doctor = Doctor.objects.get(id=doctor_id)
        # TODO: Implement slot generation logic based on doctor's availability and existing appointments
        # This would integrate with the appointments app
        
        return Response({
            'doctor_id': doctor_id,
            'date': date,
            'available_slots': []  # Placeholder
        })
    except Doctor.DoesNotExist:
        return Response({'error': 'Doctor not found'}, status=status.HTTP_404_NOT_FOUND)


@api_view(['POST'])
@permission_classes([permissions.IsAuthenticated, IsDoctor])
def update_kyc_status(request):
    """
    Update KYC status and documents (admin only in production)
    """
    doctor = request.user.doctor_profile
    kyc_documents = request.data.get('kyc_documents', [])
    
    doctor.kyc_documents = kyc_documents
    doctor.kyc_status = 'pending'  # Reset to pending for review
    doctor.save()
    
    return Response({
        'message': 'KYC documents updated successfully',
        'kyc_status': doctor.kyc_status
    })
