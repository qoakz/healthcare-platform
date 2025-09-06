'use client'

import { useState, useEffect } from 'react'
import { useParams } from 'next/navigation'
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from '@/components/ui/card'
import { Button } from '@/components/ui/button'
import { Badge } from '@/components/ui/badge'
import { Star, MapPin, Clock, Video, User, Calendar, MessageCircle, Award } from 'lucide-react'
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
  bio: string
  education: string[]
  certifications: string[]
  languages: string[]
  isAvailable: boolean
  nextAvailableSlot?: string
}

interface Review {
  id: string
  patientName: string
  rating: number
  comment: string
  date: string
}

export default function DoctorProfilePage() {
  const params = useParams()
  const doctorId = params.id as string
  const [doctor, setDoctor] = useState<Doctor | null>(null)
  const [reviews, setReviews] = useState<Review[]>([])
  const [isLoading, setIsLoading] = useState(true)

  useEffect(() => {
    const fetchDoctorProfile = async () => {
      try {
        // TODO: Replace with actual API call
        const mockDoctor: Doctor = {
          id: doctorId,
          name: 'Dr. Sarah Johnson',
          specialty: 'Cardiology',
          experience: 15,
          rating: 4.9,
          reviewCount: 234,
          consultationFee: 150,
          location: 'New York, NY',
          avatar: '/avatars/doctor1.jpg',
          bio: 'Dr. Sarah Johnson is a board-certified cardiologist with over 15 years of experience in treating cardiovascular diseases. She specializes in preventive cardiology, heart failure management, and interventional cardiology.',
          education: [
            'MD - Harvard Medical School (2008)',
            'Residency - Johns Hopkins Hospital (2012)',
            'Fellowship - Mayo Clinic (2015)'
          ],
          certifications: [
            'Board Certified in Internal Medicine',
            'Board Certified in Cardiovascular Disease',
            'Fellow of the American College of Cardiology'
          ],
          languages: ['English', 'Spanish', 'French'],
          isAvailable: true,
          nextAvailableSlot: 'Today, 2:00 PM'
        }

        const mockReviews: Review[] = [
          {
            id: '1',
            patientName: 'John Smith',
            rating: 5,
            comment: 'Dr. Johnson is an excellent cardiologist. She took the time to explain everything clearly and made me feel comfortable throughout the consultation.',
            date: '2024-01-10'
          },
          {
            id: '2',
            patientName: 'Emily Davis',
            rating: 5,
            comment: 'Very professional and knowledgeable. The video consultation was seamless and she provided great follow-up care.',
            date: '2024-01-08'
          },
          {
            id: '3',
            patientName: 'Michael Brown',
            rating: 4,
            comment: 'Good experience overall. Dr. Johnson was thorough in her examination and provided clear treatment recommendations.',
            date: '2024-01-05'
          }
        ]

        setDoctor(mockDoctor)
        setReviews(mockReviews)
      } catch (error) {
        console.error('Failed to fetch doctor profile:', error)
      } finally {
        setIsLoading(false)
      }
    }

    fetchDoctorProfile()
  }, [doctorId])

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
          <p className="mt-2 text-gray-600">The doctor you're looking for doesn't exist.</p>
          <Button className="mt-4" asChild>
            <Link href="/doctors">Browse Doctors</Link>
          </Button>
        </div>
      </div>
    )
  }

  return (
    <div className="min-h-screen bg-gray-50">
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-8">
        {/* Header */}
        <div className="bg-white rounded-lg shadow-sm border p-6 mb-8">
          <div className="flex flex-col md:flex-row md:items-center md:justify-between">
            <div className="flex items-center space-x-6">
              <div className="w-24 h-24 bg-blue-100 rounded-full flex items-center justify-center">
                <User className="h-12 w-12 text-blue-600" />
              </div>
              <div>
                <h1 className="text-3xl font-bold text-gray-900">{doctor.name}</h1>
                <p className="text-xl text-blue-600 font-medium">{doctor.specialty}</p>
                <div className="flex items-center mt-2">
                  <Star className="h-5 w-5 text-yellow-400 mr-1" />
                  <span className="font-medium">{doctor.rating}</span>
                  <span className="ml-2 text-gray-600">({doctor.reviewCount} reviews)</span>
                </div>
              </div>
            </div>
            <div className="mt-6 md:mt-0 flex flex-col space-y-4">
              <Badge variant={doctor.isAvailable ? "default" : "secondary"} className="w-fit">
                {doctor.isAvailable ? "Available" : "Busy"}
              </Badge>
              <div className="text-right">
                <p className="text-2xl font-bold text-gray-900">${doctor.consultationFee}</p>
                <p className="text-sm text-gray-600">per consultation</p>
              </div>
              <div className="flex space-x-3">
                <Button asChild className="flex-1">
                  <Link href={`/appointments/book/${doctor.id}`}>
                    Book Appointment
                  </Link>
                </Button>
                <Button variant="outline" className="flex-1">
                  <MessageCircle className="h-4 w-4 mr-2" />
                  Message
                </Button>
              </div>
            </div>
          </div>
        </div>

        <div className="grid grid-cols-1 lg:grid-cols-3 gap-8">
          {/* Main Content */}
          <div className="lg:col-span-2 space-y-8">
            {/* About */}
            <Card>
              <CardHeader>
                <CardTitle>About Dr. {doctor.name.split(' ')[1]}</CardTitle>
              </CardHeader>
              <CardContent>
                <p className="text-gray-700 leading-relaxed">{doctor.bio}</p>
              </CardContent>
            </Card>

            {/* Education & Certifications */}
            <Card>
              <CardHeader>
                <CardTitle className="flex items-center gap-2">
                  <Award className="h-5 w-5" />
                  Education & Certifications
                </CardTitle>
              </CardHeader>
              <CardContent>
                <div className="space-y-6">
                  <div>
                    <h4 className="font-semibold text-gray-900 mb-3">Education</h4>
                    <ul className="space-y-2">
                      {doctor.education.map((edu, index) => (
                        <li key={index} className="flex items-center text-gray-700">
                          <div className="w-2 h-2 bg-blue-600 rounded-full mr-3"></div>
                          {edu}
                        </li>
                      ))}
                    </ul>
                  </div>
                  <div>
                    <h4 className="font-semibold text-gray-900 mb-3">Certifications</h4>
                    <ul className="space-y-2">
                      {doctor.certifications.map((cert, index) => (
                        <li key={index} className="flex items-center text-gray-700">
                          <div className="w-2 h-2 bg-green-600 rounded-full mr-3"></div>
                          {cert}
                        </li>
                      ))}
                    </ul>
                  </div>
                </div>
              </CardContent>
            </Card>

            {/* Reviews */}
            <Card>
              <CardHeader>
                <CardTitle>Patient Reviews</CardTitle>
                <CardDescription>
                  {doctor.reviewCount} reviews • {doctor.rating} average rating
                </CardDescription>
              </CardHeader>
              <CardContent>
                <div className="space-y-6">
                  {reviews.map((review) => (
                    <div key={review.id} className="border-b border-gray-200 pb-6 last:border-b-0 last:pb-0">
                      <div className="flex items-center justify-between mb-2">
                        <div className="flex items-center space-x-2">
                          <span className="font-medium text-gray-900">{review.patientName}</span>
                          <div className="flex items-center">
                            {[...Array(5)].map((_, i) => (
                              <Star
                                key={i}
                                className={`h-4 w-4 ${
                                  i < review.rating ? 'text-yellow-400 fill-current' : 'text-gray-300'
                                }`}
                              />
                            ))}
                          </div>
                        </div>
                        <span className="text-sm text-gray-500">{review.date}</span>
                      </div>
                      <p className="text-gray-700">{review.comment}</p>
                    </div>
                  ))}
                </div>
              </CardContent>
            </Card>
          </div>

          {/* Sidebar */}
          <div className="space-y-6">
            {/* Quick Info */}
            <Card>
              <CardHeader>
                <CardTitle>Quick Info</CardTitle>
              </CardHeader>
              <CardContent className="space-y-4">
                <div className="flex items-center text-gray-700">
                  <Clock className="h-5 w-5 mr-3 text-gray-400" />
                  <span>{doctor.experience} years experience</span>
                </div>
                <div className="flex items-center text-gray-700">
                  <MapPin className="h-5 w-5 mr-3 text-gray-400" />
                  <span>{doctor.location}</span>
                </div>
                <div className="flex items-center text-gray-700">
                  <Video className="h-5 w-5 mr-3 text-gray-400" />
                  <span>Video consultations available</span>
                </div>
                <div className="flex items-center text-gray-700">
                  <User className="h-5 w-5 mr-3 text-gray-400" />
                  <span>Languages: {doctor.languages.join(', ')}</span>
                </div>
              </CardContent>
            </Card>

            {/* Availability */}
            <Card>
              <CardHeader>
                <CardTitle>Availability</CardTitle>
              </CardHeader>
              <CardContent>
                {doctor.isAvailable ? (
                  <div className="text-center">
                    <div className="w-12 h-12 bg-green-100 rounded-full flex items-center justify-center mx-auto mb-3">
                      <Calendar className="h-6 w-6 text-green-600" />
                    </div>
                    <p className="text-green-600 font-medium mb-2">Available Now</p>
                    <p className="text-sm text-gray-600 mb-4">
                      Next available: {doctor.nextAvailableSlot}
                    </p>
                    <Button asChild className="w-full">
                      <Link href={`/appointments/book/${doctor.id}`}>
                        Book Appointment
                      </Link>
                    </Button>
                  </div>
                ) : (
                  <div className="text-center">
                    <div className="w-12 h-12 bg-gray-100 rounded-full flex items-center justify-center mx-auto mb-3">
                      <Clock className="h-6 w-6 text-gray-600" />
                    </div>
                    <p className="text-gray-600 font-medium mb-2">Currently Busy</p>
                    <p className="text-sm text-gray-500 mb-4">
                      Check back later for availability
                    </p>
                    <Button variant="outline" className="w-full" disabled>
                      Not Available
                    </Button>
                  </div>
                )}
              </CardContent>
            </Card>

            {/* Contact */}
            <Card>
              <CardHeader>
                <CardTitle>Contact</CardTitle>
              </CardHeader>
              <CardContent className="space-y-3">
                <Button variant="outline" className="w-full">
                  <MessageCircle className="h-4 w-4 mr-2" />
                  Send Message
                </Button>
                <Button variant="outline" className="w-full">
                  <Video className="h-4 w-4 mr-2" />
                  Video Call
                </Button>
              </CardContent>
            </Card>
          </div>
        </div>
      </div>
    </div>
  )
}
