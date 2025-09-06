'use client'

import { useEffect, useState } from 'react'
import { useAuth } from '@/hooks/use-auth-simple'
import { useRouter } from 'next/navigation'
import { PatientDashboard } from '@/components/dashboard/patient-dashboard'
import { DoctorDashboard } from '@/components/dashboard/doctor-dashboard'
import { LoadingSpinner } from '@/components/ui/loading-spinner'

export default function DashboardPage() {
  const { user, isLoading, isAuthenticated } = useAuth()
  const router = useRouter()
  const [dashboardLoading, setDashboardLoading] = useState(true)

  useEffect(() => {
    if (!isLoading) {
      if (!isAuthenticated) {
        router.push('/auth/login')
        return
      }
      setDashboardLoading(false)
    }
  }, [isAuthenticated, isLoading, router])

  if (isLoading || dashboardLoading) {
    return <LoadingSpinner />
  }

  if (!user) {
    return (
      <div className="min-h-screen flex items-center justify-center">
        <div className="text-center">
          <h2 className="text-2xl font-bold text-gray-900">Access Denied</h2>
          <p className="mt-2 text-gray-600">Please log in to access your dashboard.</p>
        </div>
      </div>
    )
  }

  // Render appropriate dashboard based on user role
  if (user.role === 'doctor') {
    return <DoctorDashboard />
  }

  return <PatientDashboard />
}
