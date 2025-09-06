'use client'
import React, { useState } from 'react'
import { Button } from '@/components/ui/button'
import { Card } from '@/components/ui/card'
import { Input } from '@/components/ui/input'
import { Label } from '@/components/ui/label'
import { Select, SelectContent, SelectItem, SelectTrigger, SelectValue } from '@/components/ui/select'
import { Mail, MessageSquare, Send } from 'lucide-react'

interface NotificationResult {
  success: boolean
  message: string
  results?: {
    email?: { status: string }
    sms?: { status: string }
  }
}

interface NotificationResults {
  email?: NotificationResult
  sms?: NotificationResult
  appointment?: NotificationResult
}

export function TestNotifications() {
  const [loading, setLoading] = useState(false)
  const [results, setResults] = useState<NotificationResults>({})
  const [formData, setFormData] = useState({
    to_email: '',
    to_phone: '',
    message: '',
    notification_type: 'appointment_reminder'
  })

  const testEmail = async () => {
    setLoading(true)
    try {
      const response = await fetch('http://localhost:8000/api/notifications/test-email/', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({
          to_email: formData.to_email || undefined
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
        sms: { success: false, message: 'Failed to send test SMS' }
      }))
    } finally {
      setLoading(false)
    }
  }

  const sendAppointmentReminder = async () => {
    setLoading(true)
    try {
      const response = await fetch('http://localhost:8000/api/notifications/appointment-reminder/', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({
          appointment_id: 1, // Replace with actual appointment ID
          channels: ['email', 'sms']
        })
      })
      
      const data = await response.json()
      setResults(prev => ({ ...prev, appointment: data }))
    } catch (error) {
      setResults(prev => ({ 
        ...prev, 
        appointment: { success: false, message: 'Failed to send appointment reminder' }
      }))
    } finally {
      setLoading(false)
    }
  }

  return (
    <div className="min-h-screen bg-gradient-to-br from-blue-50 via-indigo-50 to-purple-50">
      <div className="max-w-4xl mx-auto p-6 space-y-6">
        {/* Header */}
        <div className="text-center space-y-2">
          <div className="inline-flex items-center justify-center w-16 h-16 bg-gradient-to-r from-blue-500 to-purple-600 rounded-full mb-4">
            <Mail className="h-8 w-8 text-white" />
          </div>
          <h1 className="text-4xl font-bold bg-gradient-to-r from-blue-600 to-purple-600 bg-clip-text text-transparent">
            Notification Center
          </h1>
          <p className="text-gray-600 text-lg">Test and manage your communication system</p>
        </div>

        <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
          {/* Email Test */}
          <Card className="p-6 bg-white/80 backdrop-blur-sm border-0 shadow-xl hover:shadow-2xl transition-all duration-300 hover:-translate-y-1">
            <div className="flex items-center space-x-3 mb-6">
              <div className="p-3 bg-gradient-to-r from-blue-500 to-blue-600 rounded-xl">
                <Mail className="h-6 w-6 text-white" />
              </div>
              <div>
                <h2 className="text-xl font-bold text-gray-800">Email Notifications</h2>
                <p className="text-sm text-gray-500">Send test emails instantly</p>
              </div>
            </div>
            
            <div className="space-y-4">
              <div>
                <Label htmlFor="to_email" className="text-sm font-medium text-gray-700">Email Address</Label>
                <Input
                  id="to_email"
                  type="email"
                  placeholder="Enter your email address"
                  value={formData.to_email}
                  onChange={(e) => setFormData(prev => ({ ...prev, to_email: e.target.value }))}
                  className="h-12 text-sm border-2 border-gray-200 focus:border-blue-500 focus:ring-2 focus:ring-blue-200 transition-all duration-200"
                />
              </div>
              
              <Button 
                onClick={testEmail} 
                disabled={loading}
                className="w-full h-12 text-sm font-semibold bg-gradient-to-r from-blue-500 to-blue-600 hover:from-blue-600 hover:to-blue-700 text-white border-0 shadow-lg hover:shadow-xl transition-all duration-200 transform hover:scale-105"
              >
                {loading ? (
                  <div className="flex items-center space-x-2">
                    <div className="w-4 h-4 border-2 border-white border-t-transparent rounded-full animate-spin"></div>
                    <span>Sending...</span>
                  </div>
                ) : (
                  <div className="flex items-center space-x-2">
                    <Mail className="h-4 w-4" />
                    <span>Send Test Email</span>
                  </div>
                )}
              </Button>
              
              {results.email && (
                <div className={`p-4 rounded-xl border-2 transition-all duration-300 ${
                  results.email.success 
                    ? 'bg-gradient-to-r from-green-50 to-emerald-50 border-green-200 text-green-800' 
                    : 'bg-gradient-to-r from-red-50 to-rose-50 border-red-200 text-red-800'
                }`}>
                  <div className="flex items-center space-x-2">
                    <div className={`w-2 h-2 rounded-full ${results.email.success ? 'bg-green-500' : 'bg-red-500'}`}></div>
                    <p className="font-semibold">
                      {results.email.success ? '✅ Email Sent Successfully!' : '❌ Failed to Send Email'}
                    </p>
                  </div>
                  <p className="text-sm mt-1">{results.email.message}</p>
                </div>
              )}
            </div>
          </Card>

          {/* SMS Test */}
          <Card className="p-6 bg-white/80 backdrop-blur-sm border-0 shadow-xl hover:shadow-2xl transition-all duration-300 hover:-translate-y-1">
            <div className="flex items-center space-x-3 mb-6">
              <div className="p-3 bg-gradient-to-r from-green-500 to-emerald-600 rounded-xl">
                <MessageSquare className="h-6 w-6 text-white" />
              </div>
              <div>
                <h2 className="text-xl font-bold text-gray-800">SMS Notifications</h2>
                <p className="text-sm text-gray-500">Send test messages via SMS</p>
              </div>
            </div>
            
            <div className="space-y-4">
              <div>
                <Label htmlFor="to_phone" className="text-sm font-medium text-gray-700">Phone Number</Label>
                <Input
                  id="to_phone"
                  type="tel"
                  placeholder="+1 (555) 123-4567"
                  value={formData.to_phone}
                  onChange={(e) => setFormData(prev => ({ ...prev, to_phone: e.target.value }))}
                  className="h-12 text-sm border-2 border-gray-200 focus:border-green-500 focus:ring-2 focus:ring-green-200 transition-all duration-200"
                />
              </div>
              
              <Button 
                onClick={testSMS} 
                disabled={loading}
                className="w-full h-12 text-sm font-semibold bg-gradient-to-r from-green-500 to-emerald-600 hover:from-green-600 hover:to-emerald-700 text-white border-0 shadow-lg hover:shadow-xl transition-all duration-200 transform hover:scale-105"
              >
                {loading ? (
                  <div className="flex items-center space-x-2">
                    <div className="w-4 h-4 border-2 border-white border-t-transparent rounded-full animate-spin"></div>
                    <span>Sending...</span>
                  </div>
                ) : (
                  <div className="flex items-center space-x-2">
                    <MessageSquare className="h-4 w-4" />
                    <span>Send Test SMS</span>
                  </div>
                )}
              </Button>
              
              {results.sms && (
                <div className={`p-4 rounded-xl border-2 transition-all duration-300 ${
                  results.sms.success 
                    ? 'bg-gradient-to-r from-green-50 to-emerald-50 border-green-200 text-green-800' 
                    : 'bg-gradient-to-r from-red-50 to-rose-50 border-red-200 text-red-800'
                }`}>
                  <div className="flex items-center space-x-2">
                    <div className={`w-2 h-2 rounded-full ${results.sms.success ? 'bg-green-500' : 'bg-red-500'}`}></div>
                    <p className="font-semibold">
                      {results.sms.success ? '✅ SMS Sent Successfully!' : '❌ Failed to Send SMS'}
                    </p>
                  </div>
                  <p className="text-sm mt-1">{results.sms.message}</p>
                </div>
              )}
            </div>
          </Card>
        </div>

        {/* Appointment Reminder Test */}
        <Card className="p-6 bg-white/80 backdrop-blur-sm border-0 shadow-xl hover:shadow-2xl transition-all duration-300 hover:-translate-y-1">
          <div className="flex items-center space-x-3 mb-6">
            <div className="p-3 bg-gradient-to-r from-purple-500 to-pink-600 rounded-xl">
              <Send className="h-6 w-6 text-white" />
            </div>
            <div>
              <h2 className="text-xl font-bold text-gray-800">Appointment Reminders</h2>
              <p className="text-sm text-gray-500">Send automated appointment notifications</p>
            </div>
          </div>
          
          <div className="space-y-4">
            <p className="text-gray-600 bg-gradient-to-r from-purple-50 to-pink-50 p-4 rounded-xl border border-purple-100">
              💡 This will send a test appointment reminder to the first appointment in the system, including both email and SMS notifications.
            </p>
            
            <Button 
              onClick={sendAppointmentReminder} 
              disabled={loading}
              className="w-full h-12 text-sm font-semibold bg-gradient-to-r from-purple-500 to-pink-600 hover:from-purple-600 hover:to-pink-700 text-white border-0 shadow-lg hover:shadow-xl transition-all duration-200 transform hover:scale-105"
            >
              {loading ? (
                <div className="flex items-center space-x-2">
                  <div className="w-4 h-4 border-2 border-white border-t-transparent rounded-full animate-spin"></div>
                  <span>Sending Reminder...</span>
                </div>
              ) : (
                <div className="flex items-center space-x-2">
                  <Send className="h-4 w-4" />
                  <span>Send Appointment Reminder</span>
                </div>
              )}
            </Button>
            
            {results.appointment && (
              <div className={`p-4 rounded-xl border-2 transition-all duration-300 ${
                results.appointment.success 
                  ? 'bg-gradient-to-r from-green-50 to-emerald-50 border-green-200 text-green-800' 
                  : 'bg-gradient-to-r from-red-50 to-rose-50 border-red-200 text-red-800'
              }`}>
                <div className="flex items-center space-x-2">
                  <div className={`w-2 h-2 rounded-full ${results.appointment.success ? 'bg-green-500' : 'bg-red-500'}`}></div>
                  <p className="font-semibold">
                    {results.appointment.success ? '✅ Reminder Sent Successfully!' : '❌ Failed to Send Reminder'}
                  </p>
                </div>
                <p className="text-sm mt-1">{results.appointment.message}</p>
                {results.appointment.results && (
                  <div className="mt-3 grid grid-cols-2 gap-2 text-xs">
                    <div className="bg-white/50 p-2 rounded-lg">
                      <span className="font-medium">Email:</span> {results.appointment.results.email?.status || 'Not sent'}
                    </div>
                    <div className="bg-white/50 p-2 rounded-lg">
                      <span className="font-medium">SMS:</span> {results.appointment.results.sms?.status || 'Not sent'}
                    </div>
                  </div>
                )}
              </div>
            )}
          </div>
        </Card>

        {/* Instructions */}
        <Card className="p-6 bg-gradient-to-r from-blue-50 via-indigo-50 to-purple-50 border-0 shadow-lg">
          <div className="flex items-center space-x-3 mb-4">
            <div className="p-2 bg-gradient-to-r from-blue-500 to-purple-600 rounded-lg">
              <span className="text-white text-lg">📋</span>
            </div>
            <h3 className="font-bold text-lg text-gray-800">Quick Guide</h3>
          </div>
          <div className="grid grid-cols-1 md:grid-cols-2 gap-4 text-sm text-gray-700">
            <div className="space-y-2">
              <div className="flex items-center space-x-2">
                <div className="w-2 h-2 bg-blue-500 rounded-full"></div>
                <span><strong>Email:</strong> Uses Gmail SMTP</span>
              </div>
              <div className="flex items-center space-x-2">
                <div className="w-2 h-2 bg-green-500 rounded-full"></div>
                <span><strong>SMS:</strong> Requires Twilio</span>
              </div>
            </div>
            <div className="space-y-2">
              <div className="flex items-center space-x-2">
                <div className="w-2 h-2 bg-purple-500 rounded-full"></div>
                <span><strong>Reminders:</strong> Auto-send both</span>
              </div>
              <div className="flex items-center space-x-2">
                <div className="w-2 h-2 bg-orange-500 rounded-full"></div>
                <span><strong>Backend:</strong> Port 8000</span>
              </div>
            </div>
          </div>
        </Card>
      </div>
    </div>
  )
}
