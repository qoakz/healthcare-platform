from rest_framework import generics, status, permissions, filters
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from django_filters.rest_framework import DjangoFilterBackend
from django.utils import timezone
from .models import Notification
from .serializers import NotificationSerializer, NotificationCreateSerializer, NotificationListSerializer
from .services import (
    send_appointment_reminder_email,
    send_appointment_reminder_sms,
    send_payment_confirmation_email,
    send_doctor_notification_email
)
from users.permissions import IsAdmin


class NotificationListView(generics.ListCreateAPIView):
    """
    List and create notifications
    """
    permission_classes = [permissions.IsAuthenticated]
    filter_backends = [DjangoFilterBackend, filters.OrderingFilter]
    filterset_fields = ['notification_type', 'channel', 'status']
    ordering_fields = ['created_at', 'scheduled_at']
    ordering = ['-created_at']
    
    def get_serializer_class(self):
        if self.request.method == 'POST':
            return NotificationCreateSerializer
        return NotificationListSerializer
    
    def get_queryset(self):
        user = self.request.user
        if user.is_staff:
            return Notification.objects.all()
        return Notification.objects.filter(user=user)


class NotificationDetailView(generics.RetrieveUpdateDestroyAPIView):
    """
    Get, update and delete notification details
    """
    serializer_class = NotificationSerializer
    permission_classes = [permissions.IsAuthenticated]
    
    def get_queryset(self):
        user = self.request.user
        if user.is_staff:
            return Notification.objects.all()
        return Notification.objects.filter(user=user)


@api_view(['GET'])
@permission_classes([permissions.IsAuthenticated])
def unread_notifications(request):
    """
    Get unread notifications for the current user
    """
    user = request.user
    unread_count = Notification.objects.filter(
        user=user,
        read_at__isnull=True
    ).count()
    
    recent_unread = Notification.objects.filter(
        user=user,
        read_at__isnull=True
    ).order_by('-created_at')[:10]
    
    serializer = NotificationListSerializer(recent_unread, many=True)
    
    return Response({
        'unread_count': unread_count,
        'notifications': serializer.data
    })


@api_view(['POST'])
@permission_classes([permissions.IsAuthenticated])
def mark_notification_read(request, notification_id):
    """
    Mark a notification as read
    """
    try:
        notification = Notification.objects.get(
            id=notification_id,
            user=request.user
        )
        
        if not notification.read_at:
            notification.read_at = timezone.now()
            notification.status = 'read'
            notification.save()
        
        return Response({
            'message': 'Notification marked as read'
        })
        
    except Notification.DoesNotExist:
        return Response(
            {'error': 'Notification not found'}, 
            status=status.HTTP_404_NOT_FOUND
        )


@api_view(['POST'])
@permission_classes([permissions.IsAuthenticated])
def mark_all_notifications_read(request):
    """
    Mark all notifications as read for the current user
    """
    user = request.user
    updated_count = Notification.objects.filter(
        user=user,
        read_at__isnull=True
    ).update(
        read_at=timezone.now(),
        status='read'
    )
    
    return Response({
        'message': f'{updated_count} notifications marked as read'
    })


@api_view(['POST'])
@permission_classes([permissions.IsAuthenticated, IsAdmin])
def send_notification(request):
    """
    Send a notification to a user (admin only)
    """
    user_id = request.data.get('user_id')
    notification_type = request.data.get('notification_type')
    channel = request.data.get('channel', 'in_app')
    title = request.data.get('title')
    message = request.data.get('message')
    metadata = request.data.get('metadata', {})
    
    if not all([user_id, notification_type, title, message]):
        return Response(
            {'error': 'user_id, notification_type, title, and message are required'}, 
            status=status.HTTP_400_BAD_REQUEST
        )
    
    try:
        from users.models import User
        user = User.objects.get(id=user_id)
        
        notification = Notification.objects.create(
            user=user,
            notification_type=notification_type,
            channel=channel,
            title=title,
            message=message,
            metadata=metadata
        )
        
        # TODO: Send notification via the specified channel
        # This would integrate with email/SMS/push notification services
        
        return Response({
            'notification_id': notification.id,
            'message': 'Notification sent successfully'
        })
        
    except User.DoesNotExist:
        return Response({'error': 'User not found'}, status=status.HTTP_404_NOT_FOUND)


@api_view(['POST'])
@permission_classes([permissions.IsAuthenticated, IsAdmin])
def send_bulk_notification(request):
    """
    Send a notification to multiple users (admin only)
    """
    user_ids = request.data.get('user_ids', [])
    notification_type = request.data.get('notification_type')
    channel = request.data.get('channel', 'in_app')
    title = request.data.get('title')
    message = request.data.get('message')
    metadata = request.data.get('metadata', {})
    
    if not all([user_ids, notification_type, title, message]):
        return Response(
            {'error': 'user_ids, notification_type, title, and message are required'}, 
            status=status.HTTP_400_BAD_REQUEST
        )
    
    try:
        from users.models import User
        users = User.objects.filter(id__in=user_ids)
        
        notifications = []
        for user in users:
            notification = Notification.objects.create(
                user=user,
                notification_type=notification_type,
                channel=channel,
                title=title,
                message=message,
                metadata=metadata
            )
            notifications.append(notification)
        
        # TODO: Send notifications via the specified channel
        # This would integrate with email/SMS/push notification services
        
        return Response({
            'notifications_sent': len(notifications),
            'message': 'Bulk notification sent successfully'
        })
        
    except Exception as e:
        return Response(
            {'error': str(e)}, 
            status=status.HTTP_400_BAD_REQUEST
        )


@api_view(['GET'])
@permission_classes([permissions.IsAuthenticated, IsAdmin])
def notification_stats(request):
    """
    Get notification statistics (admin only)
    """
    total_notifications = Notification.objects.count()
    unread_notifications = Notification.objects.filter(read_at__isnull=True).count()
    
    # Notifications by type
    by_type = {}
    for choice in Notification.TYPE_CHOICES:
        count = Notification.objects.filter(notification_type=choice[0]).count()
        by_type[choice[0]] = count
    
    # Notifications by channel
    by_channel = {}
    for choice in Notification.CHANNEL_CHOICES:
        count = Notification.objects.filter(channel=choice[0]).count()
        by_channel[choice[0]] = count
    
    # Notifications by status
    by_status = {}
    for choice in Notification.STATUS_CHOICES:
        count = Notification.objects.filter(status=choice[0]).count()
        by_status[choice[0]] = count
    
    return Response({
        'total_notifications': total_notifications,
        'unread_notifications': unread_notifications,
        'by_type': by_type,
        'by_channel': by_channel,
        'by_status': by_status
    })


@api_view(['POST'])
@permission_classes([permissions.IsAuthenticated])
def send_appointment_reminder(request):
    """
    Send appointment reminder via email and SMS
    """
    appointment_id = request.data.get('appointment_id')
    channels = request.data.get('channels', ['email', 'sms'])
    
    if not appointment_id:
        return Response(
            {'error': 'appointment_id is required'}, 
            status=status.HTTP_400_BAD_REQUEST
        )
    
    results = {}
    
    if 'email' in channels:
        task = send_appointment_reminder_email.delay(appointment_id)
        results['email'] = {'task_id': task.id, 'status': 'queued'}
    
    if 'sms' in channels:
        task = send_appointment_reminder_sms.delay(appointment_id)
        results['sms'] = {'task_id': task.id, 'status': 'queued'}
    
    return Response({
        'message': 'Appointment reminders queued successfully',
        'results': results
    })


@api_view(['POST'])
@permission_classes([permissions.IsAuthenticated])
def send_payment_confirmation(request):
    """
    Send payment confirmation email
    """
    payment_id = request.data.get('payment_id')
    
    if not payment_id:
        return Response(
            {'error': 'payment_id is required'}, 
            status=status.HTTP_400_BAD_REQUEST
        )
    
    task = send_payment_confirmation_email.delay(payment_id)
    
    return Response({
        'message': 'Payment confirmation email queued successfully',
        'task_id': task.id
    })


@api_view(['POST'])
@permission_classes([permissions.IsAuthenticated, IsAdmin])
def send_doctor_notification(request):
    """
    Send notification to doctor (admin only)
    """
    doctor_id = request.data.get('doctor_id')
    notification_type = request.data.get('notification_type')
    data = request.data.get('data', {})
    
    if not all([doctor_id, notification_type]):
        return Response(
            {'error': 'doctor_id and notification_type are required'}, 
            status=status.HTTP_400_BAD_REQUEST
        )
    
    task = send_doctor_notification_email.delay(doctor_id, notification_type, data)
    
    return Response({
        'message': 'Doctor notification queued successfully',
        'task_id': task.id
    })


@api_view(['POST'])
@permission_classes([permissions.IsAuthenticated])
def test_email_notification(request):
    """
    Test email notification (for development)
    """
    from .services import EmailService
    
    to_email = request.data.get('to_email', request.user.email)
    subject = 'Test Email - Healthcare Platform'
    message = 'This is a test email from the Healthcare Platform notification system.'
    
    success = EmailService.send_simple_email(to_email, subject, message)
    
    return Response({
        'success': success,
        'message': 'Test email sent successfully' if success else 'Failed to send test email'
    })


@api_view(['POST'])
@permission_classes([permissions.IsAuthenticated])
def test_sms_notification(request):
    """
    Test SMS notification (for development)
    """
    from .services import SMSService
    
    to_phone = request.data.get('to_phone')
    message = 'Test SMS from Healthcare Platform notification system.'
    
    if not to_phone:
        return Response(
            {'error': 'to_phone is required'}, 
            status=status.HTTP_400_BAD_REQUEST
        )
    
    success = SMSService.send_sms(to_phone, message)
    
    return Response({
        'success': success,
        'message': 'Test SMS sent successfully' if success else 'Failed to send test SMS'
    })
