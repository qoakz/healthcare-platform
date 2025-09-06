// User types
export interface User {
  id: number
  username: string
  email: string
  first_name: string
  last_name: string
  role: 'patient' | 'doctor' | 'admin'
  phone: string
  date_of_birth?: string
  gender?: 'M' | 'F' | 'O' | 'N'
  is_phone_verified: boolean
  is_email_verified: boolean
  is_identity_verified: boolean
  created_at: string
  profile?: UserProfile
}

export interface UserProfile {
  profile_image?: string
  blood_type?: string
  allergies?: string
  medical_conditions?: string
  current_medications?: string
  preferred_language: string
  timezone: string
  share_medical_history: boolean
  allow_telemedicine: boolean
}

// Doctor types
export interface Doctor {
  id: number
  user: User
  registration_number: string
  years_of_experience: number
  specialties: string[]
  clinic_name?: string
  clinic_address?: string
  consultation_fee: number
  kyc_status: 'pending' | 'verified' | 'rejected'
  is_available_for_consultation: boolean
  average_rating: number
  total_reviews: number
  availability?: DoctorAvailability[]
  reviews?: DoctorReview[]
}

export interface DoctorAvailability {
  id: number
  day_of_week: number
  start_time: string
  end_time: string
  is_available: boolean
  break_times: Array<{ start: string; end: string }>
}

export interface DoctorReview {
  id: number
  patient_name: string
  rating: number
  comment?: string
  communication_rating?: number
  treatment_rating?: number
  punctuality_rating?: number
  is_anonymous: boolean
  created_at: string
}

// Appointment types
export interface Appointment {
  id: number
  patient: User
  doctor: Doctor
  slot: ScheduleSlot
  appointment_type: 'video' | 'in_person'
  status: 'pending' | 'confirmed' | 'in_progress' | 'completed' | 'cancelled' | 'no_show' | 'refunded'
  reason: string
  symptoms?: string
  medical_history?: string
  video_room_id?: string
  consultation_fee: number
  payment_status: string
  scheduled_at: string
  started_at?: string
  ended_at?: string
  doctor_notes?: string
  patient_feedback?: string
  requires_follow_up: boolean
  follow_up_date?: string
  duration_minutes?: number
  is_upcoming: boolean
  can_be_cancelled: boolean
  can_be_rescheduled: boolean
  created_at: string
}

export interface ScheduleSlot {
  id: number
  doctor: number
  doctor_name: string
  start_time: string
  end_time: string
  status: 'open' | 'booked' | 'blocked'
  duration_minutes: number
  notes?: string
  is_available: boolean
}

// EMR types
export interface Encounter {
  id: number
  appointment: number
  encounter_type: 'consultation' | 'follow_up' | 'emergency' | 'routine'
  chief_complaint: string
  history_of_present_illness?: string
  vital_signs: Record<string, any>
  physical_examination?: string
  assessment: string
  diagnosis_codes: string[]
  plan: string
  clinical_notes?: string
  follow_up_instructions?: string
  created_by: number
  created_at: string
  updated_at: string
}

export interface Prescription {
  id: number
  encounter: number
  medications: Array<{
    name: string
    dosage: string
    frequency: string
    duration: string
    instructions?: string
  }>
  instructions: string
  prescription_date: string
  valid_until: string
  refills_allowed: number
  status: 'active' | 'completed' | 'cancelled' | 'expired'
  pdf_url?: string
  pdf_generated_at?: string
  prescribed_by: number
  created_at: string
  updated_at: string
}

// Payment types
export interface PaymentTransaction {
  id: number
  provider: 'stripe' | 'razorpay'
  amount: number
  currency: string
  status: 'pending' | 'processing' | 'completed' | 'failed' | 'cancelled' | 'refunded'
  external_id: string
  client_secret?: string
  appointment?: number
  patient: number
  description?: string
  metadata: Record<string, any>
  created_at: string
  updated_at: string
  completed_at?: string
}

// API Response types
export interface ApiResponse<T> {
  data: T
  message?: string
  status: number
}

export interface PaginatedResponse<T> {
  results: T[]
  count: number
  next?: string
  previous?: string
}

// Form types
export interface LoginForm {
  email: string
  password: string
}

export interface RegisterForm {
  username: string
  email: string
  password: string
  password_confirm: string
  first_name: string
  last_name: string
  phone: string
  date_of_birth?: string
  gender?: 'M' | 'F' | 'O' | 'N'
  role: 'patient' | 'doctor'
}

export interface AppointmentForm {
  slot_id: number
  appointment_type: 'video' | 'in_person'
  reason: string
  symptoms?: string
  medical_history?: string
}

// WebRTC types
export interface RTCSignal {
  type: 'offer' | 'answer' | 'ice_candidate' | 'join' | 'leave'
  payload: any
}

export interface RTCJoinToken {
  token: string
  expires_at: string
  room_id: string
}
