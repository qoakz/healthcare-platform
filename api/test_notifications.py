#!/usr/bin/env python
"""
Test script for email and SMS notifications
"""
import os
import sys
import django

# Add the project directory to Python path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

# Set up Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'healthcare_platform.settings')
django.setup()

from notifications.services import EmailService, SMSService, SendGridService

def test_email():
    """Test email sending"""
    print("🧪 Testing Email Service...")
    
    # Test simple email
    success = EmailService.send_simple_email(
        to_email="kom647579@gmail.com",
        subject="Test Email - Healthcare Platform",
        message="This is a test email from the Healthcare Platform notification system."
    )
    
    if success:
        print("✅ Email sent successfully!")
    else:
        print("❌ Failed to send email")
    
    return success

def test_sms():
    """Test SMS sending (requires Twilio credentials)"""
    print("\n🧪 Testing SMS Service...")
    
    # Check if Twilio is configured
    from django.conf import settings
    if not settings.TWILIO_ACCOUNT_SID or not settings.TWILIO_AUTH_TOKEN:
        print("⚠️  Twilio credentials not configured. Skipping SMS test.")
        return False
    
    # Test SMS (replace with your phone number)
    phone_number = input("Enter your phone number for SMS test (e.g., +1234567890): ")
    if not phone_number:
        print("❌ No phone number provided. Skipping SMS test.")
        return False
    
    success = SMSService.send_sms(
        to_phone=phone_number,
        message="Test SMS from Healthcare Platform notification system."
    )
    
    if success:
        print("✅ SMS sent successfully!")
    else:
        print("❌ Failed to send SMS")
    
    return success

def test_sendgrid():
    """Test SendGrid email service"""
    print("\n🧪 Testing SendGrid Service...")
    
    # Check if SendGrid is configured
    from django.conf import settings
    if not settings.SENDGRID_API_KEY:
        print("⚠️  SendGrid API key not configured. Skipping SendGrid test.")
        return False
    
    success = SendGridService.send_email(
        to_email="kom647579@gmail.com",
        subject="Test SendGrid Email - Healthcare Platform",
        html_content="<h1>Test Email</h1><p>This is a test email from SendGrid.</p>",
        text_content="Test Email - This is a test email from SendGrid."
    )
    
    if success:
        print("✅ SendGrid email sent successfully!")
    else:
        print("❌ Failed to send SendGrid email")
    
    return success

def test_celery_tasks():
    """Test Celery tasks"""
    print("\n🧪 Testing Celery Tasks...")
    
    try:
        from notifications.services import send_appointment_reminder_email
        from appointments.models import Appointment
        
        # Get first appointment if exists
        appointment = Appointment.objects.first()
        if appointment:
            print(f"Testing with appointment ID: {appointment.id}")
            task = send_appointment_reminder_email.delay(appointment.id)
            print(f"✅ Celery task queued successfully! Task ID: {task.id}")
            return True
        else:
            print("⚠️  No appointments found. Create an appointment first.")
            return False
    except Exception as e:
        print(f"❌ Failed to test Celery tasks: {str(e)}")
        return False

def main():
    """Run all tests"""
    print("🚀 Starting Notification System Tests...\n")
    
    results = {
        'email': test_email(),
        'sms': test_sms(),
        'sendgrid': test_sendgrid(),
        'celery': test_celery_tasks()
    }
    
    print("\n📊 Test Results:")
    print("=" * 50)
    for service, success in results.items():
        status = "✅ PASS" if success else "❌ FAIL"
        print(f"{service.upper()}: {status}")
    
    total_tests = len(results)
    passed_tests = sum(results.values())
    
    print(f"\n🎯 Summary: {passed_tests}/{total_tests} tests passed")
    
    if passed_tests == total_tests:
        print("🎉 All tests passed! Notification system is working correctly.")
    else:
        print("⚠️  Some tests failed. Check the configuration and try again.")

if __name__ == "__main__":
    main()

