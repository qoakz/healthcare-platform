'use client'
import React, { useEffect, useState } from 'react'
import { useParams, useRouter } from 'next/navigation'
import { VideoCall } from '@/components/video-call/video-call'
import { useAuth } from '@/hooks/use-auth-simple'
import { LoadingSpinner } from '@/components/ui/loading-spinner'

export default function CallPage() {
  const params = useParams()
  const router = useRouter()
  const { user, isLoading } = useAuth()
  const [isValidating, setIsValidating] = useState(true)
  const [validationError, setValidationError] = useState<string | null>(null)

  const roomId = params.roomId as string

  useEffect(() => {
    const validateCall = async () => {
      if (isLoading) return

      if (!user) {
        setValidationError('You must be logged in to join a call')
        setIsValidating(false)
        return
      }

      if (!roomId) {
        setValidationError('Invalid room ID')
        setIsValidating(false)
        return
      }

      // TODO: Validate that the user has permission to join this room
      // This would typically involve checking if the user is the patient or doctor
      // for the appointment associated with this room

      setIsValidating(false)
    }

    validateCall()
  }, [user, isLoading, roomId])

  const handleEndCall = () => {
    router.push('/appointments')
  }

  if (isLoading || isValidating) {
    return (
      <div className="min-h-screen flex items-center justify-center bg-gray-900">
        <div className="text-center">
          <LoadingSpinner size="lg" />
          <p className="mt-4 text-white">Joining call...</p>
        </div>
      </div>
    )
  }

  if (validationError) {
    return (
      <div className="min-h-screen flex items-center justify-center bg-gray-900">
        <div className="text-center">
          <div className="w-16 h-16 bg-red-500 rounded-full flex items-center justify-center mx-auto mb-4">
            <span className="text-white text-2xl">!</span>
          </div>
          <h2 className="text-2xl font-bold text-white mb-2">Cannot Join Call</h2>
          <p className="text-gray-300 mb-4">{validationError}</p>
          <button
            onClick={() => router.push('/appointments')}
            className="px-6 py-2 bg-blue-600 text-white rounded-lg hover:bg-blue-700"
          >
            Back to Appointments
          </button>
        </div>
      </div>
    )
  }

  if (!user) {
    return (
      <div className="min-h-screen flex items-center justify-center bg-gray-900">
        <div className="text-center">
          <h2 className="text-2xl font-bold text-white mb-4">Please log in to join the call</h2>
          <button
            onClick={() => router.push('/auth/login')}
            className="px-6 py-2 bg-blue-600 text-white rounded-lg hover:bg-blue-700"
          >
            Login
          </button>
        </div>
      </div>
    )
  }

  return (
    <VideoCall
      roomId={roomId}
      userId={user.id}
      isDoctor={user.role === 'doctor'}
      onEndCall={handleEndCall}
    />
  )
}

