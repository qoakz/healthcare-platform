'use client'
import React, { useState } from 'react'
import { Button } from '@/components/ui/button'
import { Card } from '@/components/ui/card'
import { Input } from '@/components/ui/input'
import { Label } from '@/components/ui/label'
import { Mail, CheckCircle, XCircle } from 'lucide-react'

export default function TestEmailSimplePage() {
  const [loading, setLoading] = useState(false)
  const [result, setResult] = useState<any>(null)
  const [email, setEmail] = useState('kom647579@gmail.com')

  const testEmail = async () => {
    setLoading(true)
    setResult(null)
    
    try {
      // Test the backend directly
      const response = await fetch('http://localhost:8000/api/test-email/', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({
          to_email: email
        })
      })
      
      const data = await response.json()
      setResult(data)
    } catch (error) {
      setResult({
        success: false,
        message: 'Cannot connect to server. Make sure the backend is running on port 8000.'
      })
    } finally {
      setLoading(false)
    }
  }

  return (
    <div className="min-h-screen bg-gray-100 p-8">
      <div className="max-w-2xl mx-auto">
        <h1 className="text-3xl font-bold mb-8 text-center">Email Notification Test</h1>
        
        <Card className="p-6">
          <div className="flex items-center space-x-2 mb-4">
            <Mail className="h-5 w-5 text-blue-500" />
            <h2 className="text-xl font-semibold">Test Email Sending</h2>
          </div>
          
          <div className="space-y-4">
            <div>
              <Label htmlFor="email">Email Address</Label>
              <Input
                id="email"
                type="email"
                placeholder="test@example.com"
                value={email}
                onChange={(e) => setEmail(e.target.value)}
              />
            </div>
            
            <Button 
              onClick={testEmail} 
              disabled={loading}
              className="w-full"
            >
              {loading ? 'Sending...' : 'Send Test Email'}
            </Button>
            
            {result && (
              <div className={`p-4 rounded-lg flex items-center space-x-2 ${
                result.success ? 'bg-green-50 text-green-800' : 'bg-red-50 text-red-800'
              }`}>
                {result.success ? (
                  <CheckCircle className="h-5 w-5 text-green-600" />
                ) : (
                  <XCircle className="h-5 w-5 text-red-600" />
                )}
                <div>
                  <p className="font-medium">
                    {result.success ? '✅ Success!' : '❌ Failed'}
                  </p>
                  <p className="text-sm">{result.message}</p>
                </div>
              </div>
            )}
          </div>
        </Card>

        <Card className="p-6 mt-6 bg-blue-50">
          <h3 className="font-semibold mb-2">📋 Instructions</h3>
          <ul className="text-sm text-gray-700 space-y-1">
            <li>• Make sure the backend server is running: <code>py manage.py runserver 0.0.0.0:8000</code></li>
            <li>• Enter your email address above</li>
            <li>• Click "Send Test Email"</li>
            <li>• Check your email for the test message</li>
            <li>• If it fails, check the backend server is running</li>
          </ul>
        </Card>

        <Card className="p-6 mt-6 bg-yellow-50">
          <h3 className="font-semibold mb-2">🔧 Troubleshooting</h3>
          <ul className="text-sm text-gray-700 space-y-1">
            <li>• <strong>Backend not running:</strong> Go to the <code>api</code> folder and run <code>py manage.py runserver 0.0.0.0:8000</code></li>
            <li>• <strong>Email not received:</strong> Check spam folder</li>
            <li>• <strong>Connection error:</strong> Make sure port 8000 is not blocked</li>
          </ul>
        </Card>
      </div>
    </div>
  )
}

