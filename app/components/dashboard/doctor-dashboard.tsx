'use client'

import { useState, useEffect } from 'react'
import { useAuth } from '@/hooks/use-auth-simple'
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from '@/components/ui/card'
import { Button } from '@/components/ui/button'
import { Badge } from '@/components/ui/badge'
import { Calendar, Clock, Users, DollarSign, Video, FileText, Settings } from 'lucide-react'
import Link from 'next/link'

interface DoctorAppointment {
  id: string
  patient: {
    name: string
    age: number
    avatar?: string
  }
  date: string
  time: string
  status: 'upcoming' | 'completed' | 'cancelled'
  type: 'video' | 'in-person'
  reason: string
  duration: number
}

interface DoctorStats {
  totalPatients: number
  todayAppointments: number
  monthlyEarnings: number
  averageRating: number
}

export function DoctorDashboard() {
  const { user } = useAuth()
  const [appointments, setAppointments] = useState<DoctorAppointment[]>([])
  const [stats, setStats] = useState<DoctorStats>({
    totalPatients: 0,
    todayAppointments: 0,
    monthlyEarnings: 0,
    averageRating: 0
  })
  const [isLoading, setIsLoading] = useState(true)

  useEffect(() => {
    // Fetch doctor appointments and stats
    const fetchDoctorData = async () => {
      try {
        // TODO: Replace with actual API calls
        const mockAppointments: DoctorAppointment[] = [
          {
            id: '1',
            patient: {
              name: 'John Smith',
              age: 35,
              avatar: '/avatars/patient1.jpg'
            },
            date: '2024-01-15',
            time: '10:00 AM',
            status: 'upcoming',
            type: 'video',
            reason: 'Follow-up consultation',
            duration: 30
          },
          {
            id: '2',
            patient: {
              name: 'Emily Johnson',
              age: 28,
              avatar: '/avatars/patient2.jpg'
            },
            date: '2024-01-15',
            time: '11:30 AM',
            status: 'upcoming',
            type: 'in-person',
            reason: 'Initial consultation',
            duration: 45
          },
          {
            id: '3',
            patient: {
              name: 'Michael Brown',
              age: 42,
              avatar: '/avatars/patient3.jpg'
            },
            date: '2024-01-14',
            time: '2:00 PM',
            status: 'completed',
            type: 'video',
            reason: 'Prescription refill',
            duration: 20
          }
        ]

        const mockStats: DoctorStats = {
          totalPatients: 156,
          todayAppointments: 8,
          monthlyEarnings: 12450,
          averageRating: 4.8
        }

        setAppointments(mockAppointments)
        setStats(mockStats)
      } catch (error) {
        console.error('Failed to fetch doctor data:', error)
      } finally {
        setIsLoading(false)
      }
    }

    fetchDoctorData()
  }, [])

  const todayAppointments = appointments.filter(apt => 
    apt.date === new Date().toISOString().split('T')[0] && apt.status === 'upcoming'
  )
  const upcomingAppointments = appointments.filter(apt => apt.status === 'upcoming').slice(0, 5)

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
            Welcome back, Dr. {user?.lastName}!
          </h1>
          <p className="mt-2 text-gray-600">
            Here's your practice overview for today
          </p>
        </div>

        {/* Stats Cards */}
        <div className="grid grid-cols-1 md:grid-cols-4 gap-6 mb-8">
          <Card>
            <CardHeader className="flex flex-row items-center justify-between space-y-0 pb-2">
              <CardTitle className="text-sm font-medium">Today's Appointments</CardTitle>
              <Calendar className="h-4 w-4 text-muted-foreground" />
            </CardHeader>
            <CardContent>
              <div className="text-2xl font-bold">{stats.todayAppointments}</div>
              <p className="text-xs text-muted-foreground">
                Scheduled consultations
              </p>
            </CardContent>
          </Card>

          <Card>
            <CardHeader className="flex flex-row items-center justify-between space-y-0 pb-2">
              <CardTitle className="text-sm font-medium">Total Patients</CardTitle>
              <Users className="h-4 w-4 text-muted-foreground" />
            </CardHeader>
            <CardContent>
              <div className="text-2xl font-bold">{stats.totalPatients}</div>
              <p className="text-xs text-muted-foreground">
                Active patients
              </p>
            </CardContent>
          </Card>

          <Card>
            <CardHeader className="flex flex-row items-center justify-between space-y-0 pb-2">
              <CardTitle className="text-sm font-medium">Monthly Earnings</CardTitle>
              <DollarSign className="h-4 w-4 text-muted-foreground" />
            </CardHeader>
            <CardContent>
              <div className="text-2xl font-bold">${stats.monthlyEarnings.toLocaleString()}</div>
              <p className="text-xs text-muted-foreground">
                This month
              </p>
            </CardContent>
          </Card>

          <Card>
            <CardHeader className="flex flex-row items-center justify-between space-y-0 pb-2">
              <CardTitle className="text-sm font-medium">Average Rating</CardTitle>
              <div className="h-4 w-4 text-muted-foreground">⭐</div>
            </CardHeader>
            <CardContent>
              <div className="text-2xl font-bold">{stats.averageRating}</div>
              <p className="text-xs text-muted-foreground">
                Patient satisfaction
              </p>
            </CardContent>
          </Card>
        </div>

        {/* Quick Actions */}
        <div className="grid grid-cols-1 md:grid-cols-3 gap-6 mb-8">
          <Card className="hover:shadow-lg transition-shadow cursor-pointer">
            <CardHeader className="flex flex-row items-center justify-between space-y-0 pb-2">
              <CardTitle className="text-sm font-medium">Manage Schedule</CardTitle>
              <Calendar className="h-4 w-4 text-muted-foreground" />
            </CardHeader>
            <CardContent>
              <div className="text-2xl font-bold">Availability</div>
              <p className="text-xs text-muted-foreground">
                Update your schedule
              </p>
              <Button className="mt-4 w-full" asChild>
                <Link href="/doctor/schedule">Manage Schedule</Link>
              </Button>
            </CardContent>
          </Card>

          <Card className="hover:shadow-lg transition-shadow cursor-pointer">
            <CardHeader className="flex flex-row items-center justify-between space-y-0 pb-2">
              <CardTitle className="text-sm font-medium">Patient Records</CardTitle>
              <FileText className="h-4 w-4 text-muted-foreground" />
            </CardHeader>
            <CardContent>
              <div className="text-2xl font-bold">View Records</div>
              <p className="text-xs text-muted-foreground">
                Access patient information
              </p>
              <Button className="mt-4 w-full" variant="outline" asChild>
                <Link href="/doctor/patients">View Patients</Link>
              </Button>
            </CardContent>
          </Card>

          <Card className="hover:shadow-lg transition-shadow cursor-pointer">
            <CardHeader className="flex flex-row items-center justify-between space-y-0 pb-2">
              <CardTitle className="text-sm font-medium">Profile Settings</CardTitle>
              <Settings className="h-4 w-4 text-muted-foreground" />
            </CardHeader>
            <CardContent>
              <div className="text-2xl font-bold">Settings</div>
              <p className="text-xs text-muted-foreground">
                Update your profile
              </p>
              <Button className="mt-4 w-full" variant="outline" asChild>
                <Link href="/doctor/profile">Edit Profile</Link>
              </Button>
            </CardContent>
          </Card>
        </div>

        <div className="grid grid-cols-1 lg:grid-cols-2 gap-8">
          {/* Today's Appointments */}
          <Card>
            <CardHeader>
              <CardTitle className="flex items-center gap-2">
                <Clock className="h-5 w-5" />
                Today's Appointments
              </CardTitle>
              <CardDescription>
                Your scheduled consultations for today
              </CardDescription>
            </CardHeader>
            <CardContent>
              {todayAppointments.length === 0 ? (
                <div className="text-center py-8">
                  <Calendar className="h-12 w-12 text-gray-400 mx-auto mb-4" />
                  <p className="text-gray-500">No appointments scheduled for today</p>
                </div>
              ) : (
                <div className="space-y-4">
                  {todayAppointments.map((appointment) => (
                    <div key={appointment.id} className="flex items-center justify-between p-4 border rounded-lg">
                      <div className="flex items-center space-x-4">
                        <div className="w-10 h-10 bg-blue-100 rounded-full flex items-center justify-center">
                          <Users className="h-5 w-5 text-blue-600" />
                        </div>
                        <div>
                          <p className="font-medium">{appointment.patient.name}</p>
                          <p className="text-sm text-gray-500">Age: {appointment.patient.age}</p>
                          <p className="text-sm text-gray-500">{appointment.time} ({appointment.duration} min)</p>
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
                        <Button size="sm">
                          Start
                        </Button>
                      </div>
                    </div>
                  ))}
                </div>
              )}
            </CardContent>
          </Card>

          {/* Upcoming Appointments */}
          <Card>
            <CardHeader>
              <CardTitle className="flex items-center gap-2">
                <Calendar className="h-5 w-5" />
                Upcoming Appointments
              </CardTitle>
              <CardDescription>
                Your next scheduled consultations
              </CardDescription>
            </CardHeader>
            <CardContent>
              {upcomingAppointments.length === 0 ? (
                <div className="text-center py-8">
                  <Calendar className="h-12 w-12 text-gray-400 mx-auto mb-4" />
                  <p className="text-gray-500">No upcoming appointments</p>
                </div>
              ) : (
                <div className="space-y-4">
                  {upcomingAppointments.map((appointment) => (
                    <div key={appointment.id} className="flex items-center justify-between p-4 border rounded-lg">
                      <div className="flex items-center space-x-4">
                        <div className="w-10 h-10 bg-green-100 rounded-full flex items-center justify-center">
                          <Users className="h-5 w-5 text-green-600" />
                        </div>
                        <div>
                          <p className="font-medium">{appointment.patient.name}</p>
                          <p className="text-sm text-gray-500">{appointment.date} at {appointment.time}</p>
                          <p className="text-sm text-gray-500">{appointment.reason}</p>
                        </div>
                      </div>
                      <div className="flex items-center space-x-2">
                        <Badge variant="outline">Upcoming</Badge>
                        <Button size="sm" variant="outline">
                          View Details
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
