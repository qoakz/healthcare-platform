'use client'

import { useState, useEffect } from 'react'
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from '@/components/ui/card'
import { Button } from '@/components/ui/button'
import { Input } from '@/components/ui/input'
import { Badge } from '@/components/ui/badge'
import { Select, SelectContent, SelectItem, SelectTrigger, SelectValue } from '@/components/ui/select'
import { Search, Star, MapPin, Clock, Video, User } from 'lucide-react'
import Link from 'next/link'

interface Doctor {
  id: string
  name: string
  specialty: string
  experience: number
  rating: number
  reviewCount: number
  consultationFee: number
  location: string
  avatar?: string
  isAvailable: boolean
  nextAvailableSlot?: string
}

export default function DoctorsPage() {
  const [doctors, setDoctors] = useState<Doctor[]>([])
  const [filteredDoctors, setFilteredDoctors] = useState<Doctor[]>([])
  const [isLoading, setIsLoading] = useState(true)
  const [searchTerm, setSearchTerm] = useState('')
  const [selectedSpecialty, setSelectedSpecialty] = useState('all')
  const [sortBy, setSortBy] = useState('rating')

  const specialties = [
    'all',
    'cardiology',
    'dermatology',
    'neurology',
    'orthopedics',
    'pediatrics',
    'psychiatry',
    'gynecology',
    'oncology',
    'general-practice'
  ]

  useEffect(() => {
    // Fetch doctors from API
    const fetchDoctors = async () => {
      try {
        // TODO: Replace with actual API call
        const mockDoctors: Doctor[] = [
          {
            id: '1',
            name: 'Dr. Sarah Johnson',
            specialty: 'Cardiology',
            experience: 15,
            rating: 4.9,
            reviewCount: 234,
            consultationFee: 150,
            location: 'New York, NY',
            avatar: '/avatars/doctor1.jpg',
            isAvailable: true,
            nextAvailableSlot: 'Today, 2:00 PM'
          },
          {
            id: '2',
            name: 'Dr. Michael Chen',
            specialty: 'Dermatology',
            experience: 12,
            rating: 4.8,
            reviewCount: 189,
            consultationFee: 120,
            location: 'Los Angeles, CA',
            avatar: '/avatars/doctor2.jpg',
            isAvailable: true,
            nextAvailableSlot: 'Tomorrow, 10:00 AM'
          },
          {
            id: '3',
            name: 'Dr. Emily Rodriguez',
            specialty: 'Pediatrics',
            experience: 8,
            rating: 4.7,
            reviewCount: 156,
            consultationFee: 100,
            location: 'Chicago, IL',
            avatar: '/avatars/doctor3.jpg',
            isAvailable: false,
            nextAvailableSlot: 'Next week'
          },
          {
            id: '4',
            name: 'Dr. David Kim',
            specialty: 'Neurology',
            experience: 20,
            rating: 4.9,
            reviewCount: 312,
            consultationFee: 200,
            location: 'Boston, MA',
            avatar: '/avatars/doctor4.jpg',
            isAvailable: true,
            nextAvailableSlot: 'Today, 4:30 PM'
          }
        ]
        setDoctors(mockDoctors)
        setFilteredDoctors(mockDoctors)
      } catch (error) {
        console.error('Failed to fetch doctors:', error)
      } finally {
        setIsLoading(false)
      }
    }

    fetchDoctors()
  }, [])

  useEffect(() => {
    // Filter and sort doctors
    let filtered = doctors

    // Filter by search term
    if (searchTerm) {
      filtered = filtered.filter(doctor =>
        doctor.name.toLowerCase().includes(searchTerm.toLowerCase()) ||
        doctor.specialty.toLowerCase().includes(searchTerm.toLowerCase()) ||
        doctor.location.toLowerCase().includes(searchTerm.toLowerCase())
      )
    }

    // Filter by specialty
    if (selectedSpecialty !== 'all') {
      filtered = filtered.filter(doctor =>
        doctor.specialty.toLowerCase() === selectedSpecialty
      )
    }

    // Sort doctors
    filtered.sort((a, b) => {
      switch (sortBy) {
        case 'rating':
          return b.rating - a.rating
        case 'experience':
          return b.experience - a.experience
        case 'fee':
          return a.consultationFee - b.consultationFee
        case 'availability':
          return a.isAvailable === b.isAvailable ? 0 : a.isAvailable ? -1 : 1
        default:
          return 0
      }
    })

    setFilteredDoctors(filtered)
  }, [doctors, searchTerm, selectedSpecialty, sortBy])

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
              Find Your
            </span>
            <br />
            <span className="text-gray-800">Perfect Doctor</span>
          </h1>
          <p className="text-xl text-gray-600 max-w-3xl mx-auto">
            Connect with world-class healthcare professionals who are ready to provide 
            personalized care tailored to your needs
          </p>
        </div>

        {/* Search and Filters */}
        <div className="bg-white/80 backdrop-blur-sm rounded-2xl shadow-2xl border border-white/20 p-8 mb-12">
          <div className="grid grid-cols-1 md:grid-cols-4 gap-6">
            <div className="relative group">
              <Search className="absolute left-4 top-1/2 transform -translate-y-1/2 text-gray-400 h-5 w-5 group-focus-within:text-indigo-500 transition-colors" />
              <Input
                placeholder="Search doctors, specialties, or locations..."
                value={searchTerm}
                onChange={(e) => setSearchTerm(e.target.value)}
                className="pl-12 h-14 text-lg border-2 border-gray-200 focus:border-indigo-500 focus:ring-4 focus:ring-indigo-200 transition-all duration-300 rounded-xl"
              />
            </div>

            <Select value={selectedSpecialty} onValueChange={setSelectedSpecialty}>
              <SelectTrigger className="h-14 text-lg border-2 border-gray-200 focus:border-indigo-500 focus:ring-4 focus:ring-indigo-200 transition-all duration-300 rounded-xl">
                <SelectValue placeholder="Select specialty" />
              </SelectTrigger>
              <SelectContent>
                {specialties.map((specialty) => (
                  <SelectItem key={specialty} value={specialty}>
                    {specialty === 'all' ? 'All Specialties' : specialty.charAt(0).toUpperCase() + specialty.slice(1)}
                  </SelectItem>
                ))}
              </SelectContent>
            </Select>

            <Select value={sortBy} onValueChange={setSortBy}>
              <SelectTrigger className="h-14 text-lg border-2 border-gray-200 focus:border-indigo-500 focus:ring-4 focus:ring-indigo-200 transition-all duration-300 rounded-xl">
                <SelectValue placeholder="Sort by" />
              </SelectTrigger>
              <SelectContent>
                <SelectItem value="rating">Rating</SelectItem>
                <SelectItem value="experience">Experience</SelectItem>
                <SelectItem value="fee">Consultation Fee</SelectItem>
                <SelectItem value="availability">Availability</SelectItem>
              </SelectContent>
            </Select>

            <Button className="h-14 text-lg font-semibold bg-gradient-to-r from-indigo-500 via-purple-500 to-pink-500 hover:from-indigo-600 hover:via-purple-600 hover:to-pink-600 text-white border-0 shadow-xl hover:shadow-2xl transition-all duration-300 transform hover:scale-105 rounded-xl">
              <Search className="h-5 w-5 mr-2" />
              Search
            </Button>
          </div>
        </div>

        {/* Results */}
        <div className="mb-8 text-center">
          <p className="text-lg text-gray-600">
            Found <span className="font-bold text-indigo-600">{filteredDoctors.length}</span> doctor{filteredDoctors.length !== 1 ? 's' : ''} ready to help you
          </p>
        </div>

        {/* Doctors Grid */}
        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-8">
          {filteredDoctors.map((doctor, index) => (
            <Card 
              key={doctor.id} 
              className="group relative bg-white/80 backdrop-blur-sm border border-white/20 shadow-xl hover:shadow-2xl transition-all duration-500 transform hover:-translate-y-2 hover:scale-105 rounded-2xl overflow-hidden"
              style={{ animationDelay: `${index * 100}ms` }}
            >
              {/* Gradient Background */}
              <div className="absolute inset-0 bg-gradient-to-br from-indigo-50 via-purple-50 to-pink-50 opacity-0 group-hover:opacity-100 transition-opacity duration-500"></div>
              
              {/* Availability Badge */}
              <div className="absolute top-4 right-4 z-10">
                <Badge 
                  variant={doctor.isAvailable ? "default" : "secondary"}
                  className={`px-3 py-1 text-sm font-semibold rounded-full ${
                    doctor.isAvailable 
                      ? 'bg-green-500 hover:bg-green-600 text-white' 
                      : 'bg-gray-400 text-white'
                  }`}
                >
                  {doctor.isAvailable ? "Available" : "Busy"}
                </Badge>
              </div>

              <CardHeader className="pb-4">
                <div className="flex items-center space-x-4">
                  {/* Doctor Avatar */}
                  <div className="relative">
                    <div className="w-20 h-20 bg-gradient-to-br from-indigo-500 to-purple-600 rounded-2xl flex items-center justify-center shadow-lg group-hover:scale-110 transition-transform duration-300">
                      <User className="h-10 w-10 text-white" />
                    </div>
                    {/* Online indicator */}
                    {doctor.isAvailable && (
                      <div className="absolute -bottom-1 -right-1 w-6 h-6 bg-green-500 border-2 border-white rounded-full"></div>
                    )}
                  </div>
                  
                  <div className="flex-1">
                    <CardTitle className="text-xl font-bold text-gray-800 group-hover:text-indigo-600 transition-colors">
                      {doctor.name}
                    </CardTitle>
                    <CardDescription className="text-indigo-600 font-semibold text-lg">
                      {doctor.specialty}
                    </CardDescription>
                  </div>
                </div>
              </CardHeader>

              <CardContent className="space-y-4">
                {/* Rating */}
                <div className="flex items-center space-x-2">
                  <div className="flex items-center">
                    {[...Array(5)].map((_, i) => (
                      <Star 
                        key={i} 
                        className={`h-5 w-5 ${
                          i < Math.floor(doctor.rating) 
                            ? 'text-yellow-400 fill-current' 
                            : 'text-gray-300'
                        }`} 
                      />
                    ))}
                  </div>
                  <span className="font-bold text-gray-800">{doctor.rating}</span>
                  <span className="text-gray-500">({doctor.reviewCount} reviews)</span>
                </div>

                {/* Experience */}
                <div className="flex items-center text-gray-600">
                  <Clock className="h-5 w-5 mr-3 text-indigo-500" />
                  <span className="font-medium">{doctor.experience} years experience</span>
                </div>

                {/* Location */}
                <div className="flex items-center text-gray-600">
                  <MapPin className="h-5 w-5 mr-3 text-indigo-500" />
                  <span className="font-medium">{doctor.location}</span>
                </div>

                {/* Consultation Fee */}
                <div className="flex items-center text-gray-600">
                  <Video className="h-5 w-5 mr-3 text-indigo-500" />
                  <span className="font-medium">${doctor.consultationFee}/consultation</span>
                </div>

                {/* Next Available Slot */}
                {doctor.isAvailable && doctor.nextAvailableSlot && (
                  <div className="bg-green-50 border border-green-200 rounded-xl p-3">
                    <div className="text-sm text-green-700 font-semibold">
                      🟢 Next available: {doctor.nextAvailableSlot}
                    </div>
                  </div>
                )}

                {/* Action Buttons */}
                <div className="flex space-x-3 pt-4">
                  <Button 
                    asChild 
                    className="flex-1 h-12 font-semibold bg-gradient-to-r from-indigo-500 to-purple-600 hover:from-indigo-600 hover:to-purple-700 text-white border-0 shadow-lg hover:shadow-xl transition-all duration-300 transform hover:scale-105 rounded-xl"
                  >
                    <Link href={`/doctors/${doctor.id}`}>
                      View Profile
                    </Link>
                  </Button>
                  <Button 
                    variant="outline" 
                    className={`flex-1 h-12 font-semibold border-2 transition-all duration-300 transform hover:scale-105 rounded-xl ${
                      doctor.isAvailable
                        ? 'border-green-500 text-green-600 hover:bg-green-50 hover:border-green-600'
                        : 'border-gray-300 text-gray-400 cursor-not-allowed'
                    }`}
                    disabled={!doctor.isAvailable}
                    asChild
                  >
                    <Link href={`/appointments/book/${doctor.id}`}>
                      Book Now
                    </Link>
                  </Button>
                </div>
              </CardContent>
            </Card>
          ))}
        </div>

        {filteredDoctors.length === 0 && (
          <div className="text-center py-20">
            <div className="bg-white/80 backdrop-blur-sm rounded-3xl shadow-2xl border border-white/20 p-12 max-w-md mx-auto">
              <div className="w-24 h-24 bg-gradient-to-br from-gray-400 to-gray-500 rounded-full flex items-center justify-center mx-auto mb-6">
                <User className="h-12 w-12 text-white" />
              </div>
              <h3 className="text-2xl font-bold text-gray-800 mb-4">No doctors found</h3>
              <p className="text-gray-600 mb-8 text-lg">
                Try adjusting your search criteria or filters to find the perfect doctor for you
              </p>
              <Button 
                onClick={() => {
                  setSearchTerm('')
                  setSelectedSpecialty('all')
                  setSortBy('rating')
                }}
                className="px-8 py-4 text-lg font-semibold bg-gradient-to-r from-indigo-500 to-purple-600 hover:from-indigo-600 hover:to-purple-700 text-white border-0 shadow-xl hover:shadow-2xl transition-all duration-300 transform hover:scale-105 rounded-xl"
              >
                Clear Filters
              </Button>
            </div>
          </div>
        )}
      </div>
    </div>
  )
}
