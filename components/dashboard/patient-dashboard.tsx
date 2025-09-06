'use client'

import { useState, useEffect } from 'react'
import { useAuth } from '@/hooks/use-auth-simple'
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from '@/components/ui/card'
import { Button } from '@/components/ui/button'
import { Badge } from '@/components/ui/badge'
import { Calendar, Clock, User, FileText, Video, Phone } from 'lucide-react'
import Link from 'next/link'

interface Appointment {
  id: string
  doctor: {
    name: string
    specialty: string
    avatar?: string
  }
  date: string
  time: string
  status: 'upcoming' | 'completed' | 'cancelled'
  type: 'video' | 'in-person'
  reason: string
}

export function PatientDashboard() {
  const { user } = useAuth()
  const [appointments, setAppointments] = useState<Appointment[]>([])
  const [isLoading, setIsLoading] = useState(true)

  useEffect(() => {
    // Fetch patient appointments
    const fetchAppointments = async () => {
      try {
        // TODO: Replace with actual API call
        const mockAppointments: Appointment[] = [
          {
            id: '1',
            doctor: {
              name: 'Dr. Sarah Johnson',
              specialty: 'Cardiology',
              avatar: '/avatars/doctor1.jpg'
            },
            date: '2024-01-15',
            time: '10:00 AM',
            status: 'upcoming',
            type: 'video',
            reason: 'Follow-up consultation'
          },
          {
            id: '2',
            doctor: {
              name: 'Dr. Michael Chen',
              specialty: 'Dermatology',
              avatar: '/avatars/doctor2.jpg'
            },
            date: '2024-01-10',
            time: '2:30 PM',
            status: 'completed',
            type: 'in-person',
            reason: 'Skin examination'
          }
        ]
        setAppointments(mockAppointments)
      } catch (error) {
        console.error('Failed to fetch appointments:', error)
      } finally {
        setIsLoading(false)
      }
    }

    fetchAppointments()
  }, [])

  const upcomingAppointments = appointments.filter(apt => apt.status === 'upcoming')
  const recentAppointments = appointments.filter(apt => apt.status === 'completed').slice(0, 3)

  if (isLoading) {
    return (
      <div className="min-h-screen flex items-center justify-center">
        <div className="animate-spin rounded-full h-12 w-12 border-b-2 border-blue-600"></div>
      </div>
    )
  }

  return (
    <div className="min-h-screen bg-gray-50">
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-8">
        {/* Header */}
        <div className="mb-8">
          <h1 className="text-3xl font-bold text-gray-900">
            Welcome back, {user?.firstName}!
          </h1>
          <p className="mt-2 text-gray-600">
            Here's an overview of your healthcare journey
          </p>
        </div>

        {/* Quick Actions */}
        <div className="grid grid-cols-1 md:grid-cols-3 gap-6 mb-8">
          <Card className="hover:shadow-lg transition-shadow cursor-pointer">
            <CardHeader className="flex flex-row items-center justify-between space-y-0 pb-2">
              <CardTitle className="text-sm font-medium">Book Appointment</CardTitle>
              <Calendar className="h-4 w-4 text-muted-foreground" />
            </CardHeader>
            <CardContent>
              <div className="text-2xl font-bold">Find a Doctor</div>
              <p className="text-xs text-muted-foreground">
                Schedule your next consultation
              </p>
              <Button className="mt-4 w-full" asChild>
                <Link href="/doctors">Book Now</Link>
              </Button>
            </CardContent>
          </Card>

          <Card className="hover:shadow-lg transition-shadow cursor-pointer">
            <CardHeader className="flex flex-row items-center justify-between space-y-0 pb-2">
              <CardTitle className="text-sm font-medium">Medical Records</CardTitle>
              <FileText className="h-4 w-4 text-muted-foreground" />
            </CardHeader>
            <CardContent>
              <div className="text-2xl font-bold">View Records</div>
              <p className="text-xs text-muted-foreground">
                Access your medical history
              </p>
              <Button className="mt-4 w-full" variant="outline" asChild>
                <Link href="/records">View Records</Link>
              </Button>
            </CardContent>
          </Card>

          <Card className="hover:shadow-lg transition-shadow cursor-pointer">
            <CardHeader className="flex flex-row items-center justify-between space-y-0 pb-2">
              <CardTitle className="text-sm font-medium">Emergency</CardTitle>
              <Phone className="h-4 w-4 text-muted-foreground" />
            </CardHeader>
            <CardContent>
              <div className="text-2xl font-bold">Call 911</div>
              <p className="text-xs text-muted-foreground">
                For medical emergencies
              </p>
              <Button className="mt-4 w-full" variant="destructive" asChild>
                <a href="tel:911">Emergency</a>
              </Button>
            </CardContent>
          </Card>
        </div>

        <div className="grid grid-cols-1 lg:grid-cols-2 gap-8">
          {/* Upcoming Appointments */}
          <Card>
            <CardHeader>
              <CardTitle className="flex items-center gap-2">
                <Clock className="h-5 w-5" />
                Upcoming Appointments
              </CardTitle>
              <CardDescription>
                Your scheduled consultations
              </CardDescription>
            </CardHeader>
            <CardContent>
              {upcomingAppointments.length === 0 ? (
                <div className="text-center py-8">
                  <Calendar className="h-12 w-12 text-gray-400 mx-auto mb-4" />
                  <p className="text-gray-500">No upcoming appointments</p>
                  <Button className="mt-4" asChild>
                    <Link href="/doctors">Book an appointment</Link>
                  </Button>
                </div>
              ) : (
                <div className="space-y-4">
                  {upcomingAppointments.map((appointment) => (
                    <div key={appointment.id} className="flex items-center justify-between p-4 border rounded-lg">
                      <div className="flex items-center space-x-4">
                        <div className="w-10 h-10 bg-blue-100 rounded-full flex items-center justify-center">
                          <User className="h-5 w-5 text-blue-600" />
                        </div>
                        <div>
                          <p className="font-medium">{appointment.doctor.name}</p>
                          <p className="text-sm text-gray-500">{appointment.doctor.specialty}</p>
                          <p className="text-sm text-gray-500">{appointment.date} at {appointment.time}</p>
                        </div>
                      </div>
                      <div className="flex items-center space-x-2">
                        <Badge variant={appointment.type === 'video' ? 'default' : 'secondary'}>
                          {appointment.type === 'video' ? (
                            <><Video className="h-3 w-3 mr-1" /> Video</>
                          ) : (
                            'In-Person'
                          )}
                        </Badge>
                        <Button size="sm" variant="outline">
                          Join
                        </Button>
                      </div>
                    </div>
                  ))}
                </div>
              )}
            </CardContent>
          </Card>

          {/* Recent Appointments */}
          <Card>
            <CardHeader>
              <CardTitle className="flex items-center gap-2">
                <FileText className="h-5 w-5" />
                Recent Appointments
              </CardTitle>
              <CardDescription>
                Your consultation history
              </CardDescription>
            </CardHeader>
            <CardContent>
              {recentAppointments.length === 0 ? (
                <div className="text-center py-8">
                  <FileText className="h-12 w-12 text-gray-400 mx-auto mb-4" />
                  <p className="text-gray-500">No recent appointments</p>
                </div>
              ) : (
                <div className="space-y-4">
                  {recentAppointments.map((appointment) => (
                    <div key={appointment.id} className="flex items-center justify-between p-4 border rounded-lg">
                      <div className="flex items-center space-x-4">
                        <div className="w-10 h-10 bg-green-100 rounded-full flex items-center justify-center">
                          <User className="h-5 w-5 text-green-600" />
                        </div>
                        <div>
                          <p className="font-medium">{appointment.doctor.name}</p>
                          <p className="text-sm text-gray-500">{appointment.doctor.specialty}</p>
                          <p className="text-sm text-gray-500">{appointment.date}</p>
                        </div>
                      </div>
                      <div className="flex items-center space-x-2">
                        <Badge variant="outline">Completed</Badge>
                        <Button size="sm" variant="outline">
                          View Summary
                        </Button>
                      </div>
                    </div>
                  ))}
                </div>
              )}
            </CardContent>
          </Card>
        </div>
      </div>
    </div>
  )
}
