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
      // Validate input
      if (!email || !password) {
        throw new Error('Please enter both email and password')
      }

      // Make API call to Django backend for authentication
      const response = await fetch(`${process.env.NEXT_PUBLIC_API_URL || 'http://localhost:8000'}/api/auth/login/`, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({
          username: email, // Django uses username field
          password: password
        }),
      })

      if (!response.ok) {
        const errorData = await response.json()
        console.error('Login API error:', errorData)
        
        // Handle specific authentication errors
        if (response.status === 401) {
          throw new Error('Invalid email or password')
        }
        if (errorData.detail) {
          throw new Error(errorData.detail)
        }
        if (errorData.non_field_errors) {
          throw new Error(Array.isArray(errorData.non_field_errors) ? errorData.non_field_errors[0] : errorData.non_field_errors)
        }
        
        throw new Error('Login failed')
      }

      const result = await response.json()
      
      // Store tokens
      if (result.access) {
        localStorage.setItem('access_token', result.access)
      }
      if (result.refresh) {
        localStorage.setItem('refresh_token', result.refresh)
      }

      // Get user profile
      const userResponse = await fetch(`${process.env.NEXT_PUBLIC_API_URL || 'http://localhost:8000'}/api/auth/me/`, {
        headers: {
          'Authorization': `Bearer ${result.access}`,
          'Content-Type': 'application/json',
        },
      })

      if (userResponse.ok) {
        const userData = await userResponse.json()
        
        const user: User = {
          id: userData.id.toString(),
          email: userData.email,
          firstName: userData.first_name,
          lastName: userData.last_name,
          role: userData.role,
          isVerified: userData.is_email_verified || false,
          cognitoSub: userData.cognito_sub
        }
        
        setUser(user)
        localStorage.setItem('user', JSON.stringify(user))
      } else {
        throw new Error('Failed to fetch user profile')
      }
    } catch (error) {
      console.error('Login error:', error)
      throw new Error(error instanceof Error ? error.message : 'Sign in failed')
    }
  }

  const signUp = async (userData: any) => {
    try {
      // Validate required fields
      if (!userData.email || !userData.password || !userData.firstName || !userData.lastName) {
        throw new Error('Please fill in all required fields')
      }

      if (userData.password !== userData.confirmPassword) {
        throw new Error('Passwords do not match')
      }

      if (userData.password.length < 8) {
        throw new Error('Password must be at least 8 characters long')
      }

      // Prepare data for Django backend registration
      const registrationData = {
        username: userData.email, // Use email as username
        email: userData.email,
        password: userData.password,
        password_confirm: userData.confirmPassword,
        first_name: userData.firstName,
        last_name: userData.lastName,
        phone: userData.phone || '',
        date_of_birth: userData.dateOfBirth || null,
        gender: userData.gender || 'other',
        role: userData.role || 'patient'
      }

      // Make API call to Django backend
      const response = await fetch(`${process.env.NEXT_PUBLIC_API_URL || 'http://localhost:8000'}/api/auth/register/`, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify(registrationData),
      })

      if (!response.ok) {
        const errorData = await response.json()
        console.error('Registration API error:', errorData)
        
        // Handle specific validation errors
        if (errorData.username) {
          throw new Error('Username already exists. Please use a different email.')
        }
        if (errorData.email) {
          throw new Error('Email already exists. Please use a different email.')
        }
        if (errorData.password) {
          throw new Error(Array.isArray(errorData.password) ? errorData.password[0] : errorData.password)
        }
        if (errorData.non_field_errors) {
          throw new Error(Array.isArray(errorData.non_field_errors) ? errorData.non_field_errors[0] : errorData.non_field_errors)
        }
        
        throw new Error(errorData.detail || errorData.message || 'Registration failed')
      }

      const result = await response.json()
      
      // Create user object for frontend state
      const newUser: User = {
        id: result.id.toString(),
        email: result.email,
        firstName: result.first_name,
        lastName: result.last_name,
        role: result.role,
        isVerified: result.is_email_verified || false,
        cognitoSub: result.cognito_sub
      }

      setUser(newUser)
      localStorage.setItem('user', JSON.stringify(newUser))
      
      console.log('User registered successfully:', newUser)
    } catch (error) {
      console.error('Registration error:', error)
      throw new Error(error instanceof Error ? error.message : 'Registration failed')
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
