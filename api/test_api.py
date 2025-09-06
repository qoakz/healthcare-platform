#!/usr/bin/env python
"""
Test API endpoint for email notifications
"""
import requests
import json

def test_email_api():
    """Test the email API endpoint"""
    url = "http://localhost:8000/api/notifications/test-email/"
    data = {"to_email": "kom647579@gmail.com"}
    
    try:
        response = requests.post(url, json=data)
        print(f"Status Code: {response.status_code}")
        print(f"Response: {response.text}")
        
        if response.status_code == 200:
            print("✅ API test successful!")
        else:
            print("❌ API test failed!")
            
    except requests.exceptions.ConnectionError:
        print("❌ Cannot connect to server. Make sure it's running on port 8000")
    except Exception as e:
        print(f"❌ Error: {str(e)}")

if __name__ == "__main__":
    test_email_api()

