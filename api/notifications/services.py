"""
Notification services for email and SMS
"""
import logging
from typing import Optional, Dict, Any
from django.conf import settings
from django.core.mail import send_mail, EmailMultiAlternatives
from django.template.loader import render_to_string
from django.utils.html import strip_tags
from twilio.rest import Client as TwilioClient
from sendgrid import SendGridAPIClient
from sendgrid.helpers.mail import Mail
from celery import shared_task

logger = logging.getLogger(__name__)

class EmailService:
    """Email notification service using Gmail SMTP and SendGrid"""
    
    @staticmethod
    def send_simple_email(
        to_email: str,
        subject: str,
        message: str,
        from_email: Optional[str] = None
    ) -> bool:
        """Send a simple text email"""
        try:
            from_email = from_email or settings.DEFAULT_FROM_EMAIL
            send_mail(
                subject=subject,
                message=message,
                from_email=from_email,
                recipient_list=[to_email],
                fail_silently=False,
            )
            logger.info(f"Email sent successfully to {to_email}")
            return True
        except Exception as e:
            logger.error(f"Failed to send email to {to_email}: {str(e)}")
            return False
    
    @staticmethod
    def send_html_email(
        to_email: str,
        subject: str,
        html_content: str,
        text_content: Optional[str] = None,
        from_email: Optional[str] = None
    ) -> bool:
        """Send an HTML email with text fallback"""
        try:
            from_email = from_email or settings.DEFAULT_FROM_EMAIL
            
            msg = EmailMultiAlternatives(
                subject=subject,
                body=text_content or strip_tags(html_content),
                from_email=from_email,
                to=[to_email]
            )
            msg.attach_alternative(html_content, "text/html")
            msg.send()
            
            logger.info(f"HTML email sent successfully to {to_email}")
            return True
        except Exception as e:
            logger.error(f"Failed to send HTML email to {to_email}: {str(e)}")
            return False
    
    @staticmethod
    def send_template_email(
        to_email: str,
        subject: str,
        template_name: str,
        context: Dict[str, Any],
        from_email: Optional[str] = None
    ) -> bool:
        """Send email using Django template"""
        try:
            from_email = from_email or settings.DEFAULT_FROM_EMAIL
            
            # Render HTML template
            html_content = render_to_string(f'emails/{template_name}.html', context)
            text_content = render_to_string(f'emails/{template_name}.txt', context)
            
            return EmailService.send_html_email(
                to_email=to_email,
                subject=subject,
                html_content=html_content,
                text_content=text_content,
                from_email=from_email
            )
        except Exception as e:
            logger.error(f"Failed to send template email to {to_email}: {str(e)}")
            return False

class SMSService:
    """SMS notification service using Twilio"""
    
    @staticmethod
    def send_sms(
        to_phone: str,
        message: str,
        from_phone: Optional[str] = None
    ) -> bool:
        """Send SMS using Twilio"""
        try:
            if not settings.TWILIO_ACCOUNT_SID or not settings.TWILIO_AUTH_TOKEN:
                logger.warning("Twilio credentials not configured")
                return False
            
            client = TwilioClient(settings.TWILIO_ACCOUNT_SID, settings.TWILIO_AUTH_TOKEN)
            from_phone = from_phone or settings.TWILIO_PHONE_NUMBER
            
            message_obj = client.messages.create(
                body=message,
                from_=from_phone,
                to=to_phone
            )
            
            logger.info(f"SMS sent successfully to {to_phone}, SID: {message_obj.sid}")
            return True
        except Exception as e:
            logger.error(f"Failed to send SMS to {to_phone}: {str(e)}")
            return False

class SendGridService:
    """Email service using SendGrid API"""
    
    @staticmethod
    def send_email(
        to_email: str,
        subject: str,
        html_content: str,
        text_content: Optional[str] = None,
        from_email: Optional[str] = None
    ) -> bool:
        """Send email using SendGrid API"""
        try:
            if not settings.SENDGRID_API_KEY:
                logger.warning("SendGrid API key not configured")
                return False
            
            from_email = from_email or settings.SENDGRID_FROM_EMAIL
            
            message = Mail(
                from_email=from_email,
                to_emails=to_email,
                subject=subject,
                html_content=html_content,
                plain_text_content=text_content or strip_tags(html_content)
            )
            
            sg = SendGridAPIClient(api_key=settings.SENDGRID_API_KEY)
            response = sg.send(message)
            
            if response.status_code in [200, 201, 202]:
                logger.info(f"SendGrid email sent successfully to {to_email}")
                return True
            else:
                logger.error(f"SendGrid email failed: {response.status_code}")
                return False
        except Exception as e:
            logger.error(f"Failed to send SendGrid email to {to_email}: {str(e)}")
            return False

# Celery Tasks
@shared_task
def send_appointment_reminder_email(appointment_id: int):
    """Send appointment reminder email"""
    from .models import Notification
    from appointments.models import Appointment
    
    try:
        appointment = Appointment.objects.get(id=appointment_id)
        
        # Create notification record
        notification = Notification.objects.create(
            user=appointment.patient,
            type='appointment_reminder',
            title='Appointment Reminder',
            message=f'Your appointment with Dr. {appointment.doctor.user.get_full_name()} is scheduled for {appointment.scheduled_at.strftime("%B %d, %Y at %I:%M %p")}',
            channel='email',
            status='pending'
        )
        
        # Send email
        context = {
            'patient_name': appointment.patient.user.get_full_name(),
            'doctor_name': appointment.doctor.user.get_full_name(),
            'appointment_date': appointment.scheduled_at.strftime("%B %d, %Y"),
            'appointment_time': appointment.scheduled_at.strftime("%I:%M %p"),
            'appointment_type': appointment.appointment_type,
            'meeting_link': appointment.meeting_link or 'N/A'
        }
        
        success = EmailService.send_template_email(
            to_email=appointment.patient.user.email,
            subject='Appointment Reminder - Healthcare Platform',
            template_name='appointment_reminder',
            context=context
        )
        
        notification.status = 'sent' if success else 'failed'
        notification.save()
        
        return success
    except Exception as e:
        logger.error(f"Failed to send appointment reminder email: {str(e)}")
        return False

@shared_task
def send_appointment_reminder_sms(appointment_id: int):
    """Send appointment reminder SMS"""
    from .models import Notification
    from appointments.models import Appointment
    
    try:
        appointment = Appointment.objects.get(id=appointment_id)
        
        # Create notification record
        notification = Notification.objects.create(
            user=appointment.patient,
            type='appointment_reminder',
            title='Appointment Reminder',
            message=f'Reminder: Your appointment with Dr. {appointment.doctor.user.get_full_name()} is on {appointment.scheduled_at.strftime("%B %d at %I:%M %p")}',
            channel='sms',
            status='pending'
        )
        
        # Send SMS
        message = f"Hi {appointment.patient.user.first_name}, your appointment with Dr. {appointment.doctor.user.get_full_name()} is scheduled for {appointment.scheduled_at.strftime('%B %d, %Y at %I:%M %p')}. Meeting link: {appointment.meeting_link or 'Will be provided soon'}"
        
        success = SMSService.send_sms(
            to_phone=appointment.patient.phone_number,
            message=message
        )
        
        notification.status = 'sent' if success else 'failed'
        notification.save()
        
        return success
    except Exception as e:
        logger.error(f"Failed to send appointment reminder SMS: {str(e)}")
        return False

@shared_task
def send_payment_confirmation_email(payment_id: int):
    """Send payment confirmation email"""
    from .models import Notification
    from payments.models import PaymentTransaction
    
    try:
        payment = PaymentTransaction.objects.get(id=payment_id)
        
        # Create notification record
        notification = Notification.objects.create(
            user=payment.patient,
            type='payment_confirmation',
            title='Payment Confirmation',
            message=f'Your payment of ${payment.amount} has been processed successfully',
            channel='email',
            status='pending'
        )
        
        # Send email
        context = {
            'patient_name': payment.patient.user.get_full_name(),
            'amount': payment.amount,
            'transaction_id': payment.transaction_id,
            'appointment_date': payment.appointment.scheduled_at.strftime("%B %d, %Y") if payment.appointment else 'N/A',
            'doctor_name': payment.appointment.doctor.user.get_full_name() if payment.appointment else 'N/A'
        }
        
        success = EmailService.send_template_email(
            to_email=payment.patient.user.email,
            subject='Payment Confirmation - Healthcare Platform',
            template_name='payment_confirmation',
            context=context
        )
        
        notification.status = 'sent' if success else 'failed'
        notification.save()
        
        return success
    except Exception as e:
        logger.error(f"Failed to send payment confirmation email: {str(e)}")
        return False

@shared_task
def send_doctor_notification_email(doctor_id: int, notification_type: str, data: Dict[str, Any]):
    """Send notification email to doctor"""
    from .models import Notification
    from doctors.models import Doctor
    
    try:
        doctor = Doctor.objects.get(id=doctor_id)
        
        # Create notification record
        notification = Notification.objects.create(
            user=doctor.user,
            type=notification_type,
            title=data.get('title', 'New Notification'),
            message=data.get('message', ''),
            channel='email',
            status='pending'
        )
        
        # Send email
        context = {
            'doctor_name': doctor.user.get_full_name(),
            **data
        }
        
        success = EmailService.send_template_email(
            to_email=doctor.user.email,
            subject=data.get('subject', 'Healthcare Platform Notification'),
            template_name=f'doctor_{notification_type}',
            context=context
        )
        
        notification.status = 'sent' if success else 'failed'
        notification.save()
        
        return success
    except Exception as e:
        logger.error(f"Failed to send doctor notification email: {str(e)}")
        return False

