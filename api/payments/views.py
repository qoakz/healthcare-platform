from rest_framework import generics, status, permissions, filters
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from django_filters.rest_framework import DjangoFilterBackend
from django.shortcuts import get_object_or_404
from .models import PaymentTransaction, Refund, DoctorPayout
from .serializers import (
    PaymentTransactionSerializer, PaymentTransactionCreateSerializer,
    RefundSerializer, RefundCreateSerializer, DoctorPayoutSerializer, DoctorPayoutCreateSerializer
)
from users.permissions import IsPatient, IsDoctor, IsAdmin


class PaymentTransactionListView(generics.ListCreateAPIView):
    """
    List and create payment transactions
    """
    permission_classes = [permissions.IsAuthenticated, IsPatient]
    filter_backends = [DjangoFilterBackend, filters.OrderingFilter]
    filterset_fields = ['status', 'provider', 'appointment']
    ordering_fields = ['created_at', 'amount']
    ordering = ['-created_at']
    
    def get_serializer_class(self):
        if self.request.method == 'POST':
            return PaymentTransactionCreateSerializer
        return PaymentTransactionSerializer
    
    def get_queryset(self):
        return PaymentTransaction.objects.filter(patient=self.request.user)


class PaymentTransactionDetailView(generics.RetrieveAPIView):
    """
    Get payment transaction details
    """
    serializer_class = PaymentTransactionSerializer
    permission_classes = [permissions.IsAuthenticated, IsPatient]
    
    def get_queryset(self):
        return PaymentTransaction.objects.filter(patient=self.request.user)


class RefundListView(generics.ListCreateAPIView):
    """
    List and create refunds
    """
    permission_classes = [permissions.IsAuthenticated, IsAdmin]
    filter_backends = [DjangoFilterBackend, filters.OrderingFilter]
    filterset_fields = ['status', 'payment__patient', 'payment__appointment']
    ordering_fields = ['created_at', 'amount']
    ordering = ['-created_at']
    
    def get_serializer_class(self):
        if self.request.method == 'POST':
            return RefundCreateSerializer
        return RefundSerializer
    
    def get_queryset(self):
        return Refund.objects.all()


class RefundDetailView(generics.RetrieveUpdateAPIView):
    """
    Get and update refund details
    """
    serializer_class = RefundSerializer
    permission_classes = [permissions.IsAuthenticated, IsAdmin]
    
    def get_queryset(self):
        return Refund.objects.all()


class DoctorPayoutListView(generics.ListCreateAPIView):
    """
    List and create doctor payouts
    """
    permission_classes = [permissions.IsAuthenticated, IsAdmin]
    filter_backends = [DjangoFilterBackend, filters.OrderingFilter]
    filterset_fields = ['status', 'doctor', 'period_start', 'period_end']
    ordering_fields = ['created_at', 'amount', 'period_start']
    ordering = ['-created_at']
    
    def get_serializer_class(self):
        if self.request.method == 'POST':
            return DoctorPayoutCreateSerializer
        return DoctorPayoutSerializer
    
    def get_queryset(self):
        return DoctorPayout.objects.all()


class DoctorPayoutDetailView(generics.RetrieveUpdateAPIView):
    """
    Get and update doctor payout details
    """
    serializer_class = DoctorPayoutSerializer
    permission_classes = [permissions.IsAuthenticated, IsAdmin]
    
    def get_queryset(self):
        return DoctorPayout.objects.all()


@api_view(['POST'])
@permission_classes([permissions.IsAuthenticated, IsPatient])
def create_payment_intent(request):
    """
    Create payment intent for an appointment
    """
    appointment_id = request.data.get('appointment_id')
    provider = request.data.get('provider', 'stripe')
    
    if not appointment_id:
        return Response(
            {'error': 'appointment_id is required'}, 
            status=status.HTTP_400_BAD_REQUEST
        )
    
    try:
        from appointments.models import Appointment
        appointment = Appointment.objects.get(id=appointment_id, patient=request.user)
        
        # Check if payment already exists
        existing_payment = PaymentTransaction.objects.filter(
            appointment=appointment,
            status__in=['pending', 'processing', 'completed']
        ).first()
        
        if existing_payment:
            return Response({
                'payment_id': existing_payment.id,
                'client_secret': existing_payment.client_secret,
                'status': existing_payment.status
            })
        
        # Create new payment transaction
        payment = PaymentTransaction.objects.create(
            appointment=appointment,
            patient=request.user,
            provider=provider,
            amount=appointment.consultation_fee,
            currency='USD',
            description=f"Consultation fee for appointment with Dr. {appointment.doctor.full_name}"
        )
        
        # TODO: Create payment intent with external provider (Stripe/Razorpay)
        # This would integrate with the actual payment provider API
        
        return Response({
            'payment_id': payment.id,
            'client_secret': payment.client_secret,
            'amount': payment.amount,
            'currency': payment.currency
        })
        
    except Appointment.DoesNotExist:
        return Response({'error': 'Appointment not found'}, status=status.HTTP_404_NOT_FOUND)


@api_view(['POST'])
@permission_classes([permissions.AllowAny])
def payment_webhook(request):
    """
    Handle payment webhooks from external providers
    """
    provider = request.data.get('provider')
    
    if provider == 'stripe':
        # TODO: Verify Stripe webhook signature
        # TODO: Handle Stripe webhook events
        pass
    elif provider == 'razorpay':
        # TODO: Verify Razorpay webhook signature
        # TODO: Handle Razorpay webhook events
        pass
    
    # Update payment status based on webhook data
    external_id = request.data.get('external_id')
    if external_id:
        try:
            payment = PaymentTransaction.objects.get(external_id=external_id)
            payment.status = request.data.get('status', payment.status)
            payment.save()
            
            # Update appointment payment status
            if payment.appointment:
                payment.appointment.payment_status = payment.status
                payment.appointment.save()
                
        except PaymentTransaction.DoesNotExist:
            pass
    
    return Response({'status': 'success'})


@api_view(['POST'])
@permission_classes([permissions.IsAuthenticated, IsAdmin])
def process_refund(request, payment_id):
    """
    Process a refund for a payment
    """
    try:
        payment = PaymentTransaction.objects.get(id=payment_id)
        
        if payment.status != 'completed':
            return Response(
                {'error': 'Only completed payments can be refunded'}, 
                status=status.HTTP_400_BAD_REQUEST
            )
        
        refund_amount = request.data.get('amount', payment.amount)
        refund_reason = request.data.get('reason', '')
        
        # Create refund
        refund = Refund.objects.create(
            payment=payment,
            amount=refund_amount,
            reason=refund_reason,
            processed_by=request.user
        )
        
        # TODO: Process refund with external provider
        # This would integrate with the actual payment provider API
        
        return Response({
            'refund_id': refund.id,
            'amount': refund.amount,
            'status': refund.status
        })
        
    except PaymentTransaction.DoesNotExist:
        return Response({'error': 'Payment not found'}, status=status.HTTP_404_NOT_FOUND)


@api_view(['GET'])
@permission_classes([permissions.IsAuthenticated, IsDoctor])
def doctor_earnings(request):
    """
    Get doctor's earnings summary
    """
    doctor = request.user.doctor_profile
    
    # Get completed appointments
    from appointments.models import Appointment
    completed_appointments = Appointment.objects.filter(
        doctor=doctor,
        status='completed',
        payment_status='completed'
    )
    
    # Calculate total earnings
    total_earnings = sum(app.consultation_fee for app in completed_appointments)
    
    # Get recent payouts
    recent_payouts = DoctorPayout.objects.filter(doctor=doctor).order_by('-created_at')[:5]
    payouts_serializer = DoctorPayoutSerializer(recent_payouts, many=True)
    
    return Response({
        'total_earnings': total_earnings,
        'completed_appointments': completed_appointments.count(),
        'recent_payouts': payouts_serializer.data
    })


@api_view(['POST'])
@permission_classes([permissions.IsAuthenticated, IsAdmin])
def generate_doctor_payout(request):
    """
    Generate payout for a doctor for a specific period
    """
    doctor_id = request.data.get('doctor_id')
    period_start = request.data.get('period_start')
    period_end = request.data.get('period_end')
    
    if not all([doctor_id, period_start, period_end]):
        return Response(
            {'error': 'doctor_id, period_start, and period_end are required'}, 
            status=status.HTTP_400_BAD_REQUEST
        )
    
    try:
        from doctors.models import Doctor
        from appointments.models import Appointment
        from datetime import datetime
        
        doctor = Doctor.objects.get(id=doctor_id)
        
        # Get completed appointments in the period
        appointments = Appointment.objects.filter(
            doctor=doctor,
            status='completed',
            payment_status='completed',
            scheduled_at__date__range=[period_start, period_end]
        )
        
        if not appointments.exists():
            return Response(
                {'error': 'No completed appointments found for the period'}, 
                status=status.HTTP_400_BAD_REQUEST
            )
        
        # Calculate payout amount (assuming 80% goes to doctor, 20% to platform)
        total_amount = sum(app.consultation_fee for app in appointments)
        payout_amount = total_amount * 0.8  # 80% to doctor
        
        # Create payout
        payout = DoctorPayout.objects.create(
            doctor=doctor,
            amount=payout_amount,
            period_start=period_start,
            period_end=period_end
        )
        
        # Add appointments to payout
        payout.appointments.set(appointments)
        
        return Response({
            'payout_id': payout.id,
            'amount': payout.amount,
            'appointments_count': appointments.count(),
            'period_start': period_start,
            'period_end': period_end
        })
        
    except Doctor.DoesNotExist:
        return Response({'error': 'Doctor not found'}, status=status.HTTP_404_NOT_FOUND)
