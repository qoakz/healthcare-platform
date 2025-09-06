#!/usr/bin/env python
"""
Simple working server for email testing
"""
import os
import sys
import django
from http.server import HTTPServer, BaseHTTPRequestHandler
import json

# Add the project directory to Python path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

# Set up Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'healthcare_platform.settings')
django.setup()

from django.core.mail import send_mail

class EmailHandler(BaseHTTPRequestHandler):
    def do_POST(self):
        if self.path == '/api/test-email/':
            self.send_response(200)
            self.send_header('Content-type', 'application/json')
            self.send_header('Access-Control-Allow-Origin', '*')
            self.send_header('Access-Control-Allow-Methods', 'POST, OPTIONS')
            self.send_header('Access-Control-Allow-Headers', 'Content-Type')
            self.end_headers()
            
            try:
                # Read request body
                content_length = int(self.headers['Content-Length'])
                post_data = self.rfile.read(content_length)
                data = json.loads(post_data.decode('utf-8'))
                
                # Send email
                send_mail(
                    subject='Test Email - Healthcare Platform',
                    message='This is a test email from the Healthcare Platform notification system.',
                    from_email='kom647579@gmail.com',
                    recipient_list=[data.get('to_email', 'kom647579@gmail.com')],
                    fail_silently=False,
                )
                
                response = {
                    'success': True,
                    'message': 'Email sent successfully!'
                }
                
            except Exception as e:
                response = {
                    'success': False,
                    'message': f'Failed to send email: {str(e)}'
                }
            
            self.wfile.write(json.dumps(response).encode())
        else:
            self.send_response(404)
            self.end_headers()
    
    def do_OPTIONS(self):
        self.send_response(200)
        self.send_header('Access-Control-Allow-Origin', '*')
        self.send_header('Access-Control-Allow-Methods', 'POST, OPTIONS')
        self.send_header('Access-Control-Allow-Headers', 'Content-Type')
        self.end_headers()

def run_server():
    server_address = ('0.0.0.0', 8000)
    httpd = HTTPServer(server_address, EmailHandler)
    print("🚀 Simple email server running on http://0.0.0.0:8000")
    print("📧 Email test endpoint: http://localhost:8000/api/test-email/")
    print("⏳ Press Ctrl+C to stop")
    
    try:
        httpd.serve_forever()
    except KeyboardInterrupt:
        print("\n🛑 Server stopped")
        httpd.server_close()

if __name__ == "__main__":
    run_server()

