from rest_framework import generics, status, permissions, filters
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from django_filters.rest_framework import DjangoFilterBackend
from django.utils import timezone
from django.shortcuts import get_object_or_404
from .models import RTCRoom, RTCSignal, RTCJoinToken
from .serializers import (
    RTCRoomSerializer, RTCRoomCreateSerializer, RTCSignalSerializer,
    RTCSignalCreateSerializer, RTCJoinTokenSerializer, RTCJoinTokenCreateSerializer
)
from users.permissions import IsDoctorOrPatient


class RTCRoomListView(generics.ListCreateAPIView):
    """
    List and create RTC rooms
    """
    permission_classes = [permissions.IsAuthenticated, IsDoctorOrPatient]
    filter_backends = [DjangoFilterBackend, filters.OrderingFilter]
    filterset_fields = ['status', 'appointment__doctor', 'appointment__patient']
    ordering_fields = ['created_at', 'started_at']
    ordering = ['-created_at']
    
    def get_serializer_class(self):
        if self.request.method == 'POST':
            return RTCRoomCreateSerializer
        return RTCRoomSerializer
    
    def get_queryset(self):
        user = self.request.user
        if user.is_doctor:
            return RTCRoom.objects.filter(appointment__doctor=user.doctor_profile)
        elif user.is_patient:
            return RTCRoom.objects.filter(appointment__patient=user)
        return RTCRoom.objects.none()


class RTCRoomDetailView(generics.RetrieveUpdateAPIView):
    """
    Get and update RTC room details
    """
    serializer_class = RTCRoomSerializer
    permission_classes = [permissions.IsAuthenticated, IsDoctorOrPatient]
    
    def get_queryset(self):
        user = self.request.user
        if user.is_doctor:
            return RTCRoom.objects.filter(appointment__doctor=user.doctor_profile)
        elif user.is_patient:
            return RTCRoom.objects.filter(appointment__patient=user)
        return RTCRoom.objects.none()


class RTCSignalListView(generics.ListCreateAPIView):
    """
    List and create RTC signals
    """
    permission_classes = [permissions.IsAuthenticated, IsDoctorOrPatient]
    filter_backends = [DjangoFilterBackend, filters.OrderingFilter]
    filterset_fields = ['room', 'signal_type', 'sender']
    ordering_fields = ['created_at']
    ordering = ['created_at']
    
    def get_serializer_class(self):
        if self.request.method == 'POST':
            return RTCSignalCreateSerializer
        return RTCSignalSerializer
    
    def get_queryset(self):
        user = self.request.user
        if user.is_doctor:
            return RTCSignal.objects.filter(room__appointment__doctor=user.doctor_profile)
        elif user.is_patient:
            return RTCSignal.objects.filter(room__appointment__patient=user)
        return RTCSignal.objects.none()


class RTCJoinTokenListView(generics.ListCreateAPIView):
    """
    List and create RTC join tokens
    """
    permission_classes = [permissions.IsAuthenticated, IsDoctorOrPatient]
    filter_backends = [DjangoFilterBackend, filters.OrderingFilter]
    filterset_fields = ['room', 'user']
    ordering_fields = ['created_at', 'expires_at']
    ordering = ['-created_at']
    
    def get_serializer_class(self):
        if self.request.method == 'POST':
            return RTCJoinTokenCreateSerializer
        return RTCJoinTokenSerializer
    
    def get_queryset(self):
        user = self.request.user
        if user.is_doctor:
            return RTCJoinToken.objects.filter(room__appointment__doctor=user.doctor_profile)
        elif user.is_patient:
            return RTCJoinToken.objects.filter(room__appointment__patient=user)
        return RTCJoinToken.objects.none()


@api_view(['POST'])
@permission_classes([permissions.IsAuthenticated, IsDoctorOrPatient])
def create_room_for_appointment(request, appointment_id):
    """
    Create an RTC room for a specific appointment
    """
    try:
        from appointments.models import Appointment
        
        # Get appointment
        appointment = Appointment.objects.get(id=appointment_id)
        
        # Check permissions
        user = request.user
        if not (user == appointment.patient or user == appointment.doctor.user):
            return Response(
                {'error': 'Permission denied'}, 
                status=status.HTTP_403_FORBIDDEN
            )
        
        # Check if room already exists
        if hasattr(appointment, 'rtc_room'):
            return Response({
                'room_id': appointment.rtc_room.room_id,
                'status': appointment.rtc_room.status,
                'message': 'Room already exists for this appointment'
            })
        
        # Create room
        import uuid
        from datetime import timedelta
        
        room_id = f"room_{uuid.uuid4().hex[:12]}"
        expires_at = timezone.now() + timedelta(hours=2)  # Room expires in 2 hours
        
        room = RTCRoom.objects.create(
            appointment=appointment,
            room_id=room_id,
            expires_at=expires_at,
            max_participants=2,
            recording_enabled=False
        )
        
        return Response({
            'room_id': room.room_id,
            'status': room.status,
            'expires_at': room.expires_at,
            'message': 'Room created successfully'
        })
        
    except Appointment.DoesNotExist:
        return Response({'error': 'Appointment not found'}, status=status.HTTP_404_NOT_FOUND)


@api_view(['POST'])
@permission_classes([permissions.IsAuthenticated, IsDoctorOrPatient])
def join_room(request, room_id):
    """
    Join an RTC room
    """
    try:
        room = RTCRoom.objects.get(room_id=room_id)
        
        # Check permissions
        user = request.user
        if not (user == room.appointment.patient or user == room.appointment.doctor.user):
            return Response(
                {'error': 'Permission denied'}, 
                status=status.HTTP_403_FORBIDDEN
            )
        
        # Check if room is active
        if room.status != 'active':
            return Response(
                {'error': 'Room is not active'}, 
                status=status.HTTP_400_BAD_REQUEST
            )
        
        # Check if room has expired
        if room.expires_at < timezone.now():
            room.status = 'expired'
            room.save()
            return Response(
                {'error': 'Room has expired'}, 
                status=status.HTTP_400_BAD_REQUEST
            )
        
        # Generate join token
        import jwt
        from datetime import datetime, timedelta
        from django.conf import settings
        
        expires_at = timezone.now() + timedelta(minutes=30)  # Token expires in 30 minutes
        
        payload = {
            'user_id': user.id,
            'room_id': room.room_id,
            'exp': expires_at
        }
        
        token = jwt.encode(payload, settings.SECRET_KEY, algorithm='HS256')
        
        # Create join token record
        join_token = RTCJoinToken.objects.create(
            room=room,
            user=user,
            token=token,
            expires_at=expires_at
        )
        
        return Response({
            'join_token': token,
            'expires_at': expires_at,
            'room_id': room.room_id,
            'message': 'Join token generated successfully'
        })
        
    except RTCRoom.DoesNotExist:
        return Response({'error': 'Room not found'}, status=status.HTTP_404_NOT_FOUND)


@api_view(['POST'])
@permission_classes([permissions.IsAuthenticated, IsDoctorOrPatient])
def start_room(request, room_id):
    """
    Start an RTC room (doctor only)
    """
    try:
        room = RTCRoom.objects.get(room_id=room_id)
        
        # Check permissions (only doctor can start the room)
        user = request.user
        if user != room.appointment.doctor.user:
            return Response(
                {'error': 'Only the doctor can start the room'}, 
                status=status.HTTP_403_FORBIDDEN
            )
        
        # Check if room can be started
        if room.status != 'created':
            return Response(
                {'error': f'Room cannot be started from status: {room.status}'}, 
                status=status.HTTP_400_BAD_REQUEST
            )
        
        # Start the room
        room.status = 'active'
        room.started_at = timezone.now()
        room.save()
        
        return Response({
            'room_id': room.room_id,
            'status': room.status,
            'started_at': room.started_at,
            'message': 'Room started successfully'
        })
        
    except RTCRoom.DoesNotExist:
        return Response({'error': 'Room not found'}, status=status.HTTP_404_NOT_FOUND)


@api_view(['POST'])
@permission_classes([permissions.IsAuthenticated, IsDoctorOrPatient])
def end_room(request, room_id):
    """
    End an RTC room
    """
    try:
        room = RTCRoom.objects.get(room_id=room_id)
        
        # Check permissions
        user = request.user
        if not (user == room.appointment.patient or user == room.appointment.doctor.user):
            return Response(
                {'error': 'Permission denied'}, 
                status=status.HTTP_403_FORBIDDEN
            )
        
        # Check if room can be ended
        if room.status not in ['active', 'created']:
            return Response(
                {'error': f'Room cannot be ended from status: {room.status}'}, 
                status=status.HTTP_400_BAD_REQUEST
            )
        
        # End the room
        room.status = 'ended'
        room.ended_at = timezone.now()
        room.save()
        
        return Response({
            'room_id': room.room_id,
            'status': room.status,
            'ended_at': room.ended_at,
            'message': 'Room ended successfully'
        })
        
    except RTCRoom.DoesNotExist:
        return Response({'error': 'Room not found'}, status=status.HTTP_404_NOT_FOUND)


@api_view(['GET'])
@permission_classes([permissions.IsAuthenticated, IsDoctorOrPatient])
def room_signals(request, room_id):
    """
    Get signals for a specific room
    """
    try:
        room = RTCRoom.objects.get(room_id=room_id)
        
        # Check permissions
        user = request.user
        if not (user == room.appointment.patient or user == room.appointment.doctor.user):
            return Response(
                {'error': 'Permission denied'}, 
                status=status.HTTP_403_FORBIDDEN
            )
        
        # Get signals for the room
        signals = RTCSignal.objects.filter(room=room).order_by('created_at')
        serializer = RTCSignalSerializer(signals, many=True)
        
        return Response({
            'room_id': room.room_id,
            'signals': serializer.data
        })
        
    except RTCRoom.DoesNotExist:
        return Response({'error': 'Room not found'}, status=status.HTTP_404_NOT_FOUND)


@api_view(['GET'])
@permission_classes([permissions.IsAuthenticated, IsDoctorOrPatient])
def room_status(request, room_id):
    """
    Get current status of an RTC room
    """
    try:
        room = RTCRoom.objects.get(room_id=room_id)
        
        # Check permissions
        user = request.user
        if not (user == room.appointment.patient or user == room.appointment.doctor.user):
            return Response(
                {'error': 'Permission denied'}, 
                status=status.HTTP_403_FORBIDDEN
            )
        
        # Check if room has expired
        if room.expires_at < timezone.now() and room.status != 'ended':
            room.status = 'expired'
            room.save()
        
        return Response({
            'room_id': room.room_id,
            'status': room.status,
            'created_at': room.created_at,
            'started_at': room.started_at,
            'ended_at': room.ended_at,
            'expires_at': room.expires_at,
            'max_participants': room.max_participants,
            'recording_enabled': room.recording_enabled
        })
        
    except RTCRoom.DoesNotExist:
        return Response({'error': 'Room not found'}, status=status.HTTP_404_NOT_FOUND)
