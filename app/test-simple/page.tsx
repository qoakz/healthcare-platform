'use client'
import React, { useState } from 'react'
import { Button } from '@/components/ui/button'
import { Card } from '@/components/ui/card'
import { Input } from '@/components/ui/input'
import { Label } from '@/components/ui/label'
import { Mail, MessageSquare } from 'lucide-react'

interface NotificationResult {
  success: boolean
  message: string
}

interface NotificationResults {
  email?: NotificationResult
}

export default function TestSimplePage() {
  const [loading, setLoading] = useState(false)
  const [results, setResults] = useState<NotificationResults>({})
  const [email, setEmail] = useState('kom647579@gmail.com')

  const testEmail = async () => {
    setLoading(true)
    try {
      const response = await fetch('http://localhost:8000/api/notifications/test-email/', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({
          to_email: email
        })
      })
      
      const data = await response.json()
      setResults(prev => ({ ...prev, email: data }))
    } catch (error) {
      setResults(prev => ({ 
        ...prev, 
        email: { success: false, message: 'Failed to send test email' }
      }))
    } finally {
      setLoading(false)
    }
  }

  return (
    <div className="min-h-screen bg-gradient-to-br from-blue-50 via-indigo-50 to-purple-50">
      <div className="max-w-2xl mx-auto p-8">
        {/* Header */}
        <div className="text-center space-y-4 mb-8">
          <div className="inline-flex items-center justify-center w-20 h-20 bg-gradient-to-r from-blue-500 to-purple-600 rounded-full mb-4">
            <Mail className="h-10 w-10 text-white" />
          </div>
          <h1 className="text-4xl font-bold bg-gradient-to-r from-blue-600 to-purple-600 bg-clip-text text-transparent">
            Email Test Center
          </h1>
          <p className="text-gray-600 text-lg">Quick and easy email testing</p>
        </div>
        
        <Card className="p-8 bg-white/80 backdrop-blur-sm border-0 shadow-2xl hover:shadow-3xl transition-all duration-300 hover:-translate-y-2">
          <div className="flex items-center space-x-3 mb-6">
            <div className="p-3 bg-gradient-to-r from-blue-500 to-blue-600 rounded-xl">
              <Mail className="h-6 w-6 text-white" />
            </div>
            <div>
              <h2 className="text-2xl font-bold text-gray-800">Send Test Email</h2>
              <p className="text-gray-500">Test your email configuration instantly</p>
            </div>
          </div>
          
          <div className="space-y-6">
            <div>
              <Label htmlFor="email" className="text-sm font-medium text-gray-700 mb-2 block">Email Address</Label>
              <Input
                id="email"
                type="email"
                placeholder="Enter your email address"
                value={email}
                onChange={(e) => setEmail(e.target.value)}
                className="h-14 text-lg border-2 border-gray-200 focus:border-blue-500 focus:ring-4 focus:ring-blue-200 transition-all duration-200 rounded-xl"
              />
            </div>
            
            <Button 
              onClick={testEmail} 
              disabled={loading}
              className="w-full h-14 text-lg font-semibold bg-gradient-to-r from-blue-500 to-purple-600 hover:from-blue-600 hover:to-purple-700 text-white border-0 shadow-xl hover:shadow-2xl transition-all duration-300 transform hover:scale-105 rounded-xl"
            >
              {loading ? (
                <div className="flex items-center space-x-3">
                  <div className="w-6 h-6 border-3 border-white border-t-transparent rounded-full animate-spin"></div>
                  <span>Sending Email...</span>
                </div>
              ) : (
                <div className="flex items-center space-x-3">
                  <Mail className="h-6 w-6" />
                  <span>Send Test Email</span>
                </div>
              )}
            </Button>
            
            {results.email && (
              <div className={`p-6 rounded-2xl border-2 transition-all duration-500 transform ${
                results.email.success 
                  ? 'bg-gradient-to-r from-green-50 to-emerald-50 border-green-200 text-green-800 scale-100' 
                  : 'bg-gradient-to-r from-red-50 to-rose-50 border-red-200 text-red-800 scale-100'
              }`}>
                <div className="flex items-center space-x-3">
                  <div className={`w-4 h-4 rounded-full ${results.email.success ? 'bg-green-500' : 'bg-red-500'} animate-pulse`}></div>
                  <p className="font-bold text-lg">
                    {results.email.success ? '🎉 Email Sent Successfully!' : '❌ Failed to Send Email'}
                  </p>
                </div>
                <p className="text-base mt-2">{results.email.message}</p>
                {results.email.success && (
                  <div className="mt-4 p-3 bg-white/50 rounded-lg">
                    <p className="text-sm text-green-700">
                      💌 Check your inbox for the test email!
                    </p>
                  </div>
                )}
              </div>
            )}
          </div>
        </Card>

        <Card className="p-6 mt-8 bg-gradient-to-r from-blue-50 via-indigo-50 to-purple-50 border-0 shadow-lg">
          <div className="flex items-center space-x-3 mb-4">
            <div className="p-2 bg-gradient-to-r from-blue-500 to-purple-600 rounded-lg">
              <span className="text-white text-xl">📋</span>
            </div>
            <h3 className="font-bold text-xl text-gray-800">Quick Instructions</h3>
          </div>
          <div className="grid grid-cols-1 md:grid-cols-2 gap-4 text-sm text-gray-700">
            <div className="space-y-3">
              <div className="flex items-center space-x-3">
                <div className="w-3 h-3 bg-blue-500 rounded-full"></div>
                <span>Enter your email address above</span>
              </div>
              <div className="flex items-center space-x-3">
                <div className="w-3 h-3 bg-green-500 rounded-full"></div>
                <span>Click "Send Test Email"</span>
              </div>
            </div>
            <div className="space-y-3">
              <div className="flex items-center space-x-3">
                <div className="w-3 h-3 bg-purple-500 rounded-full"></div>
                <span>Check your email inbox</span>
              </div>
              <div className="flex items-center space-x-3">
                <div className="w-3 h-3 bg-orange-500 rounded-full"></div>
                <span>Backend must be running on port 8000</span>
              </div>
            </div>
          </div>
        </Card>
      </div>
    </div>
  )
}
