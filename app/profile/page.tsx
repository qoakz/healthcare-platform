'use client'

import { useState, useEffect } from 'react'
import { useAuth } from '@/hooks/use-auth-simple'
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from '@/components/ui/card'
import { Button } from '@/components/ui/button'
import { Input } from '@/components/ui/input'
import { Select, SelectContent, SelectItem, SelectTrigger, SelectValue } from '@/components/ui/select'
import { Badge } from '@/components/ui/badge'
import { User, Mail, Phone, Calendar, MapPin, Shield, Edit, Save, X } from 'lucide-react'

interface UserProfile {
  firstName: string
  lastName: string
  email: string
  phone: string
  dateOfBirth: string
  gender: 'male' | 'female' | 'other'
  address: string
  city: string
  state: string
  zipCode: string
  role: 'patient' | 'doctor'
  isVerified: boolean
  emergencyContact: {
    name: string
    phone: string
    relationship: string
  }
}

export default function ProfilePage() {
  const { user, isAuthenticated } = useAuth()
  const [profile, setProfile] = useState<UserProfile | null>(null)
  const [isEditing, setIsEditing] = useState(false)
  const [isLoading, setIsLoading] = useState(true)
  const [isSaving, setIsSaving] = useState(false)
  const [editedProfile, setEditedProfile] = useState<UserProfile | null>(null)

  useEffect(() => {
    if (!isAuthenticated) {
      return
    }

    const fetchProfile = async () => {
      try {
        // TODO: Replace with actual API call
        const mockProfile: UserProfile = {
          firstName: user?.firstName || 'John',
          lastName: user?.lastName || 'Doe',
          email: user?.email || 'john.doe@example.com',
          phone: '+1 (555) 123-4567',
          dateOfBirth: '1990-01-15',
          gender: 'male',
          address: '123 Main Street',
          city: 'New York',
          state: 'NY',
          zipCode: '10001',
          role: (user?.role as 'patient' | 'doctor') || 'patient',
          isVerified: true,
          emergencyContact: {
            name: 'Jane Doe',
            phone: '+1 (555) 987-6543',
            relationship: 'Spouse'
          }
        }
        setProfile(mockProfile)
        setEditedProfile(mockProfile)
      } catch (error) {
        console.error('Failed to fetch profile:', error)
      } finally {
        setIsLoading(false)
      }
    }

    fetchProfile()
  }, [isAuthenticated, user])

  const handleEdit = () => {
    setIsEditing(true)
    setEditedProfile(profile)
  }

  const handleCancel = () => {
    setIsEditing(false)
    setEditedProfile(profile)
  }

  const handleSave = async () => {
    setIsSaving(true)
    try {
      // TODO: Replace with actual API call
      console.log('Saving profile:', editedProfile)
      
      // Simulate API call
      await new Promise(resolve => setTimeout(resolve, 1000))
      
      setProfile(editedProfile)
      setIsEditing(false)
    } catch (error) {
      console.error('Failed to save profile:', error)
    } finally {
      setIsSaving(false)
    }
  }

  const handleInputChange = (field: string, value: string) => {
    if (!editedProfile) return
    
    if (field.includes('.')) {
      const [parent, child] = field.split('.')
      setEditedProfile(prev => ({
        ...prev!,
        [parent]: {
          ...prev![parent as keyof UserProfile] as any,
          [child]: value
        }
      }))
    } else {
      setEditedProfile(prev => ({
        ...prev!,
        [field]: value
      }))
    }
  }

  if (!isAuthenticated) {
    return (
      <div className="min-h-screen flex items-center justify-center">
        <div className="text-center">
          <h2 className="text-2xl font-bold text-gray-900">Please log in</h2>
          <p className="mt-2 text-gray-600">You need to be logged in to view your profile.</p>
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

  if (!profile) {
    return (
      <div className="min-h-screen flex items-center justify-center">
        <div className="text-center">
          <h2 className="text-2xl font-bold text-gray-900">Profile not found</h2>
          <p className="mt-2 text-gray-600">Unable to load your profile information.</p>
        </div>
      </div>
    )
  }

  const currentProfile = isEditing ? editedProfile : profile

  return (
    <div className="min-h-screen bg-gray-50">
      <div className="max-w-4xl mx-auto px-4 sm:px-6 lg:px-8 py-8">
        {/* Header */}
        <div className="mb-8">
          <div className="flex items-center justify-between">
            <div>
              <h1 className="text-3xl font-bold text-gray-900">My Profile</h1>
              <p className="mt-2 text-gray-600">
                Manage your personal information and preferences
              </p>
            </div>
            <div className="flex items-center space-x-2">
              {profile.isVerified && (
                <Badge variant="default" className="flex items-center">
                  <Shield className="h-3 w-3 mr-1" />
                  Verified
                </Badge>
              )}
              {!isEditing ? (
                <Button onClick={handleEdit}>
                  <Edit className="h-4 w-4 mr-2" />
                  Edit Profile
                </Button>
              ) : (
                <div className="flex space-x-2">
                  <Button variant="outline" onClick={handleCancel}>
                    <X className="h-4 w-4 mr-2" />
                    Cancel
                  </Button>
                  <Button onClick={handleSave} disabled={isSaving}>
                    <Save className="h-4 w-4 mr-2" />
                    {isSaving ? 'Saving...' : 'Save Changes'}
                  </Button>
                </div>
              )}
            </div>
          </div>
        </div>

        <div className="grid grid-cols-1 lg:grid-cols-3 gap-8">
          {/* Main Profile Information */}
          <div className="lg:col-span-2 space-y-6">
            {/* Personal Information */}
            <Card>
              <CardHeader>
                <CardTitle className="flex items-center gap-2">
                  <User className="h-5 w-5" />
                  Personal Information
                </CardTitle>
                <CardDescription>
                  Your basic personal details
                </CardDescription>
              </CardHeader>
              <CardContent className="space-y-4">
                <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
                  <div>
                    <label className="block text-sm font-medium text-gray-700 mb-1">
                      First Name
                    </label>
                    {isEditing ? (
                      <Input
                        value={currentProfile?.firstName || ''}
                        onChange={(e) => handleInputChange('firstName', e.target.value)}
                      />
                    ) : (
                      <p className="text-gray-900">{profile.firstName}</p>
                    )}
                  </div>
                  <div>
                    <label className="block text-sm font-medium text-gray-700 mb-1">
                      Last Name
                    </label>
                    {isEditing ? (
                      <Input
                        value={currentProfile?.lastName || ''}
                        onChange={(e) => handleInputChange('lastName', e.target.value)}
                      />
                    ) : (
                      <p className="text-gray-900">{profile.lastName}</p>
                    )}
                  </div>
                </div>

                <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
                  <div>
                    <label className="block text-sm font-medium text-gray-700 mb-1">
                      Email Address
                    </label>
                    <div className="flex items-center">
                      <Mail className="h-4 w-4 text-gray-400 mr-2" />
                      <p className="text-gray-900">{profile.email}</p>
                    </div>
                    <p className="text-xs text-gray-500 mt-1">Email cannot be changed</p>
                  </div>
                  <div>
                    <label className="block text-sm font-medium text-gray-700 mb-1">
                      Phone Number
                    </label>
                    {isEditing ? (
                      <Input
                        value={currentProfile?.phone || ''}
                        onChange={(e) => handleInputChange('phone', e.target.value)}
                      />
                    ) : (
                      <div className="flex items-center">
                        <Phone className="h-4 w-4 text-gray-400 mr-2" />
                        <p className="text-gray-900">{profile.phone}</p>
                      </div>
                    )}
                  </div>
                </div>

                <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
                  <div>
                    <label className="block text-sm font-medium text-gray-700 mb-1">
                      Date of Birth
                    </label>
                    {isEditing ? (
                      <Input
                        type="date"
                        value={currentProfile?.dateOfBirth || ''}
                        onChange={(e) => handleInputChange('dateOfBirth', e.target.value)}
                      />
                    ) : (
                      <div className="flex items-center">
                        <Calendar className="h-4 w-4 text-gray-400 mr-2" />
                        <p className="text-gray-900">{profile.dateOfBirth}</p>
                      </div>
                    )}
                  </div>
                  <div>
                    <label className="block text-sm font-medium text-gray-700 mb-1">
                      Gender
                    </label>
                    {isEditing ? (
                      <Select value={currentProfile?.gender || 'other'} onValueChange={(value) => handleInputChange('gender', value)}>
                        <SelectTrigger>
                          <SelectValue />
                        </SelectTrigger>
                        <SelectContent>
                          <SelectItem value="male">Male</SelectItem>
                          <SelectItem value="female">Female</SelectItem>
                          <SelectItem value="other">Other</SelectItem>
                        </SelectContent>
                      </Select>
                    ) : (
                      <p className="text-gray-900 capitalize">{profile.gender}</p>
                    )}
                  </div>
                </div>
              </CardContent>
            </Card>

            {/* Address Information */}
            <Card>
              <CardHeader>
                <CardTitle className="flex items-center gap-2">
                  <MapPin className="h-5 w-5" />
                  Address Information
                </CardTitle>
                <CardDescription>
                  Your residential address
                </CardDescription>
              </CardHeader>
              <CardContent className="space-y-4">
                <div>
                  <label className="block text-sm font-medium text-gray-700 mb-1">
                    Street Address
                  </label>
                  {isEditing ? (
                    <Input
                      value={currentProfile?.address || ''}
                      onChange={(e) => handleInputChange('address', e.target.value)}
                    />
                  ) : (
                    <p className="text-gray-900">{profile.address}</p>
                  )}
                </div>

                <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
                  <div>
                    <label className="block text-sm font-medium text-gray-700 mb-1">
                      City
                    </label>
                    {isEditing ? (
                      <Input
                        value={currentProfile?.city || ''}
                        onChange={(e) => handleInputChange('city', e.target.value)}
                      />
                    ) : (
                      <p className="text-gray-900">{profile.city}</p>
                    )}
                  </div>
                  <div>
                    <label className="block text-sm font-medium text-gray-700 mb-1">
                      State
                    </label>
                    {isEditing ? (
                      <Input
                        value={currentProfile?.state || ''}
                        onChange={(e) => handleInputChange('state', e.target.value)}
                      />
                    ) : (
                      <p className="text-gray-900">{profile.state}</p>
                    )}
                  </div>
                  <div>
                    <label className="block text-sm font-medium text-gray-700 mb-1">
                      ZIP Code
                    </label>
                    {isEditing ? (
                      <Input
                        value={currentProfile?.zipCode || ''}
                        onChange={(e) => handleInputChange('zipCode', e.target.value)}
                      />
                    ) : (
                      <p className="text-gray-900">{profile.zipCode}</p>
                    )}
                  </div>
                </div>
              </CardContent>
            </Card>

            {/* Emergency Contact */}
            <Card>
              <CardHeader>
                <CardTitle>Emergency Contact</CardTitle>
                <CardDescription>
                  Contact information for emergencies
                </CardDescription>
              </CardHeader>
              <CardContent className="space-y-4">
                <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
                  <div>
                    <label className="block text-sm font-medium text-gray-700 mb-1">
                      Contact Name
                    </label>
                    {isEditing ? (
                      <Input
                        value={currentProfile?.emergencyContact.name || ''}
                        onChange={(e) => handleInputChange('emergencyContact.name', e.target.value)}
                      />
                    ) : (
                      <p className="text-gray-900">{profile.emergencyContact.name}</p>
                    )}
                  </div>
                  <div>
                    <label className="block text-sm font-medium text-gray-700 mb-1">
                      Relationship
                    </label>
                    {isEditing ? (
                      <Input
                        value={currentProfile?.emergencyContact.relationship || ''}
                        onChange={(e) => handleInputChange('emergencyContact.relationship', e.target.value)}
                      />
                    ) : (
                      <p className="text-gray-900">{profile.emergencyContact.relationship}</p>
                    )}
                  </div>
                </div>
                <div>
                  <label className="block text-sm font-medium text-gray-700 mb-1">
                    Phone Number
                  </label>
                  {isEditing ? (
                    <Input
                      value={currentProfile?.emergencyContact.phone || ''}
                      onChange={(e) => handleInputChange('emergencyContact.phone', e.target.value)}
                    />
                  ) : (
                    <div className="flex items-center">
                      <Phone className="h-4 w-4 text-gray-400 mr-2" />
                      <p className="text-gray-900">{profile.emergencyContact.phone}</p>
                    </div>
                  )}
                </div>
              </CardContent>
            </Card>
          </div>

          {/* Sidebar */}
          <div className="space-y-6">
            {/* Account Status */}
            <Card>
              <CardHeader>
                <CardTitle>Account Status</CardTitle>
              </CardHeader>
              <CardContent className="space-y-4">
                <div className="flex items-center justify-between">
                  <span className="text-sm text-gray-600">Account Type</span>
                  <Badge variant="outline" className="capitalize">
                    {profile.role}
                  </Badge>
                </div>
                <div className="flex items-center justify-between">
                  <span className="text-sm text-gray-600">Verification</span>
                  <Badge variant={profile.isVerified ? "default" : "secondary"}>
                    {profile.isVerified ? "Verified" : "Pending"}
                  </Badge>
                </div>
                <div className="flex items-center justify-between">
                  <span className="text-sm text-gray-600">Member Since</span>
                  <span className="text-sm text-gray-900">Jan 2024</span>
                </div>
              </CardContent>
            </Card>

            {/* Security */}
            <Card>
              <CardHeader>
                <CardTitle>Security</CardTitle>
              </CardHeader>
              <CardContent className="space-y-3">
                <Button variant="outline" className="w-full">
                  Change Password
                </Button>
                <Button variant="outline" className="w-full">
                  Two-Factor Authentication
                </Button>
                <Button variant="outline" className="w-full">
                  Privacy Settings
                </Button>
              </CardContent>
            </Card>
          </div>
        </div>
      </div>
    </div>
  )
}
