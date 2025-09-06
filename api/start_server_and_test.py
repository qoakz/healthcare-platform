#!/usr/bin/env python
"""
Start server and test email
"""
import subprocess
import time
import requests
import json
import os
import sys

def start_server():
    """Start Django server"""
    print("🚀 Starting Django server...")
    try:
        # Start server in background
        process = subprocess.Popen([
            sys.executable, 'manage.py', 'runserver', '0.0.0.0:8000'
        ], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        
        # Wait for server to start
        time.sleep(8)
        
        # Check if server is running
        try:
            response = requests.get('http://localhost:8000/api/', timeout=5)
            print("✅ Server started successfully!")
            return process
        except:
            print("❌ Server failed to start")
            return None
            
    except Exception as e:
        print(f"❌ Error starting server: {e}")
        return None

def test_email():
    """Test email sending"""
    print("\n🧪 Testing email...")
    try:
        response = requests.post(
            'http://localhost:8000/api/test-email/',
            json={'to_email': 'kom647579@gmail.com'},
            timeout=10
        )
        
        if response.status_code == 200:
            data = response.json()
            print(f"✅ Email test successful: {data['message']}")
            return True
        else:
            print(f"❌ Email test failed: {response.status_code} - {response.text}")
            return False
            
    except Exception as e:
        print(f"❌ Email test error: {e}")
        return False

def main():
    """Main function"""
    print("🔧 Healthcare Platform - Email Test")
    print("=" * 50)
    
    # Start server
    server_process = start_server()
    if not server_process:
        print("❌ Cannot start server. Exiting.")
        return
    
    # Test email
    success = test_email()
    
    if success:
        print("\n🎉 SUCCESS! Email system is working!")
        print("📧 Check your email: kom647579@gmail.com")
        print("🌐 Frontend test: http://localhost:3000/test-email-simple")
    else:
        print("\n❌ Email test failed. Check the error messages above.")
    
    # Keep server running
    print("\n⏳ Server is running. Press Ctrl+C to stop.")
    try:
        server_process.wait()
    except KeyboardInterrupt:
        print("\n🛑 Stopping server...")
        server_process.terminate()

if __name__ == "__main__":
    main()

