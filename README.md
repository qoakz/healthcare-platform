# Healthcare Platform - Complete Solution

A comprehensive HIPAA-compliant healthcare platform with patient management, doctor scheduling, video consultations, and medical record management.

## 🚀 Features

- **Patient Management**: Registration, profile management, ID verification
- **Doctor Management**: KYC, availability calendar, specialty management  
- **Appointment Booking**: Search, book, reschedule, cancel appointments
- **Video Consultations**: WebRTC-based video calls with device checks
- **E-Prescriptions**: PDF generation and secure storage
- **Payment Processing**: Stripe/Razorpay integration with refunds
- **Medical Records**: Secure EMR with encounter tracking
- **Notifications**: SMS/Email/Push reminders
- **Admin Dashboard**: User and appointment management

## 🛠 Tech Stack

### Frontend
- **Next.js 14** (App Router)
- **TypeScript**
- **Tailwind CSS**
- **React Query**
- **Zod Validation**

### Backend
- **Django 4.2** + Django REST Framework
- **PostgreSQL**
- **Redis** (Celery)
- **JWT Authentication**

### Infrastructure
- **Docker** & Docker Compose
- **AWS Services** (Cognito, S3, EC2)
- **Vercel** (Frontend Deployment)
- **Railway/Render** (Backend Deployment)

## 🚀 Quick Start

### Prerequisites
- Node.js 18+
- Python 3.11+
- Docker & Docker Compose
- Git

### 1. Clone Repository
```bash
git clone <your-repo-url>
cd healthcare-platform
```

### 2. Backend Setup
```bash
cd api
pip install -r requirements.txt
cp env.example .env
# Edit .env with your configuration
python manage.py migrate
python manage.py runserver
```

### 3. Frontend Setup
```bash
cd app
npm install
cp .env.example .env.local
# Edit .env.local with your configuration
npm run dev
```

### 4. Docker Setup (Alternative)
```bash
docker-compose up -d
```

## 🔧 Environment Configuration

### Backend (.env)
```env
SECRET_KEY=your-secret-key
DEBUG=True
DATABASE_URL=postgresql://user:pass@localhost:5432/healthcare
REDIS_URL=redis://localhost:6379/0
AWS_COGNITO_USER_POOL_ID=your-pool-id
AWS_COGNITO_CLIENT_ID=your-client-id
EMAIL_HOST=smtp.gmail.com
EMAIL_HOST_USER=your-email@gmail.com
EMAIL_HOST_PASSWORD=your-app-password
```

### Frontend (.env.local)
```env
NEXT_PUBLIC_API_URL=http://localhost:8000
NEXT_PUBLIC_COGNITO_DOMAIN=your-cognito-domain
NEXT_PUBLIC_COGNITO_CLIENT_ID=your-client-id
```

## 📱 API Endpoints

### Authentication
- `POST /api/auth/register/` - User registration
- `POST /api/auth/login/` - User login
- `POST /api/auth/token/refresh/` - Refresh JWT token
- `GET /api/auth/me/` - Get current user

### Appointments
- `GET /api/appointments/` - List appointments
- `POST /api/appointments/` - Create appointment
- `GET /api/appointments/{id}/` - Get appointment details

### Doctors
- `GET /api/doctors/` - List doctors
- `POST /api/doctors/register/` - Doctor registration
- `GET /api/doctors/{id}/availability/` - Get doctor availability

## 🚀 Deployment

### Frontend (Vercel)
1. Connect your GitHub repository to Vercel
2. Set environment variables in Vercel dashboard
3. Deploy automatically on push to main branch

### Backend (Railway/Render)
1. Connect your GitHub repository
2. Set environment variables
3. Deploy automatically

### Docker Deployment
```bash
# Build and run with Docker Compose
docker-compose -f docker-compose.prod.yml up -d
```

## 🧪 Testing

### Run Tests
```bash
# Backend tests
cd api
python manage.py test

# Frontend tests
cd app
npm test

# E2E tests
npm run test:e2e
```

### Test Registration
```bash
node test_registration.js
```

## 📁 Project Structure

```
healthcare-platform/
├── app/                    # Next.js frontend
│   ├── app/               # App router pages
│   ├── components/        # React components
│   ├── hooks/            # Custom hooks
│   ├── lib/              # Utilities
│   └── types/            # TypeScript types
├── api/                   # Django backend
│   ├── users/            # User management
│   ├── appointments/     # Appointment system
│   ├── doctors/          # Doctor management
│   ├── emr/              # Medical records
│   ├── payments/         # Payment processing
│   └── notifications/    # Notification system
├── infra/                # Infrastructure configs
├── docker-compose.yml    # Development setup
└── README.md
```

## 🔒 Security Features

- JWT Authentication
- CORS Protection
- Input Validation
- SQL Injection Prevention
- XSS Protection
- Rate Limiting
- Audit Logging

## 📊 Monitoring

- Error Tracking (Sentry)
- Performance Monitoring
- Database Monitoring
- API Analytics

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests
5. Submit a pull request

## 📄 License

This project is licensed under the MIT License.

## 🆘 Support

For support, email support@healthcare-platform.com or create an issue on GitHub.

## 🔄 Recent Updates

- ✅ Fixed user registration functionality
- ✅ Added JWT authentication
- ✅ Enhanced error handling
- ✅ Improved validation
- ✅ Added comprehensive testing

---

**Ready to deploy?** Follow the deployment guide above to get your healthcare platform live! 🚀