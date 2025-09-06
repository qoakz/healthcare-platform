#!/usr/bin/env python
"""
Update email password in .env file
"""
import os

# Read current .env file
env_file = '.env'
if os.path.exists(env_file):
    with open(env_file, 'r') as f:
        lines = f.readlines()
else:
    lines = []

# Update or add email settings
email_settings = {
    'EMAIL_HOST_USER': 'kom647579@gmail.com',
    'EMAIL_HOST_PASSWORD': 'qzlo gtdv dtza aqbu',
    'DEFAULT_FROM_EMAIL': 'kom647579@gmail.com'
}

# Update existing lines or add new ones
updated_lines = []
email_keys_found = set()

for line in lines:
    line = line.strip()
    if '=' in line:
        key = line.split('=')[0].strip()
        if key in email_settings:
            updated_lines.append(f"{key}={email_settings[key]}\n")
            email_keys_found.add(key)
        else:
            updated_lines.append(line + '\n')
    else:
        updated_lines.append(line + '\n')

# Add any missing email settings
for key, value in email_settings.items():
    if key not in email_keys_found:
        updated_lines.append(f"{key}={value}\n")

# Write updated .env file
with open(env_file, 'w') as f:
    f.writelines(updated_lines)

print("✅ Email settings updated successfully!")
print("📧 EMAIL_HOST_USER: kom647579@gmail.com")
print("🔑 EMAIL_HOST_PASSWORD: qzlo gtdv dtza aqbu")
print("📤 DEFAULT_FROM_EMAIL: kom647579@gmail.com")

