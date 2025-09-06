#!/usr/bin/env python3
"""
Simple script to update Gmail App Password in .env file
"""

import os

def update_password():
    """Update the Gmail App Password in .env file."""
    
    print("🔑 Gmail App Password Updater")
    print("=" * 40)
    print("Enter your 16-character Gmail App Password:")
    print("(The one you just generated from Google Account settings)")
    print()
    
    app_password = input("App Password: ").strip()
    
    if len(app_password) != 16:
        print("❌ Error: App Password should be exactly 16 characters")
        return False
    
    # Read the .env file
    with open('.env', 'r') as f:
        content = f.read()
    
    # Update the password
    if 'EMAIL_HOST_PASSWORD=' in content:
        # Find the line and replace it
        lines = content.split('\n')
        for i, line in enumerate(lines):
            if line.startswith('EMAIL_HOST_PASSWORD='):
                lines[i] = f'EMAIL_HOST_PASSWORD={app_password}'
                break
        
        # Write back to file
        with open('.env', 'w') as f:
            f.write('\n'.join(lines))
        
        print("✅ App Password updated successfully!")
        print("Now let's test the email configuration...")
        return True
    else:
        print("❌ Could not find EMAIL_HOST_PASSWORD in .env file")
        return False

if __name__ == "__main__":
    update_password()
