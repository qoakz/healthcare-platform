#!/usr/bin/env python
"""
Simple email test script
"""
import os
import sys
import django

# Add the project directory to Python path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

# Set up Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'healthcare_platform.settings')
django.setup()

# Set email credentials directly
os.environ['EMAIL_HOST_USER'] = 'kom647579@gmail.com'
os.environ['EMAIL_HOST_PASSWORD'] = 'sbxnvacjqadjbnvg'

from django.core.mail import send_mail
from django.conf import settings

def test_email():
    """Test email sending"""
    print("🧪 Testing Email Service...")
    print(f"EMAIL_HOST_USER: {settings.EMAIL_HOST_USER}")
    print(f"EMAIL_HOST: {settings.EMAIL_HOST}")
    print(f"EMAIL_PORT: {settings.EMAIL_PORT}")
    print(f"EMAIL_USE_TLS: {settings.EMAIL_USE_TLS}")
    
    try:
        send_mail(
            subject='Test Email - Healthcare Platform',
            message='This is a test email from the Healthcare Platform notification system.',
            from_email='kom647579@gmail.com',
            recipient_list=['kom647579@gmail.com'],
            fail_silently=False,
        )
        print("✅ Email sent successfully!")
        return True
    except Exception as e:
        print(f"❌ Failed to send email: {str(e)}")
        return False

if __name__ == "__main__":
    test_email()

