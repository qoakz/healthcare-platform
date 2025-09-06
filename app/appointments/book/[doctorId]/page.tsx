'use client'

import { useState, useEffect } from 'react'
import { useParams, useRouter } from 'next/navigation'
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from '@/components/ui/card'
import { Button } from '@/components/ui/button'
import { Input } from '@/components/ui/input'
import { Select, SelectContent, SelectItem, SelectTrigger, SelectValue } from '@/components/ui/select'
import { Badge } from '@/components/ui/badge'
import { Calendar, Clock, Video, User, CreditCard } from 'lucide-react'
import { useAuth } from '@/hooks/use-auth-simple'

interface Doctor {
  id: string
  name: string
  specialty: string
  consultationFee: number
  avatar?: string
}

interface TimeSlot {
  id: string
  time: string
  isAvailable: boolean
}

interface BookingForm {
  date: string
  time: string
  type: 'video' | 'in-person'
  reason: string
  notes: string
}

export default function BookAppointmentPage() {
  const params = useParams()
  const router = useRouter()
  const { user, isAuthenticated } = useAuth()
  const doctorId = params.doctorId as string
  
  const [doctor, setDoctor] = useState<Doctor | null>(null)
  const [availableSlots, setAvailableSlots] = useState<TimeSlot[]>([])
  const [selectedDate, setSelectedDate] = useState('')
  const [isLoading, setIsLoading] = useState(true)
  const [isBooking, setIsBooking] = useState(false)
  
  const [formData, setFormData] = useState<BookingForm>({
    date: '',
    time: '',
    type: 'video',
    reason: '',
    notes: ''
  })

  useEffect(() => {
    if (!isAuthenticated) {
      router.push('/auth/login')
      return
    }

    const fetchDoctorAndSlots = async () => {
      try {
        // TODO: Replace with actual API calls
        const mockDoctor: Doctor = {
          id: doctorId,
          name: 'Dr. Sarah Johnson',
          specialty: 'Cardiology',
          consultationFee: 150,
          avatar: '/avatars/doctor1.jpg'
        }

        const mockSlots: TimeSlot[] = [
          { id: '1', time: '09:00', isAvailable: true },
          { id: '2', time: '09:30', isAvailable: false },
          { id: '3', time: '10:00', isAvailable: true },
          { id: '4', time: '10:30', isAvailable: true },
          { id: '5', time: '11:00', isAvailable: false },
          { id: '6', time: '11:30', isAvailable: true },
          { id: '7', time: '14:00', isAvailable: true },
          { id: '8', time: '14:30', isAvailable: true },
          { id: '9', time: '15:00', isAvailable: false },
          { id: '10', time: '15:30', isAvailable: true }
        ]

        setDoctor(mockDoctor)
        setAvailableSlots(mockSlots)
      } catch (error) {
        console.error('Failed to fetch doctor and slots:', error)
      } finally {
        setIsLoading(false)
      }
    }

    fetchDoctorAndSlots()
  }, [doctorId, isAuthenticated, router])

  const handleDateChange = (date: string) => {
    setSelectedDate(date)
    setFormData(prev => ({ ...prev, date, time: '' }))
  }

  const handleTimeSelect = (time: string) => {
    setFormData(prev => ({ ...prev, time }))
  }

  const handleInputChange = (field: keyof BookingForm, value: string) => {
    setFormData(prev => ({ ...prev, [field]: value }))
  }

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault()
    setIsBooking(true)

    try {
      // TODO: Replace with actual API call
      console.log('Booking appointment:', formData)
      
      // Simulate API call
      await new Promise(resolve => setTimeout(resolve, 2000))
      
      // Redirect to payment or confirmation
      router.push(`/appointments/confirm/${doctorId}`)
    } catch (error) {
      console.error('Failed to book appointment:', error)
    } finally {
      setIsBooking(false)
    }
  }

  const isFormValid = formData.date && formData.time && formData.reason

  if (isLoading) {
    return (
      <div className="min-h-screen flex items-center justify-center">
        <div className="animate-spin rounded-full h-12 w-12 border-b-2 border-blue-600"></div>
      </div>
    )
  }

  if (!doctor) {
    return (
      <div className="min-h-screen flex items-center justify-center">
        <div className="text-center">
          <h2 className="text-2xl font-bold text-gray-900">Doctor not found</h2>
          <Button className="mt-4" onClick={() => router.push('/doctors')}>
            Browse Doctors
          </Button>
        </div>
      </div>
    )
  }

  return (
    <div className="min-h-screen bg-gray-50">
      <div className="max-w-4xl mx-auto px-4 sm:px-6 lg:px-8 py-8">
        {/* Header */}
        <div className="mb-8">
          <h1 className="text-3xl font-bold text-gray-900">Book Appointment</h1>
          <p className="mt-2 text-gray-600">
            Schedule your consultation with {doctor.name}
          </p>
        </div>

        <div className="grid grid-cols-1 lg:grid-cols-3 gap-8">
          {/* Booking Form */}
          <div className="lg:col-span-2">
            <Card>
              <CardHeader>
                <CardTitle>Appointment Details</CardTitle>
                <CardDescription>
                  Select your preferred date, time, and consultation type
                </CardDescription>
              </CardHeader>
              <CardContent>
                <form onSubmit={handleSubmit} className="space-y-6">
                  {/* Date Selection */}
                  <div>
                    <label className="block text-sm font-medium text-gray-700 mb-2">
                      Select Date
                    </label>
                    <Input
                      type="date"
                      value={formData.date}
                      onChange={(e) => handleDateChange(e.target.value)}
                      min={new Date().toISOString().split('T')[0]}
                      required
                    />
                  </div>

                  {/* Time Selection */}
                  {formData.date && (
                    <div>
                      <label className="block text-sm font-medium text-gray-700 mb-2">
                        Select Time
                      </label>
                      <div className="grid grid-cols-5 gap-2">
                        {availableSlots.map((slot) => (
                          <Button
                            key={slot.id}
                            type="button"
                            variant={formData.time === slot.time ? "default" : "outline"}
                            disabled={!slot.isAvailable}
                            onClick={() => handleTimeSelect(slot.time)}
                            className="text-sm"
                          >
                            {slot.time}
                          </Button>
                        ))}
                      </div>
                      {!formData.time && (
                        <p className="text-sm text-gray-500 mt-2">
                          Please select an available time slot
                        </p>
                      )}
                    </div>
                  )}

                  {/* Consultation Type */}
                  <div>
                    <label className="block text-sm font-medium text-gray-700 mb-2">
                      Consultation Type
                    </label>
                    <Select value={formData.type} onValueChange={(value: 'video' | 'in-person') => handleInputChange('type', value)}>
                      <SelectTrigger>
                        <SelectValue />
                      </SelectTrigger>
                      <SelectContent>
                        <SelectItem value="video">
                          <div className="flex items-center">
                            <Video className="h-4 w-4 mr-2" />
                            Video Consultation
                          </div>
                        </SelectItem>
                        <SelectItem value="in-person">
                          <div className="flex items-center">
                            <User className="h-4 w-4 mr-2" />
                            In-Person Visit
                          </div>
                        </SelectItem>
                      </SelectContent>
                    </Select>
                  </div>

                  {/* Reason for Visit */}
                  <div>
                    <label className="block text-sm font-medium text-gray-700 mb-2">
                      Reason for Visit *
                    </label>
                    <Input
                      placeholder="Briefly describe your symptoms or reason for consultation"
                      value={formData.reason}
                      onChange={(e) => handleInputChange('reason', e.target.value)}
                      required
                    />
                  </div>

                  {/* Additional Notes */}
                  <div>
                    <label className="block text-sm font-medium text-gray-700 mb-2">
                      Additional Notes (Optional)
                    </label>
                    <textarea
                      className="w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500 focus:border-transparent"
                      rows={3}
                      placeholder="Any additional information you'd like to share..."
                      value={formData.notes}
                      onChange={(e) => handleInputChange('notes', e.target.value)}
                    />
                  </div>

                  {/* Submit Button */}
                  <Button
                    type="submit"
                    disabled={!isFormValid || isBooking}
                    className="w-full"
                  >
                    {isBooking ? 'Booking...' : 'Continue to Payment'}
                  </Button>
                </form>
              </CardContent>
            </Card>
          </div>

          {/* Booking Summary */}
          <div>
            <Card className="sticky top-8">
              <CardHeader>
                <CardTitle>Booking Summary</CardTitle>
              </CardHeader>
              <CardContent className="space-y-4">
                {/* Doctor Info */}
                <div className="flex items-center space-x-3">
                  <div className="w-12 h-12 bg-blue-100 rounded-full flex items-center justify-center">
                    <User className="h-6 w-6 text-blue-600" />
                  </div>
                  <div>
                    <p className="font-medium">{doctor.name}</p>
                    <p className="text-sm text-gray-600">{doctor.specialty}</p>
                  </div>
                </div>

                {/* Appointment Details */}
                <div className="space-y-2">
                  <div className="flex items-center text-sm text-gray-600">
                    <Calendar className="h-4 w-4 mr-2" />
                    <span>{formData.date || 'Select date'}</span>
                  </div>
                  <div className="flex items-center text-sm text-gray-600">
                    <Clock className="h-4 w-4 mr-2" />
                    <span>{formData.time || 'Select time'}</span>
                  </div>
                  <div className="flex items-center text-sm text-gray-600">
                    {formData.type === 'video' ? (
                      <Video className="h-4 w-4 mr-2" />
                    ) : (
                      <User className="h-4 w-4 mr-2" />
                    )}
                    <span>{formData.type === 'video' ? 'Video Consultation' : 'In-Person Visit'}</span>
                  </div>
                </div>

                {/* Pricing */}
                <div className="border-t pt-4">
                  <div className="flex justify-between items-center">
                    <span className="text-sm text-gray-600">Consultation Fee</span>
                    <span className="font-medium">${doctor.consultationFee}</span>
                  </div>
                  <div className="flex justify-between items-center mt-2">
                    <span className="text-sm text-gray-600">Platform Fee</span>
                    <span className="font-medium">$5.00</span>
                  </div>
                  <div className="flex justify-between items-center mt-2 pt-2 border-t">
                    <span className="font-medium">Total</span>
                    <span className="font-bold text-lg">${doctor.consultationFee + 5}</span>
                  </div>
                </div>

                {/* Payment Info */}
                <div className="flex items-center text-sm text-gray-600">
                  <CreditCard className="h-4 w-4 mr-2" />
                  <span>Payment required to confirm appointment</span>
                </div>
              </CardContent>
            </Card>
          </div>
        </div>
      </div>
    </div>
  )
}
