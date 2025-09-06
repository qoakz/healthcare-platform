'use client'

import React, { useState, useEffect, createContext, useContext, ReactNode } from 'react'

interface User {
  id: string
  email: string
  firstName: string
  lastName: string
  role: 'patient' | 'doctor' | 'admin'
  isVerified: boolean
  cognitoSub?: string
}

interface AuthContextType {
  user: User | null
  isAuthenticated: boolean
  isLoading: boolean
  signIn: (email: string, password: string) => Promise<void>
  signUp: (userData: any) => Promise<void>
  signOut: () => Promise<void>
  handleCognitoCallback: (code: string) => Promise<void>
}

const AuthContext = createContext<AuthContextType | undefined>(undefined)

export function AuthProvider({ children }: { children: ReactNode }) {
  const [user, setUser] = useState<User | null>(null)
  const [isLoading, setIsLoading] = useState(true)

  useEffect(() => {
    // Check for existing authentication on mount
    const checkAuth = async () => {
      try {
        // TODO: Implement actual authentication check
        const storedUser = localStorage.getItem('user')
        if (storedUser && storedUser.trim() !== '') {
          try {
            const parsedUser = JSON.parse(storedUser)
            setUser(parsedUser)
          } catch (parseError) {
            console.error('Failed to parse stored user data:', parseError)
            // Clear corrupted data
            localStorage.removeItem('user')
          }
        }
      } catch (error) {
        console.error('Auth check failed:', error)
      } finally {
        setIsLoading(false)
      }
    }

    checkAuth()
  }, [])

  const signIn = async (email: string, password: string) => {
    try {
      // TODO: Replace with actual API call to Django backend
      console.log('Signing in:', email, password)
      
      // Mock authentication - replace with real implementation
      const mockUser: User = {
        id: '1',
        email,
        firstName: 'John',
        lastName: 'Doe',
        role: 'patient',
        isVerified: true,
        cognitoSub: 'mock-cognito-sub'
      }
      
      setUser(mockUser)
      localStorage.setItem('user', JSON.stringify(mockUser))
    } catch (error) {
      throw new Error('Sign in failed')
    }
  }

  const signUp = async (userData: any) => {
    try {
      // TODO: Replace with actual API call to Django backend
      console.log('Signing up:', userData)
    } catch (error) {
      throw new Error('Sign up failed')
    }
  }

  const signOut = async () => {
    try {
      setUser(null)
      localStorage.removeItem('user')
    } catch (error) {
      throw new Error('Sign out failed')
    }
  }

  const handleCognitoCallback = async (code: string) => {
    try {
      console.log('Handling Cognito callback with code:', code)
      
      const mockUser: User = {
        id: '1',
        email: 'user@example.com',
        firstName: 'John',
        lastName: 'Doe',
        role: 'patient',
        isVerified: true,
        cognitoSub: 'cognito-sub-123'
      }
      
      setUser(mockUser)
      localStorage.setItem('user', JSON.stringify(mockUser))
    } catch (error) {
      throw new Error('Authentication callback failed')
    }
  }

  const contextValue = {
    user,
    isAuthenticated: !!user,
    isLoading,
    signIn,
    signUp,
    signOut,
    handleCognitoCallback
  }

  return React.createElement(AuthContext.Provider, { value: contextValue }, children)
}

export function useAuth() {
  const context = useContext(AuthContext)
  if (context === undefined) {
    throw new Error('useAuth must be used within an AuthProvider')
  }
  return context
}
