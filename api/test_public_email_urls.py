from django.urls import path
import test_public_email

urlpatterns = [
    path('', test_public_email.test_email_public, name='test-email-public'),
]
