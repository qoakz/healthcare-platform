#!/usr/bin/env python3
"""
Environment File Updater
This script helps update your .env file with the correct values.
"""

import os
import re

def update_env_file():
    """Update the .env file with correct values."""
    
    env_file = '.env'
    
    if not os.path.exists(env_file):
        print("❌ .env file not found!")
        return False
    
    # Read the current .env file
    with open(env_file, 'r') as f:
        content = f.read()
    
    print("🔧 Updating .env file...")
    print("=" * 50)
    
    # Update SECRET_KEY
    if 'SECRET_KEY=your-secret-key-here' in content:
        new_secret_key = 'pn0XDpCmD6Kk1nhX4py83hfZn5RRh0N8u4IZu_jZtZHoJPvXxnv8fTCc-iYZzCwRHwM'
        content = content.replace('SECRET_KEY=your-secret-key-here', f'SECRET_KEY={new_secret_key}')
        print("✅ Updated SECRET_KEY")
    
    # Update EMAIL_HOST_USER
    if 'EMAIL_HOST_USER=your-email@gmail.com' in content:
        content = content.replace('EMAIL_HOST_USER=your-email@gmail.com', 'EMAIL_HOST_USER=kom647579@gmail.com')
        print("✅ Updated EMAIL_HOST_USER to kom647579@gmail.com")
    
    # Update EMAIL_HOST_PASSWORD (ask user for input)
    if 'EMAIL_HOST_PASSWORD=your-app-password' in content:
        print("\n📧 Gmail App Password Setup")
        print("=" * 30)
        print("To get your Gmail App Password:")
        print("1. Go to https://myaccount.google.com/security")
        print("2. Enable 2-Factor Authentication if not already enabled")
        print("3. Go to https://myaccount.google.com/apppasswords")
        print("4. Select 'Mail' and 'Other device'")
        print("5. Type 'Healthcare Platform' as device name")
        print("6. Copy the 16-character password (no spaces)")
        print()
        
        app_password = input("Enter your 16-character Gmail App Password: ").strip()
        
        if len(app_password) == 16 and app_password.isalnum():
            content = content.replace('EMAIL_HOST_PASSWORD=your-app-password', f'EMAIL_HOST_PASSWORD={app_password}')
            print("✅ Updated EMAIL_HOST_PASSWORD")
        else:
            print("❌ Invalid app password format. Should be 16 alphanumeric characters.")
            return False
    
    # Write the updated content back to the file
    with open(env_file, 'w') as f:
        f.write(content)
    
    print("\n✅ .env file updated successfully!")
    print("=" * 50)
    
    return True

if __name__ == "__main__":
    update_env_file()
