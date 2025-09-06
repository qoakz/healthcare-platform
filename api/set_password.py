#!/usr/bin/env python3
"""
Set Gmail App Password in .env file
"""

def set_password():
    """Set the Gmail App Password in .env file."""
    
    app_password = "sbxnvacjqadjbnvg"  # Your app password without spaces
    
    print("🔑 Setting Gmail App Password...")
    print(f"Password: {app_password}")
    
    # Read the .env file
    with open('.env', 'r') as f:
        content = f.read()
    
    # Update the password
    if 'EMAIL_HOST_PASSWORD=' in content:
        # Find and replace the password line
        lines = content.split('\n')
        for i, line in enumerate(lines):
            if line.startswith('EMAIL_HOST_PASSWORD='):
                lines[i] = f'EMAIL_HOST_PASSWORD={app_password}'
                break
        
        # Write back to file
        with open('.env', 'w') as f:
            f.write('\n'.join(lines))
        
        print("✅ App Password updated successfully!")
        return True
    else:
        print("❌ Could not find EMAIL_HOST_PASSWORD in .env file")
        return False

if __name__ == "__main__":
    set_password()
