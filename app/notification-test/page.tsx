'use client'
import React, { useState } from 'react'
import { Button } from '@/components/ui/button'
import { Card } from '@/components/ui/card'
import { Input } from '@/components/ui/input'
import { Label } from '@/components/ui/label'
import { Mail, MessageSquare, Send, Sparkles, CheckCircle, XCircle, Loader2 } from 'lucide-react'

interface NotificationResult {
  success: boolean
  message: string
}

interface NotificationResults {
  email?: NotificationResult
  sms?: NotificationResult
}

export default function NotificationTestPage() {
  const [loading, setLoading] = useState(false)
  const [results, setResults] = useState<NotificationResults>({})
  const [formData, setFormData] = useState({
    to_email: 'kom647579@gmail.com',
    to_phone: '',
    message: 'Test notification from Healthcare Platform'
  })

  const testEmail = async () => {
    setLoading(true)
    try {
      const response = await fetch('http://localhost:8000/api/test-email/', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({
          to_email: formData.to_email
        })
      })
      
      const data = await response.json()
      setResults(prev => ({ ...prev, email: data }))
    } catch (error) {
      setResults(prev => ({ 
        ...prev, 
        email: { success: false, message: 'Cannot connect to server. Make sure the backend is running on port 8000.' }
      }))
    } finally {
      setLoading(false)
    }
  }

  const testSMS = async () => {
    if (!formData.to_phone) {
      setResults(prev => ({ 
        ...prev, 
        sms: { success: false, message: 'Phone number is required' }
      }))
      return
    }

    setLoading(true)
    try {
      const response = await fetch('http://localhost:8000/api/notifications/test-sms/', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({
          to_phone: formData.to_phone
        })
      })
      
      const data = await response.json()
      setResults(prev => ({ ...prev, sms: data }))
    } catch (error) {
      setResults(prev => ({ 
        ...prev, 
        sms: { success: false, message: 'Cannot connect to server. Make sure the backend is running on port 8000.' }
      }))
    } finally {
      setLoading(false)
    }
  }

  return (
    <div className="min-h-screen bg-gradient-to-br from-indigo-50 via-white to-cyan-50">
      {/* Animated Background */}
      <div className="absolute inset-0 overflow-hidden">
        <div className="absolute -top-40 -right-40 w-80 h-80 bg-purple-300 rounded-full mix-blend-multiply filter blur-xl opacity-70 animate-pulse"></div>
        <div className="absolute -bottom-40 -left-40 w-80 h-80 bg-yellow-300 rounded-full mix-blend-multiply filter blur-xl opacity-70 animate-pulse"></div>
        <div className="absolute top-40 left-40 w-80 h-80 bg-pink-300 rounded-full mix-blend-multiply filter blur-xl opacity-70 animate-pulse"></div>
      </div>

      <div className="relative max-w-6xl mx-auto p-6 space-y-8">
        {/* Header */}
        <div className="text-center space-y-4">
          <div className="inline-flex items-center justify-center w-24 h-24 bg-gradient-to-r from-indigo-500 via-purple-500 to-pink-500 rounded-full mb-6 shadow-2xl">
            <Sparkles className="h-12 w-12 text-white animate-pulse" />
          </div>
          <h1 className="text-5xl font-bold bg-gradient-to-r from-indigo-600 via-purple-600 to-pink-600 bg-clip-text text-transparent">
            Notification Center
          </h1>
          <p className="text-xl text-gray-600 max-w-2xl mx-auto">
            Test and manage your healthcare platform's communication system with beautiful, interactive notifications
          </p>
        </div>

        <div className="grid grid-cols-1 lg:grid-cols-2 gap-8">
          {/* Email Test */}
          <Card className="p-8 bg-white/70 backdrop-blur-sm border-0 shadow-2xl hover:shadow-3xl transition-all duration-500 hover:-translate-y-2 group">
            <div className="flex items-center space-x-4 mb-8">
              <div className="p-4 bg-gradient-to-r from-blue-500 to-cyan-500 rounded-2xl shadow-lg group-hover:scale-110 transition-transform duration-300">
                <Mail className="h-8 w-8 text-white" />
              </div>
              <div>
                <h2 className="text-2xl font-bold text-gray-800">Email Notifications</h2>
                <p className="text-gray-500">Send beautiful test emails instantly</p>
              </div>
            </div>
            
            <div className="space-y-6">
              <div>
                <Label htmlFor="to_email" className="text-sm font-semibold text-gray-700 mb-3 block">Email Address</Label>
                <Input
                  id="to_email"
                  type="email"
                  placeholder="Enter your email address"
                  value={formData.to_email}
                  onChange={(e) => setFormData(prev => ({ ...prev, to_email: e.target.value }))}
                  className="h-14 text-lg border-2 border-gray-200 focus:border-blue-500 focus:ring-4 focus:ring-blue-200 transition-all duration-300 rounded-xl"
                />
              </div>
              
              <Button 
                onClick={testEmail} 
                disabled={loading}
                className="w-full h-14 text-lg font-bold bg-gradient-to-r from-blue-500 via-cyan-500 to-blue-600 hover:from-blue-600 hover:via-cyan-600 hover:to-blue-700 text-white border-0 shadow-xl hover:shadow-2xl transition-all duration-300 transform hover:scale-105 rounded-xl"
              >
                {loading ? (
                  <div className="flex items-center space-x-3">
                    <Loader2 className="h-6 w-6 animate-spin" />
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
                    ? 'bg-gradient-to-r from-green-50 to-emerald-50 border-green-300 text-green-800 scale-100' 
                    : 'bg-gradient-to-r from-red-50 to-rose-50 border-red-300 text-red-800 scale-100'
                }`}>
                  <div className="flex items-center space-x-3">
                    {results.email.success ? (
                      <CheckCircle className="h-6 w-6 text-green-500" />
                    ) : (
                      <XCircle className="h-6 w-6 text-red-500" />
                    )}
                    <p className="font-bold text-lg">
                      {results.email.success ? '🎉 Email Sent Successfully!' : '❌ Failed to Send Email'}
                    </p>
                  </div>
                  <p className="text-base mt-2">{results.email.message}</p>
                  {results.email.success && (
                    <div className="mt-4 p-4 bg-white/60 rounded-xl">
                      <p className="text-sm text-green-700 font-medium">
                        💌 Check your inbox for the beautiful test email!
                      </p>
                    </div>
                  )}
                </div>
              )}
            </div>
          </Card>

          {/* SMS Test */}
          <Card className="p-8 bg-white/70 backdrop-blur-sm border-0 shadow-2xl hover:shadow-3xl transition-all duration-500 hover:-translate-y-2 group">
            <div className="flex items-center space-x-4 mb-8">
              <div className="p-4 bg-gradient-to-r from-green-500 to-emerald-500 rounded-2xl shadow-lg group-hover:scale-110 transition-transform duration-300">
                <MessageSquare className="h-8 w-8 text-white" />
              </div>
              <div>
                <h2 className="text-2xl font-bold text-gray-800">SMS Notifications</h2>
                <p className="text-gray-500">Send test messages via SMS</p>
              </div>
            </div>
            
            <div className="space-y-6">
              <div>
                <Label htmlFor="to_phone" className="text-sm font-semibold text-gray-700 mb-3 block">Phone Number</Label>
                <Input
                  id="to_phone"
                  type="tel"
                  placeholder="+1 (555) 123-4567"
                  value={formData.to_phone}
                  onChange={(e) => setFormData(prev => ({ ...prev, to_phone: e.target.value }))}
                  className="h-14 text-lg border-2 border-gray-200 focus:border-green-500 focus:ring-4 focus:ring-green-200 transition-all duration-300 rounded-xl"
                />
              </div>
              
              <Button 
                onClick={testSMS} 
                disabled={loading}
                className="w-full h-14 text-lg font-bold bg-gradient-to-r from-green-500 via-emerald-500 to-green-600 hover:from-green-600 hover:via-emerald-600 hover:to-green-700 text-white border-0 shadow-xl hover:shadow-2xl transition-all duration-300 transform hover:scale-105 rounded-xl"
              >
                {loading ? (
                  <div className="flex items-center space-x-3">
                    <Loader2 className="h-6 w-6 animate-spin" />
                    <span>Sending SMS...</span>
                  </div>
                ) : (
                  <div className="flex items-center space-x-3">
                    <MessageSquare className="h-6 w-6" />
                    <span>Send Test SMS</span>
                  </div>
                )}
              </Button>
              
              {results.sms && (
                <div className={`p-6 rounded-2xl border-2 transition-all duration-500 transform ${
                  results.sms.success 
                    ? 'bg-gradient-to-r from-green-50 to-emerald-50 border-green-300 text-green-800 scale-100' 
                    : 'bg-gradient-to-r from-red-50 to-rose-50 border-red-300 text-red-800 scale-100'
                }`}>
                  <div className="flex items-center space-x-3">
                    {results.sms.success ? (
                      <CheckCircle className="h-6 w-6 text-green-500" />
                    ) : (
                      <XCircle className="h-6 w-6 text-red-500" />
                    )}
                    <p className="font-bold text-lg">
                      {results.sms.success ? '🎉 SMS Sent Successfully!' : '❌ Failed to Send SMS'}
                    </p>
                  </div>
                  <p className="text-base mt-2">{results.sms.message}</p>
                  {results.sms.success && (
                    <div className="mt-4 p-4 bg-white/60 rounded-xl">
                      <p className="text-sm text-green-700 font-medium">
                        📱 Check your phone for the test message!
                      </p>
                    </div>
                  )}
                </div>
              )}
            </div>
          </Card>
        </div>

        {/* Quick Actions */}
        <Card className="p-8 bg-gradient-to-r from-indigo-50 via-purple-50 to-pink-50 border-0 shadow-xl">
          <div className="flex items-center space-x-4 mb-6">
            <div className="p-3 bg-gradient-to-r from-indigo-500 to-purple-600 rounded-xl">
              <Send className="h-6 w-6 text-white" />
            </div>
            <div>
              <h3 className="text-2xl font-bold text-gray-800">Quick Actions</h3>
              <p className="text-gray-600">Test different notification types</p>
            </div>
          </div>
          
          <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
            <Button 
              onClick={() => window.open('/test-notifications', '_blank')}
              className="h-16 text-lg font-semibold bg-gradient-to-r from-purple-500 to-pink-600 hover:from-purple-600 hover:to-pink-700 text-white border-0 shadow-lg hover:shadow-xl transition-all duration-300 transform hover:scale-105 rounded-xl"
            >
              <div className="flex items-center space-x-3">
                <Sparkles className="h-6 w-6" />
                <span>Full Test Suite</span>
              </div>
            </Button>
            
            <Button 
              onClick={() => window.open('/test-email-simple', '_blank')}
              className="h-16 text-lg font-semibold bg-gradient-to-r from-blue-500 to-cyan-600 hover:from-blue-600 hover:to-cyan-700 text-white border-0 shadow-lg hover:shadow-xl transition-all duration-300 transform hover:scale-105 rounded-xl"
            >
              <div className="flex items-center space-x-3">
                <Mail className="h-6 w-6" />
                <span>Simple Email Test</span>
              </div>
            </Button>
            
            <Button 
              onClick={() => window.open('/dashboard', '_blank')}
              className="h-16 text-lg font-semibold bg-gradient-to-r from-gray-500 to-gray-600 hover:from-gray-600 hover:to-gray-700 text-white border-0 shadow-lg hover:shadow-xl transition-all duration-300 transform hover:scale-105 rounded-xl"
            >
              <div className="flex items-center space-x-3">
                <CheckCircle className="h-6 w-6" />
                <span>Go to Dashboard</span>
              </div>
            </Button>
          </div>
        </Card>

        {/* Instructions */}
        <Card className="p-8 bg-white/80 backdrop-blur-sm border-0 shadow-xl">
          <div className="flex items-center space-x-4 mb-6">
            <div className="p-3 bg-gradient-to-r from-yellow-500 to-orange-500 rounded-xl">
              <span className="text-white text-2xl">📋</span>
            </div>
            <div>
              <h3 className="text-2xl font-bold text-gray-800">Getting Started</h3>
              <p className="text-gray-600">Follow these steps to test your notifications</p>
            </div>
          </div>
          
          <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6">
            <div className="text-center space-y-3">
              <div className="w-12 h-12 bg-blue-500 rounded-full flex items-center justify-center mx-auto text-white font-bold text-lg">1</div>
              <h4 className="font-semibold text-gray-800">Start Backend</h4>
              <p className="text-sm text-gray-600">Run: <code className="bg-gray-100 px-2 py-1 rounded">py manage.py runserver</code></p>
            </div>
            
            <div className="text-center space-y-3">
              <div className="w-12 h-12 bg-green-500 rounded-full flex items-center justify-center mx-auto text-white font-bold text-lg">2</div>
              <h4 className="font-semibold text-gray-800">Enter Email</h4>
              <p className="text-sm text-gray-600">Type your email address in the field above</p>
            </div>
            
            <div className="text-center space-y-3">
              <div className="w-12 h-12 bg-purple-500 rounded-full flex items-center justify-center mx-auto text-white font-bold text-lg">3</div>
              <h4 className="font-semibold text-gray-800">Click Send</h4>
              <p className="text-sm text-gray-600">Press the "Send Test Email" button</p>
            </div>
            
            <div className="text-center space-y-3">
              <div className="w-12 h-12 bg-pink-500 rounded-full flex items-center justify-center mx-auto text-white font-bold text-lg">4</div>
              <h4 className="font-semibold text-gray-800">Check Inbox</h4>
              <p className="text-sm text-gray-600">Look for the test email in your inbox</p>
            </div>
          </div>
        </Card>
      </div>
    </div>
  )
}

