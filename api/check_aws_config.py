#!/usr/bin/env python3
"""
Check AWS configuration in .env file
"""

import os
from dotenv import load_dotenv

def check_aws_config():
    """Check AWS configuration from .env file."""
    
    # Load environment variables
    load_dotenv()
    
    print("🔍 AWS Configuration Check")
    print("=" * 50)
    
    # Check AWS Cognito
    print("📱 AWS Cognito Configuration:")
    cognito_vars = {
        'AWS_COGNITO_USER_POOL_ID': os.getenv('AWS_COGNITO_USER_POOL_ID'),
        'AWS_COGNITO_CLIENT_ID': os.getenv('AWS_COGNITO_CLIENT_ID'),
        'AWS_COGNITO_REGION': os.getenv('AWS_COGNITO_REGION'),
    }
    
    for key, value in cognito_vars.items():
        display_value = value if value else 'NOT SET'
        print(f"  {key}: {display_value}")
    
    # Check AWS S3
    print("\n🪣 AWS S3 Configuration:")
    s3_vars = {
        'AWS_ACCESS_KEY_ID': os.getenv('AWS_ACCESS_KEY_ID'),
        'AWS_SECRET_ACCESS_KEY': os.getenv('AWS_SECRET_ACCESS_KEY'),
        'AWS_STORAGE_BUCKET_NAME': os.getenv('AWS_STORAGE_BUCKET_NAME'),
        'AWS_S3_REGION_NAME': os.getenv('AWS_S3_REGION_NAME'),
    }
    
    for key, value in s3_vars.items():
        if key == 'AWS_SECRET_ACCESS_KEY':
            display_value = '*' * len(value) if value else 'NOT SET'
        else:
            display_value = value if value else 'NOT SET'
        print(f"  {key}: {display_value}")
    
    # Check email
    print("\n📧 Email Configuration:")
    email_vars = {
        'EMAIL_HOST_USER': os.getenv('EMAIL_HOST_USER'),
        'EMAIL_HOST_PASSWORD': os.getenv('EMAIL_HOST_PASSWORD'),
    }
    
    for key, value in email_vars.items():
        if key == 'EMAIL_HOST_PASSWORD':
            display_value = '*' * len(value) if value else 'NOT SET'
        else:
            display_value = value if value else 'NOT SET'
        print(f"  {key}: {display_value}")
    
    print("\n" + "=" * 50)
    
    # Check for issues
    issues = []
    
    if not cognito_vars['AWS_COGNITO_USER_POOL_ID'] or cognito_vars['AWS_COGNITO_USER_POOL_ID'] == 'your-user-pool-id':
        issues.append("❌ AWS_COGNITO_USER_POOL_ID is not set or still has placeholder value")
    
    if not cognito_vars['AWS_COGNITO_CLIENT_ID'] or cognito_vars['AWS_COGNITO_CLIENT_ID'] == 'your-client-id':
        issues.append("❌ AWS_COGNITO_CLIENT_ID is not set or still has placeholder value")
    
    if not s3_vars['AWS_ACCESS_KEY_ID'] or s3_vars['AWS_ACCESS_KEY_ID'] == 'your-access-key':
        issues.append("❌ AWS_ACCESS_KEY_ID is not set or still has placeholder value")
    
    if not s3_vars['AWS_STORAGE_BUCKET_NAME'] or s3_vars['AWS_STORAGE_BUCKET_NAME'] == 'your-bucket-name':
        issues.append("❌ AWS_STORAGE_BUCKET_NAME is not set or still has placeholder value")
    
    if issues:
        print("🚨 Issues Found:")
        for issue in issues:
            print(f"  {issue}")
    else:
        print("✅ All AWS configuration looks good!")
    
    print("\n" + "=" * 50)

if __name__ == "__main__":
    check_aws_config()
