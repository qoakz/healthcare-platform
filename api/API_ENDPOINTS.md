# Healthcare Platform API Endpoints

This document provides a comprehensive overview of all API endpoints implemented in the Healthcare Platform.

## Authentication Endpoints (`/api/auth/`)

### User Management
- `POST /api/auth/register/` - User registration
- `GET /api/auth/me/` - Get current user profile
- `GET /api/auth/profile/` - Get/update user profile
- `GET /api/auth/list/` - List users (admin only)
- `POST /api/auth/cognito/callback/` - AWS Cognito OIDC callback
- `POST /api/auth/verify/phone/` - Verify phone number
- `POST /api/auth/verify/identity/` - Verify identity documents

## Doctor Endpoints (`/api/doctors/`)

### Doctor Management
- `GET /api/doctors/` - List all doctors with filtering and search
- `POST /api/doctors/register/` - Doctor registration
- `GET /api/doctors/profile/` - Get/update doctor's own profile
- `GET /api/doctors/{id}/` - Get doctor details
- `GET /api/doctors/{id}/availability/` - Get available time slots for a doctor
- `GET /api/doctors/{id}/reviews/` - Get reviews for a specific doctor
- `POST /api/doctors/{id}/reviews/create/` - Create a review for a doctor

### Doctor Availability
- `GET /api/doctors/availability/` - Manage doctor's availability schedule
- `POST /api/doctors/availability/` - Create availability slot
- `GET /api/doctors/availability/{id}/` - Get/update specific availability slot
- `PUT /api/doctors/availability/{id}/` - Update availability slot
- `DELETE /api/doctors/availability/{id}/` - Delete availability slot

### Doctor KYC
- `POST /api/doctors/kyc/update/` - Update KYC status and documents

## Appointment Endpoints (`/api/appointments/`)

### Appointment Management
- `GET /api/appointments/` - List appointments (filtered by user role)
- `POST /api/appointments/` - Create new appointment
- `GET /api/appointments/upcoming/` - Get upcoming appointments
- `GET /api/appointments/{id}/` - Get/update appointment details
- `POST /api/appointments/{id}/cancel/` - Cancel an appointment
- `POST /api/appointments/{id}/reschedule/` - Reschedule an appointment
- `POST /api/appointments/{id}/start/` - Start an appointment (doctor only)
- `POST /api/appointments/{id}/end/` - End an appointment (doctor only)
- `GET /api/appointments/{id}/reminders/` - Get reminders for an appointment

### Schedule Slots
- `GET /api/appointments/slots/` - List available schedule slots

## EMR (Electronic Medical Records) Endpoints (`/api/emr/`)

### Encounters
- `GET /api/emr/encounters/` - List medical encounters
- `POST /api/emr/encounters/` - Create medical encounter
- `GET /api/emr/encounters/{id}/` - Get/update encounter details
- `PUT /api/emr/encounters/{id}/` - Update encounter details

### Prescriptions
- `GET /api/emr/prescriptions/` - List prescriptions
- `POST /api/emr/prescriptions/` - Create prescription
- `GET /api/emr/prescriptions/{id}/` - Get/update prescription details
- `PUT /api/emr/prescriptions/{id}/` - Update prescription details
- `POST /api/emr/prescriptions/{id}/pdf/` - Generate prescription PDF

### Medical Documents
- `GET /api/emr/documents/` - List medical documents
- `POST /api/emr/documents/` - Upload medical document
- `GET /api/emr/documents/{id}/` - Get/update/delete medical document
- `PUT /api/emr/documents/{id}/` - Update medical document
- `DELETE /api/emr/documents/{id}/` - Delete medical document
- `GET /api/emr/documents/{id}/download/` - Get presigned URL for document download

### Medical History
- `GET /api/emr/medical-history/{patient_id}/` - Get/update patient's medical history
- `PUT /api/emr/medical-history/{patient_id}/` - Update medical history

### Vitals
- `GET /api/emr/vitals/` - List vital signs
- `POST /api/emr/vitals/` - Record vital signs
- `GET /api/emr/vitals/{id}/` - Get/update vital signs
- `PUT /api/emr/vitals/{id}/` - Update vital signs

### Medical Summary
- `GET /api/emr/summary/{patient_id}/` - Get comprehensive medical summary for a patient

## Payment Endpoints (`/api/payments/`)

### Payment Transactions
- `GET /api/payments/transactions/` - List payment transactions
- `POST /api/payments/transactions/` - Create payment transaction
- `GET /api/payments/transactions/{id}/` - Get payment transaction details
- `POST /api/payments/intent/` - Create payment intent for an appointment

### Refunds
- `GET /api/payments/refunds/` - List refunds (admin only)
- `POST /api/payments/refunds/` - Create refund (admin only)
- `GET /api/payments/refunds/{id}/` - Get/update refund details (admin only)
- `PUT /api/payments/refunds/{id}/` - Update refund details (admin only)
- `POST /api/payments/transactions/{id}/refund/` - Process refund for a payment

### Doctor Payouts
- `GET /api/payments/payouts/` - List doctor payouts (admin only)
- `POST /api/payments/payouts/` - Create doctor payout (admin only)
- `GET /api/payments/payouts/{id}/` - Get/update doctor payout details (admin only)
- `PUT /api/payments/payouts/{id}/` - Update doctor payout details (admin only)
- `POST /api/payments/payouts/generate/` - Generate payout for a doctor for a specific period

### Doctor Earnings
- `GET /api/payments/earnings/` - Get doctor's earnings summary

### Webhooks
- `POST /api/payments/webhooks/` - Handle payment webhooks from external providers

## Notification Endpoints (`/api/notifications/`)

### Notifications
- `GET /api/notifications/` - List notifications
- `POST /api/notifications/` - Create notification
- `GET /api/notifications/{id}/` - Get/update/delete notification details
- `PUT /api/notifications/{id}/` - Update notification
- `DELETE /api/notifications/{id}/` - Delete notification

### Notification Management
- `GET /api/notifications/unread/` - Get unread notifications for current user
- `POST /api/notifications/{id}/read/` - Mark a notification as read
- `POST /api/notifications/mark-all-read/` - Mark all notifications as read for current user

### Admin Notification Functions
- `POST /api/notifications/send/` - Send a notification to a user (admin only)
- `POST /api/notifications/send-bulk/` - Send a notification to multiple users (admin only)
- `GET /api/notifications/stats/` - Get notification statistics (admin only)

## RTC (Real-Time Communication) Endpoints (`/api/rtc/`)

### RTC Rooms
- `GET /api/rtc/rooms/` - List RTC rooms
- `POST /api/rtc/rooms/` - Create RTC room
- `GET /api/rtc/rooms/{id}/` - Get/update RTC room details
- `PUT /api/rtc/rooms/{id}/` - Update RTC room details
- `POST /api/rtc/rooms/appointment/{id}/` - Create an RTC room for a specific appointment
- `POST /api/rtc/rooms/{room_id}/join/` - Join an RTC room
- `POST /api/rtc/rooms/{room_id}/start/` - Start an RTC room (doctor only)
- `POST /api/rtc/rooms/{room_id}/end/` - End an RTC room
- `GET /api/rtc/rooms/{room_id}/status/` - Get current status of an RTC room
- `GET /api/rtc/rooms/{room_id}/signals/` - Get signals for a specific room

### RTC Signals
- `GET /api/rtc/signals/` - List RTC signals
- `POST /api/rtc/signals/` - Create RTC signal

### RTC Join Tokens
- `GET /api/rtc/join-tokens/` - List RTC join tokens
- `POST /api/rtc/join-tokens/` - Create RTC join token

## Audit Endpoints (`/api/audit/`)

### Audit Logs
- `GET /api/audit/logs/` - List audit logs (admin only)
- `GET /api/audit/stats/` - Get audit log statistics (admin only)

## WebSocket Endpoints (`/ws/`)

### RTC WebSocket
- `ws://localhost:8000/ws/rtc/{room_id}/` - WebSocket connection for RTC signaling

## Authentication & Permissions

### User Roles
- **Patient**: Can access their own data and book appointments
- **Doctor**: Can access their patients' data and manage their profile
- **Admin**: Can access all data and manage the system

### Permission Classes
- `IsAuthenticated`: User must be logged in
- `IsPatient`: User must be a patient
- `IsDoctor`: User must be a doctor
- `IsAdmin`: User must be an admin
- `IsDoctorOrPatient`: User must be either a doctor or patient
- `IsOwnerOrReadOnly`: User can only modify their own data

### Authentication Methods
- **AWS Cognito**: Primary authentication method
- **JWT Tokens**: For API access after Cognito authentication
- **Session Authentication**: For Django admin and development

## Response Formats

All API endpoints return JSON responses with the following structure:

### Success Response
```json
{
    "data": {...},
    "message": "Success message",
    "status": "success"
}
```

### Error Response
```json
{
    "error": "Error message",
    "details": {...},
    "status": "error"
}
```

### Pagination
List endpoints support pagination with the following parameters:
- `page`: Page number
- `page_size`: Number of items per page

## Filtering and Search

Most list endpoints support filtering and search:

### Common Filters
- `status`: Filter by status
- `created_at`: Filter by creation date
- `updated_at`: Filter by update date

### Search Fields
- Text search across relevant fields
- Use `search` query parameter

### Ordering
- Use `ordering` query parameter
- Prefix with `-` for descending order
- Example: `?ordering=-created_at`

## Rate Limiting

API endpoints are rate-limited to prevent abuse:
- **Authentication endpoints**: 5 requests per minute
- **General endpoints**: 100 requests per minute
- **File upload endpoints**: 10 requests per minute

## CORS Configuration

CORS is configured to allow requests from:
- `http://localhost:3000` (development)
- `https://yourdomain.com` (production)

## Webhook Security

Webhook endpoints verify signatures from external providers:
- **Stripe**: Verify webhook signature
- **Razorpay**: Verify webhook signature

## Data Validation

All endpoints use Django REST Framework serializers for:
- Input validation
- Data sanitization
- Output formatting

## Error Handling

The API provides comprehensive error handling:
- **400 Bad Request**: Invalid input data
- **401 Unauthorized**: Authentication required
- **403 Forbidden**: Insufficient permissions
- **404 Not Found**: Resource not found
- **500 Internal Server Error**: Server error

## Development vs Production

### Development
- Debug mode enabled
- Detailed error messages
- CORS allows all origins
- No rate limiting

### Production
- Debug mode disabled
- Generic error messages
- Restricted CORS origins
- Rate limiting enabled
- HTTPS required
