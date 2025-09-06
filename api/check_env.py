#!/usr/bin/env python3
"""
Environment Variables Checker
This script helps verify your .env file configuration.
"""

import os
from dotenv import load_dotenv

def check_env_vars():
    """Check environment variables from .env file."""
    
    # Load environment variables
    load_dotenv()
    
    print("🔍 Environment Variables Check")
    print("=" * 50)
    
    # Check email configuration
    email_vars = {
        'EMAIL_HOST': os.getenv('EMAIL_HOST'),
        'EMAIL_PORT': os.getenv('EMAIL_PORT'),
        'EMAIL_USE_TLS': os.getenv('EMAIL_USE_TLS'),
        'EMAIL_HOST_USER': os.getenv('EMAIL_HOST_USER'),
        'EMAIL_HOST_PASSWORD': os.getenv('EMAIL_HOST_PASSWORD'),
    }
    
    print("📧 Email Configuration:")
    for key, value in email_vars.items():
        if key == 'EMAIL_HOST_PASSWORD':
            display_value = '*' * len(value) if value else 'NOT SET'
        else:
            display_value = value if value else 'NOT SET'
        print(f"  {key}: {display_value}")
    
    print("\n" + "=" * 50)
    
    # Check for common issues
    issues = []
    
    if not email_vars['EMAIL_HOST_USER'] or email_vars['EMAIL_HOST_USER'] == 'your-email@gmail.com':
        issues.append("❌ EMAIL_HOST_USER is not set or still has placeholder value")
    
    if not email_vars['EMAIL_HOST_PASSWORD'] or email_vars['EMAIL_HOST_PASSWORD'] == 'your-gmail-app-password-here':
        issues.append("❌ EMAIL_HOST_PASSWORD is not set or still has placeholder value")
    
    if email_vars['EMAIL_HOST_USER'] and '@gmail.com' not in email_vars['EMAIL_HOST_USER']:
        issues.append("⚠️  EMAIL_HOST_USER doesn't look like a Gmail address")
    
    if email_vars['EMAIL_HOST_PASSWORD'] and len(email_vars['EMAIL_HOST_PASSWORD']) != 16:
        issues.append("⚠️  EMAIL_HOST_PASSWORD should be exactly 16 characters")
    
    if issues:
        print("🚨 Issues Found:")
        for issue in issues:
            print(f"  {issue}")
    else:
        print("✅ Email configuration looks good!")
    
    print("\n" + "=" * 50)
    print("📝 Next Steps:")
    print("1. Make sure 2-Factor Authentication is enabled on your Google account")
    print("2. Generate a new App Password from Google Account settings")
    print("3. Update your .env file with the correct values")
    print("4. Run the email test again")

if __name__ == "__main__":
    check_env_vars()
