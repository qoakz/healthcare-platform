from django.urls import path
from . import views

urlpatterns = [
    path('', views.NotificationListView.as_view(), name='notification-list'),
    path('<int:pk>/', views.NotificationDetailView.as_view(), name='notification-detail'),
    path('unread/', views.unread_notifications, name='unread-notifications'),
    path('<int:notification_id>/read/', views.mark_notification_read, name='mark-notification-read'),
    path('mark-all-read/', views.mark_all_notifications_read, name='mark-all-notifications-read'),
    path('send/', views.send_notification, name='send-notification'),
    path('send-bulk/', views.send_bulk_notification, name='send-bulk-notification'),
    path('stats/', views.notification_stats, name='notification-stats'),
    
    # Notification Services
    path('appointment-reminder/', views.send_appointment_reminder, name='send-appointment-reminder'),
    path('payment-confirmation/', views.send_payment_confirmation, name='send-payment-confirmation'),
    path('doctor-notification/', views.send_doctor_notification, name='send-doctor-notification'),
    
    # Test Endpoints
    path('test-email/', views.test_email_notification, name='test-email-notification'),
    path('test-sms/', views.test_sms_notification, name='test-sms-notification'),
]