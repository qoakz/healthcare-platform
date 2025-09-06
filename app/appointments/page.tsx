'use client'

import { useState, useEffect } from 'react'
import { useAuth } from '@/hooks/use-auth-simple'
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from '@/components/ui/card'
import { Button } from '@/components/ui/button'
import { Badge } from '@/components/ui/badge'
import { Input } from '@/components/ui/input'
import { Select, SelectContent, SelectItem, SelectTrigger, SelectValue } from '@/components/ui/select'
import { Calendar, Clock, Video, User, Search, Filter, MoreVertical } from 'lucide-react'
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
  status: 'upcoming' | 'completed' | 'cancelled' | 'rescheduled'
  type: 'video' | 'in-person'
  reason: string
  duration: number
  meetingLink?: string
}

export default function AppointmentsPage() {
  const { user, isAuthenticated } = useAuth()
  const [appointments, setAppointments] = useState<Appointment[]>([])
  const [filteredAppointments, setFilteredAppointments] = useState<Appointment[]>([])
  const [isLoading, setIsLoading] = useState(true)
  const [searchTerm, setSearchTerm] = useState('')
  const [statusFilter, setStatusFilter] = useState('all')
  const [typeFilter, setTypeFilter] = useState('all')

  useEffect(() => {
    if (!isAuthenticated) {
      return
    }

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
            reason: 'Follow-up consultation',
            duration: 30,
            meetingLink: 'https://meet.healthcare.com/abc123'
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
            reason: 'Skin examination',
            duration: 45
          },
          {
            id: '3',
            doctor: {
              name: 'Dr. Emily Rodriguez',
              specialty: 'Pediatrics',
              avatar: '/avatars/doctor3.jpg'
            },
            date: '2024-01-08',
            time: '11:00 AM',
            status: 'cancelled',
            type: 'video',
            reason: 'General checkup',
            duration: 30
          },
          {
            id: '4',
            doctor: {
              name: 'Dr. David Kim',
              specialty: 'Neurology',
              avatar: '/avatars/doctor4.jpg'
            },
            date: '2024-01-20',
            time: '3:00 PM',
            status: 'upcoming',
            type: 'in-person',
            reason: 'Neurological assessment',
            duration: 60
          }
        ]
        setAppointments(mockAppointments)
        setFilteredAppointments(mockAppointments)
      } catch (error) {
        console.error('Failed to fetch appointments:', error)
      } finally {
        setIsLoading(false)
      }
    }

    fetchAppointments()
  }, [isAuthenticated])

  useEffect(() => {
    // Filter appointments
    let filtered = appointments

    // Filter by search term
    if (searchTerm) {
      filtered = filtered.filter(appointment =>
        appointment.doctor.name.toLowerCase().includes(searchTerm.toLowerCase()) ||
        appointment.doctor.specialty.toLowerCase().includes(searchTerm.toLowerCase()) ||
        appointment.reason.toLowerCase().includes(searchTerm.toLowerCase())
      )
    }

    // Filter by status
    if (statusFilter !== 'all') {
      filtered = filtered.filter(appointment => appointment.status === statusFilter)
    }

    // Filter by type
    if (typeFilter !== 'all') {
      filtered = filtered.filter(appointment => appointment.type === typeFilter)
    }

    setFilteredAppointments(filtered)
  }, [appointments, searchTerm, statusFilter, typeFilter])

  const getStatusBadge = (status: string) => {
    const variants = {
      upcoming: 'default',
      completed: 'secondary',
      cancelled: 'destructive',
      rescheduled: 'outline'
    } as const

    return (
      <Badge variant={variants[status as keyof typeof variants] || 'outline'}>
        {status.charAt(0).toUpperCase() + status.slice(1)}
      </Badge>
    )
  }

  const getStatusColor = (status: string) => {
    const colors = {
      upcoming: 'text-blue-600',
      completed: 'text-green-600',
      cancelled: 'text-red-600',
      rescheduled: 'text-yellow-600'
    }
    return colors[status as keyof typeof colors] || 'text-gray-600'
  }

  if (!isAuthenticated) {
    return (
      <div className="min-h-screen flex items-center justify-center">
        <div className="text-center">
          <h2 className="text-2xl font-bold text-gray-900">Please log in</h2>
          <p className="mt-2 text-gray-600">You need to be logged in to view your appointments.</p>
          <Button className="mt-4" asChild>
            <Link href="/auth/login">Log In</Link>
          </Button>
        </div>
      </div>
    )
  }

  if (isLoading) {
    return (
      <div className="min-h-screen flex items-center justify-center">
        <div className="animate-spin rounded-full h-12 w-12 border-b-2 border-blue-600"></div>
      </div>
    )
  }

  return (
    <div className="min-h-screen bg-gradient-to-br from-slate-50 via-blue-50 to-indigo-100">
      {/* Background Pattern */}
      <div className="absolute inset-0 bg-[url('data:image/svg+xml,%3Csvg%20width%3D%2260%22%20height%3D%2260%22%20viewBox%3D%220%200%2060%2060%22%20xmlns%3D%22http%3A//www.w3.org/2000/svg%22%3E%3Cg%20fill%3D%22none%22%20fill-rule%3D%22evenodd%22%3E%3Cg%20fill%3D%22%239C92AC%22%20fill-opacity%3D%220.05%22%3E%3Ccircle%20cx%3D%2230%22%20cy%3D%2230%22%20r%3D%222%22/%3E%3C/g%3E%3C/g%3E%3C/svg%3E')] opacity-40"></div>
      
      <div className="relative max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-8">
        {/* Header */}
        <div className="text-center mb-12">
          <h1 className="text-5xl md:text-6xl font-bold mb-6">
            <span className="bg-gradient-to-r from-indigo-600 via-purple-600 to-pink-600 bg-clip-text text-transparent">
              My
            </span>
            <br />
            <span className="text-gray-800">Appointments</span>
          </h1>
          <p className="text-xl text-gray-600 max-w-3xl mx-auto">
            Manage your healthcare appointments and stay on top of your medical care
          </p>
        </div>

        {/* Filters */}
        <div className="bg-white/80 backdrop-blur-sm rounded-2xl shadow-2xl border border-white/20 p-8 mb-12">
          <div className="grid grid-cols-1 md:grid-cols-4 gap-6">
            <div className="relative group">
              <Search className="absolute left-4 top-1/2 transform -translate-y-1/2 text-gray-400 h-5 w-5 group-focus-within:text-indigo-500 transition-colors" />
              <Input
                placeholder="Search appointments..."
                value={searchTerm}
                onChange={(e) => setSearchTerm(e.target.value)}
                className="pl-12 h-14 text-lg border-2 border-gray-200 focus:border-indigo-500 focus:ring-4 focus:ring-indigo-200 transition-all duration-300 rounded-xl"
              />
            </div>

            <Select value={statusFilter} onValueChange={setStatusFilter}>
              <SelectTrigger className="h-14 text-lg border-2 border-gray-200 focus:border-indigo-500 focus:ring-4 focus:ring-indigo-200 transition-all duration-300 rounded-xl">
                <SelectValue placeholder="Filter by status" />
              </SelectTrigger>
              <SelectContent>
                <SelectItem value="all">All Status</SelectItem>
                <SelectItem value="upcoming">Upcoming</SelectItem>
                <SelectItem value="completed">Completed</SelectItem>
                <SelectItem value="cancelled">Cancelled</SelectItem>
                <SelectItem value="rescheduled">Rescheduled</SelectItem>
              </SelectContent>
            </Select>

            <Select value={typeFilter} onValueChange={setTypeFilter}>
              <SelectTrigger className="h-14 text-lg border-2 border-gray-200 focus:border-indigo-500 focus:ring-4 focus:ring-indigo-200 transition-all duration-300 rounded-xl">
                <SelectValue placeholder="Filter by type" />
              </SelectTrigger>
              <SelectContent>
                <SelectItem value="all">All Types</SelectItem>
                <SelectItem value="video">Video</SelectItem>
                <SelectItem value="in-person">In-Person</SelectItem>
              </SelectContent>
            </Select>

            <Button variant="outline" className="h-14 text-lg font-semibold border-2 border-indigo-200 text-indigo-600 hover:bg-indigo-50 hover:border-indigo-300 transition-all duration-300 rounded-xl">
              <Filter className="h-5 w-5 mr-2" />
              More Filters
            </Button>
          </div>
        </div>

        {/* Results */}
        <div className="mb-8 text-center">
          <p className="text-lg text-gray-600">
            Found <span className="font-bold text-indigo-600">{filteredAppointments.length}</span> appointment{filteredAppointments.length !== 1 ? 's' : ''} in your schedule
          </p>
        </div>

        {/* Appointments List */}
        <div className="space-y-6">
          {filteredAppointments.map((appointment, index) => (
            <Card 
              key={appointment.id} 
              className="group relative bg-white/80 backdrop-blur-sm border border-white/20 shadow-xl hover:shadow-2xl transition-all duration-500 transform hover:-translate-y-1 rounded-2xl overflow-hidden"
              style={{ animationDelay: `${index * 100}ms` }}
            >
              {/* Gradient Background */}
              <div className="absolute inset-0 bg-gradient-to-r from-indigo-50 via-purple-50 to-pink-50 opacity-0 group-hover:opacity-100 transition-opacity duration-500"></div>
              
              <CardContent className="relative p-8">
                <div className="flex items-center justify-between">
                  <div className="flex items-center space-x-6">
                    {/* Doctor Avatar */}
                    <div className="relative">
                      <div className="w-16 h-16 bg-gradient-to-br from-indigo-500 to-purple-600 rounded-2xl flex items-center justify-center shadow-lg group-hover:scale-110 transition-transform duration-300">
                        <User className="h-8 w-8 text-white" />
                      </div>
                      {/* Status indicator */}
                      <div className={`absolute -bottom-1 -right-1 w-6 h-6 border-2 border-white rounded-full ${
                        appointment.status === 'upcoming' ? 'bg-green-500' :
                        appointment.status === 'completed' ? 'bg-blue-500' :
                        appointment.status === 'cancelled' ? 'bg-red-500' :
                        'bg-yellow-500'
                      }`}></div>
                    </div>
                    
                    <div className="flex-1">
                      <h3 className="text-2xl font-bold text-gray-800 group-hover:text-indigo-600 transition-colors">
                        {appointment.doctor.name}
                      </h3>
                      <p className="text-indigo-600 font-semibold text-lg mb-3">
                        {appointment.doctor.specialty}
                      </p>
                      
                      {/* Appointment Details */}
                      <div className="flex items-center space-x-6">
                        <div className="flex items-center text-gray-600">
                          <Calendar className="h-5 w-5 mr-2 text-indigo-500" />
                          <span className="font-medium">{appointment.date}</span>
                        </div>
                        <div className="flex items-center text-gray-600">
                          <Clock className="h-5 w-5 mr-2 text-indigo-500" />
                          <span className="font-medium">{appointment.time}</span>
                        </div>
                        <div className="flex items-center text-gray-600">
                          {appointment.type === 'video' ? (
                            <Video className="h-5 w-5 mr-2 text-indigo-500" />
                          ) : (
                            <User className="h-5 w-5 mr-2 text-indigo-500" />
                          )}
                          <span className="font-medium">
                            {appointment.type === 'video' ? 'Video Call' : 'In-Person'}
                          </span>
                        </div>
                      </div>
                      
                      {/* Reason */}
                      <p className="text-gray-600 mt-3 font-medium">
                        {appointment.reason}
                      </p>
                    </div>
                  </div>
                  
                  <div className="flex items-center space-x-6">
                    {/* Status Badge */}
                    <div className="text-right">
                      {getStatusBadge(appointment.status)}
                    </div>
                    
                    {/* Action Buttons */}
                    <div className="flex items-center space-x-3">
                      {appointment.status === 'upcoming' && (
                        <>
                          {appointment.type === 'video' && appointment.meetingLink && (
                            <Button 
                              size="lg" 
                              className="bg-gradient-to-r from-green-500 to-emerald-600 hover:from-green-600 hover:to-emerald-700 text-white border-0 shadow-lg hover:shadow-xl transition-all duration-300 transform hover:scale-105 rounded-xl"
                              asChild
                            >
                              <a href={appointment.meetingLink} target="_blank" rel="noopener noreferrer">
                                Join Call
                              </a>
                            </Button>
                          )}
                          <Button 
                            size="lg" 
                            variant="outline"
                            className="border-2 border-blue-500 text-blue-600 hover:bg-blue-50 hover:border-blue-600 transition-all duration-300 transform hover:scale-105 rounded-xl"
                          >
                            Reschedule
                          </Button>
                          <Button 
                            size="lg" 
                            variant="outline"
                            className="border-2 border-red-500 text-red-600 hover:bg-red-50 hover:border-red-600 transition-all duration-300 transform hover:scale-105 rounded-xl"
                          >
                            Cancel
                          </Button>
                        </>
                      )}
                      
                      {appointment.status === 'completed' && (
                        <Button 
                          size="lg" 
                          variant="outline"
                          className="border-2 border-indigo-500 text-indigo-600 hover:bg-indigo-50 hover:border-indigo-600 transition-all duration-300 transform hover:scale-105 rounded-xl"
                        >
                          View Summary
                        </Button>
                      )}
                      
                      <Button 
                        size="lg" 
                        variant="ghost"
                        className="text-gray-400 hover:text-gray-600 transition-colors duration-300"
                      >
                        <MoreVertical className="h-5 w-5" />
                      </Button>
                    </div>
                  </div>
                </div>
              </CardContent>
            </Card>
          ))}
        </div>

        {filteredAppointments.length === 0 && (
          <div className="text-center py-20">
            <div className="bg-white/80 backdrop-blur-sm rounded-3xl shadow-2xl border border-white/20 p-12 max-w-md mx-auto">
              <div className="w-24 h-24 bg-gradient-to-br from-indigo-400 to-purple-500 rounded-full flex items-center justify-center mx-auto mb-6">
                <Calendar className="h-12 w-12 text-white" />
              </div>
              <h3 className="text-2xl font-bold text-gray-800 mb-4">No appointments found</h3>
              <p className="text-gray-600 mb-8 text-lg">
                {appointments.length === 0 
                  ? "You don't have any appointments yet. Book your first appointment to get started!"
                  : "Try adjusting your search criteria or filters to find your appointments."
                }
              </p>
              {appointments.length === 0 && (
                <Button 
                  asChild
                  className="px-8 py-4 text-lg font-semibold bg-gradient-to-r from-indigo-500 to-purple-600 hover:from-indigo-600 hover:to-purple-700 text-white border-0 shadow-xl hover:shadow-2xl transition-all duration-300 transform hover:scale-105 rounded-xl"
                >
                  <Link href="/doctors">Book Your First Appointment</Link>
                </Button>
              )}
            </div>
          </div>
        )}
      </div>
    </div>
  )
}
