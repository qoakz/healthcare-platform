#!/usr/bin/env python
"""
Public email test endpoint
"""
import os
import sys
import django

# Add the project directory to Python path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

# Set up Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'healthcare_platform.settings')
django.setup()

from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_http_methods
from django.core.mail import send_mail
import json

@csrf_exempt
@require_http_methods(["POST"])
def test_email_public(request):
    """Public email test endpoint"""
    try:
        data = json.loads(request.body)
        to_email = data.get('to_email', 'kom647579@gmail.com')
        
        send_mail(
            subject='Test Email - Healthcare Platform',
            message='This is a test email from the Healthcare Platform notification system.',
            from_email='kom647579@gmail.com',
            recipient_list=[to_email],
            fail_silently=False,
        )
        
        return JsonResponse({
            'success': True,
            'message': 'Email sent successfully!'
        })
    except Exception as e:
        return JsonResponse({
            'success': False,
            'message': f'Failed to send email: {str(e)}'
        })

# Test the function directly
if __name__ == "__main__":
    from django.test import RequestFactory
    
    factory = RequestFactory()
    request = factory.post('/test-email/', 
                          data=json.dumps({'to_email': 'kom647579@gmail.com'}),
                          content_type='application/json')
    
    response = test_email_public(request)
    print(f"Response: {response.content.decode()}")

