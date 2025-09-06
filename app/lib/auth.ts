import { Amplify } from 'aws-amplify'
import { getCurrentUser, signIn, signUp, signOut, confirmSignUp, resendSignUpCode } from 'aws-amplify/auth'

// Configure Amplify
Amplify.configure({
  Auth: {
    Cognito: {
      userPoolId: process.env.NEXT_PUBLIC_AWS_USER_POOL_ID!,
      userPoolClientId: process.env.NEXT_PUBLIC_AWS_USER_POOL_WEB_CLIENT_ID!,
    }
  }
})

export interface AuthUser {
  userId: string
  username: string
  email: string
  emailVerified: boolean
  phoneNumber?: string
  phoneNumberVerified?: boolean
}

export interface SignUpParams {
  username: string
  password: string
  email: string
  phoneNumber?: string
  givenName?: string
  familyName?: string
}

export interface SignInParams {
  username: string
  password: string
}

export class AuthService {
  static async getCurrentUser(): Promise<AuthUser | null> {
    try {
      const user = await getCurrentUser()
      return {
        userId: user.userId,
        username: user.username,
        email: user.signInDetails?.loginId || '',
        emailVerified: user.signInDetails?.loginId ? true : false,
        phoneNumber: user.signInDetails?.loginId,
        phoneNumberVerified: false,
      }
    } catch (error) {
      return null
    }
  }

  static async signIn({ username, password }: SignInParams) {
    try {
      const result = await signIn({ username, password })
      return result
    } catch (error) {
      throw error
    }
  }

  static async signUp({ username, password, email, phoneNumber, givenName, familyName }: SignUpParams) {
    try {
      const result = await signUp({
        username,
        password,
        options: {
          userAttributes: {
            email,
            phone_number: phoneNumber,
            given_name: givenName,
            family_name: familyName,
          },
        },
      })
      return result
    } catch (error) {
      throw error
    }
  }

  static async confirmSignUp(username: string, confirmationCode: string) {
    try {
      const result = await confirmSignUp({ username, confirmationCode })
      return result
    } catch (error) {
      throw error
    }
  }

  static async resendSignUpCode(username: string) {
    try {
      const result = await resendSignUpCode({ username })
      return result
    } catch (error) {
      throw error
    }
  }

  static async signOut() {
    try {
      await signOut()
    } catch (error) {
      throw error
    }
  }

  static async getAccessToken(): Promise<string | null> {
    try {
      const user = await getCurrentUser()
      // In a real implementation, you would get the access token from the user session
      // For now, we'll return null and handle this in the API layer
      return null
    } catch (error) {
      return null
    }
  }
}
