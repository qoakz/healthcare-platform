#!/usr/bin/env python
import os
import sys
import django

# Add the project directory to Python path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

# Set up Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'healthcare_platform.settings')
django.setup()

from django.core.management import execute_from_command_line

# Create migration with default responses
def create_migration():
    # Set up input responses
    import io
    import sys
    
    # Mock input to answer migration questions
    original_input = input
    def mock_input(prompt):
        if "renamed to prescription.patient" in prompt:
            return "y"
        elif "Provide a one-off default" in prompt:
            return "1"
        elif "Please select a fix" in prompt:
            return "1"
        else:
            return "y"
    
    # Replace input function
    sys.modules['builtins'].input = mock_input
    
    try:
        execute_from_command_line(['manage.py', 'makemigrations', 'emr'])
        print("Migration created successfully!")
    except Exception as e:
        print(f"Error creating migration: {e}")
    finally:
        # Restore original input
        sys.modules['builtins'].input = original_input

if __name__ == '__main__':
    create_migration()

