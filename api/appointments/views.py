from rest_framework import generics, status, permissions, filters
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from django_filters.rest_framework import DjangoFilterBackend
from django.utils import timezone
from datetime import datetime, timedelta
from .models import Appointment, ScheduleSlot, AppointmentReminder, AppointmentReschedule
from .serializers import (
    AppointmentSerializer, AppointmentCreateSerializer, AppointmentUpdateSerializer,
    AppointmentListSerializer, AppointmentRescheduleSerializer, ScheduleSlotSerializer
)
from users.permissions import IsPatient, IsDoctor, IsDoctorOrPatient


class AppointmentListView(generics.ListCreateAPIView):
    """
    List and create appointments
    """
    permission_classes = [permissions.IsAuthenticated, IsDoctorOrPatient]
    filter_backends = [DjangoFilterBackend, filters.OrderingFilter]
    filterset_fields = ['status', 'appointment_type', 'doctor', 'patient']
    ordering_fields = ['scheduled_at', 'created_at']
    ordering = ['-scheduled_at']
    
    def get_serializer_class(self):
        if self.request.method == 'POST':
            return AppointmentCreateSerializer
        return AppointmentListSerializer
    
    def get_queryset(self):
        user = self.request.user
        if user.is_doctor:
            return Appointment.objects.filter(doctor=user.doctor_profile)
        elif user.is_patient:
            return Appointment.objects.filter(patient=user)
        return Appointment.objects.none()
    
    def perform_create(self, serializer):
        serializer.save()


class AppointmentDetailView(generics.RetrieveUpdateAPIView):
    """
    Get and update appointment details
    """
    serializer_class = AppointmentSerializer
    permission_classes = [permissions.IsAuthenticated, IsDoctorOrPatient]
    
    def get_queryset(self):
        user = self.request.user
        if user.is_doctor:
            return Appointment.objects.filter(doctor=user.doctor_profile)
        elif user.is_patient:
            return Appointment.objects.filter(patient=user)
        return Appointment.objects.none()


class ScheduleSlotListView(generics.ListAPIView):
    """
    List available schedule slots for a doctor
    """
    serializer_class = ScheduleSlotSerializer
    permission_classes = [permissions.AllowAny]
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['doctor', 'status']
    
    def get_queryset(self):
        doctor_id = self.request.query_params.get('doctor_id')
        date = self.request.query_params.get('date')
        
        queryset = ScheduleSlot.objects.filter(status='open')
        
        if doctor_id:
            queryset = queryset.filter(doctor_id=doctor_id)
        
        if date:
            try:
                date_obj = datetime.strptime(date, '%Y-%m-%d').date()
                queryset = queryset.filter(start_time__date=date_obj)
            except ValueError:
                pass
        
        # Only show future slots
        queryset = queryset.filter(start_time__gt=timezone.now())
        
        return queryset.order_by('start_time')


class AppointmentRescheduleView(generics.CreateAPIView):
    """
    Reschedule an appointment
    """
    serializer_class = AppointmentRescheduleSerializer
    permission_classes = [permissions.IsAuthenticated, IsDoctorOrPatient]
    
    def create(self, request, *args, **kwargs):
        appointment_id = kwargs['appointment_id']
        
        try:
            appointment = Appointment.objects.get(id=appointment_id)
            
            # Check permissions
            user = request.user
            if not (user == appointment.patient or user == appointment.doctor.user):
                return Response(
                    {'error': 'Permission denied'},
                    status=status.HTTP_403_FORBIDDEN
                )
            
            # Check if appointment can be rescheduled
            if not appointment.can_be_rescheduled:
                return Response(
                    {'error': 'Appointment cannot be rescheduled'},
                    status=status.HTTP_400_BAD_REQUEST
                )
            
            serializer = self.get_serializer(data=request.data)
            serializer.is_valid(raise_exception=True)
            
            # Add context for serializer
            serializer.context.update({
                'appointment': appointment,
                'request': request
            })
            
            reschedule = serializer.save()
            return Response({
                'message': 'Appointment rescheduled successfully',
                'reschedule_id': reschedule.id
            }, status=status.HTTP_201_CREATED)
            
        except Appointment.DoesNotExist:
            return Response({'error': 'Appointment not found'}, status=status.HTTP_404_NOT_FOUND)


@api_view(['POST'])
@permission_classes([permissions.IsAuthenticated, IsDoctorOrPatient])
def cancel_appointment(request, appointment_id):
    """
    Cancel an appointment
    """
    try:
        appointment = Appointment.objects.get(id=appointment_id)
        
        # Check permissions
        user = request.user
        if not (user == appointment.patient or user == appointment.doctor.user):
            return Response(
                {'error': 'Permission denied'},
                status=status.HTTP_403_FORBIDDEN
            )
        
        # Check if appointment can be cancelled
        if not appointment.can_be_cancelled:
            return Response(
                {'error': 'Appointment cannot be cancelled'},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        # Update appointment status
        appointment.status = 'cancelled'
        appointment.save()
        
        # Free up the slot
        appointment.slot.status = 'open'
        appointment.slot.save()
        
        return Response({
            'message': 'Appointment cancelled successfully'
        }, status=status.HTTP_200_OK)
        
    except Appointment.DoesNotExist:
        return Response({'error': 'Appointment not found'}, status=status.HTTP_404_NOT_FOUND)


@api_view(['POST'])
@permission_classes([permissions.IsAuthenticated, IsDoctor])
def start_appointment(request, appointment_id):
    """
    Start an appointment (doctor only)
    """
    try:
        appointment = Appointment.objects.get(id=appointment_id, doctor=request.user.doctor_profile)
        
        if appointment.status != 'confirmed':
            return Response(
                {'error': 'Appointment must be confirmed to start'},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        appointment.status = 'in_progress'
        appointment.started_at = timezone.now()
        appointment.save()
        
        return Response({
            'message': 'Appointment started successfully',
            'started_at': appointment.started_at
        }, status=status.HTTP_200_OK)
        
    except Appointment.DoesNotExist:
        return Response({'error': 'Appointment not found'}, status=status.HTTP_404_NOT_FOUND)


@api_view(['POST'])
@permission_classes([permissions.IsAuthenticated, IsDoctor])
def end_appointment(request, appointment_id):
    """
    End an appointment (doctor only)
    """
    try:
        appointment = Appointment.objects.get(id=appointment_id, doctor=request.user.doctor_profile)
        
        if appointment.status != 'in_progress':
            return Response(
                {'error': 'Appointment must be in progress to end'},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        appointment.status = 'completed'
        appointment.ended_at = timezone.now()
        appointment.save()
        
        return Response({
            'message': 'Appointment completed successfully',
            'ended_at': appointment.ended_at,
            'duration_minutes': appointment.duration_minutes
        }, status=status.HTTP_200_OK)
        
    except Appointment.DoesNotExist:
        return Response({'error': 'Appointment not found'}, status=status.HTTP_404_NOT_FOUND)


@api_view(['GET'])
@permission_classes([permissions.IsAuthenticated, IsDoctorOrPatient])
def appointment_reminders(request, appointment_id):
    """
    Get reminders for an appointment
    """
    try:
        appointment = Appointment.objects.get(id=appointment_id)
        
        # Check permissions
        user = request.user
        if not (user == appointment.patient or user == appointment.doctor.user):
            return Response(
                {'error': 'Permission denied'},
                status=status.HTTP_403_FORBIDDEN
            )
        
        reminders = AppointmentReminder.objects.filter(appointment=appointment)
        serializer = AppointmentReminderSerializer(reminders, many=True)
        
        return Response(serializer.data)
        
    except Appointment.DoesNotExist:
        return Response({'error': 'Appointment not found'}, status=status.HTTP_404_NOT_FOUND)


@api_view(['GET'])
@permission_classes([permissions.IsAuthenticated])
def upcoming_appointments(request):
    """
    Get upcoming appointments for the current user
    """
    user = request.user
    now = timezone.now()
    
    if user.is_doctor:
        appointments = Appointment.objects.filter(
            doctor=user.doctor_profile,
            scheduled_at__gt=now,
            status__in=['pending', 'confirmed']
        )
    elif user.is_patient:
        appointments = Appointment.objects.filter(
            patient=user,
            scheduled_at__gt=now,
            status__in=['pending', 'confirmed']
        )
    else:
        appointments = Appointment.objects.none()
    
    serializer = AppointmentListSerializer(appointments, many=True)
    return Response(serializer.data)
