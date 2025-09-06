#!/usr/bin/env python3
"""
Email Configuration Test Script
This script tests if your Gmail SMTP configuration is working correctly.
"""

import os
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from dotenv import load_dotenv

def test_email_config():
    """Test email configuration by sending a test email."""
    
    # Load environment variables
    load_dotenv()
    
    # Get email configuration from environment
    email_host = os.getenv('EMAIL_HOST')
    email_port = int(os.getenv('EMAIL_PORT', 587))
    email_user = os.getenv('EMAIL_HOST_USER')
    email_password = os.getenv('EMAIL_HOST_PASSWORD')
    email_use_tls = os.getenv('EMAIL_USE_TLS', 'True').lower() == 'true'
    
    print("🔧 Email Configuration Test")
    print("=" * 40)
    print(f"Host: {email_host}")
    print(f"Port: {email_port}")
    print(f"User: {email_user}")
    print(f"Use TLS: {email_use_tls}")
    print(f"Password: {'*' * len(email_password) if email_password else 'NOT SET'}")
    print("=" * 40)
    
    # Check if all required fields are set
    if not all([email_host, email_user, email_password]):
        print("❌ Missing required email configuration!")
        print("Please check your .env file and ensure all email settings are configured.")
        return False
    
    try:
        # Create SMTP connection
        print("📧 Connecting to Gmail SMTP server...")
        server = smtplib.SMTP(email_host, email_port)
        
        if email_use_tls:
            print("🔒 Starting TLS encryption...")
            server.starttls()
        
        print("🔐 Authenticating with Gmail...")
        server.login(email_user, email_password)
        
        # Create test email
        msg = MIMEMultipart()
        msg['From'] = email_user
        msg['To'] = email_user  # Send to yourself for testing
        msg['Subject'] = "Healthcare Platform - Email Test"
        
        body = """
        🎉 Congratulations! Your email configuration is working correctly.
        
        This is a test email from your Healthcare Platform application.
        
        Your Gmail SMTP setup is ready for sending notifications!
        
        Best regards,
        Healthcare Platform Team
        """
        
        msg.attach(MIMEText(body, 'plain'))
        
        # Send email
        print("📤 Sending test email...")
        text = msg.as_string()
        server.sendmail(email_user, email_user, text)
        
        # Close connection
        server.quit()
        
        print("✅ SUCCESS! Email configuration is working correctly!")
        print(f"📬 Test email sent to: {email_user}")
        print("Check your inbox for the test email.")
        
        return True
        
    except smtplib.SMTPAuthenticationError as e:
        print("❌ Authentication failed!")
        print("This usually means:")
        print("1. Your Gmail app password is incorrect")
        print("2. 2-Factor Authentication is not enabled")
        print("3. App password was not generated correctly")
        print(f"Error: {e}")
        return False
        
    except smtplib.SMTPException as e:
        print("❌ SMTP Error occurred!")
        print(f"Error: {e}")
        return False
        
    except Exception as e:
        print("❌ Unexpected error occurred!")
        print(f"Error: {e}")
        return False

if __name__ == "__main__":
    test_email_config()
