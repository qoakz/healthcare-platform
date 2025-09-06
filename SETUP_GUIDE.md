# Healthcare Platform Setup Guide

This guide will walk you through setting up and running the Healthcare Appointment & Telemedicine Platform step by step.

## Prerequisites

Before you begin, ensure you have the following installed:

- **Docker** and **Docker Compose** (for containerized development)
- **Node.js** (v18 or higher) and **npm**
- **Python** (v3.11 or higher) and **pip**
- **Git** (for version control)
- **AWS Account** (for Cognito, S3, and other services)

## Step 1: Environment Setup

### 1.1 Clone and Navigate to Project
```bash
cd "D:\health care platform"
```

### 1.2 Create Environment Files
Create the following environment files:

**Backend Environment (`api/.env`):**
```bash
# Database
DATABASE_URL=postgresql://healthcare_user:healthcare_pass@db:5432/healthcare_db

# Django Settings
SECRET_KEY=your-secret-key-here
DEBUG=True
ALLOWED_HOSTS=localhost,127.0.0.1,0.0.0.0

# AWS Configuration
AWS_ACCESS_KEY_ID=your-aws-access-key
AWS_SECRET_ACCESS_KEY=your-aws-secret-key
AWS_STORAGE_BUCKET_NAME=your-s3-bucket-name
AWS_S3_REGION_NAME=us-east-1

# AWS Cognito
COGNITO_USER_POOL_ID=your-cognito-user-pool-id
COGNITO_CLIENT_ID=your-cognito-client-id
COGNITO_CLIENT_SECRET=your-cognito-client-secret
COGNITO_REGION=us-east-1

# Redis
REDIS_URL=redis://redis:6379/0

# Email Configuration (for notifications)
EMAIL_HOST=smtp.gmail.com
EMAIL_PORT=587
EMAIL_USE_TLS=True
EMAIL_HOST_USER=your-email@gmail.com
EMAIL_HOST_PASSWORD=your-app-password

# SMS Configuration (Twilio)
TWILIO_ACCOUNT_SID=your-twilio-account-sid
TWILIO_AUTH_TOKEN=your-twilio-auth-token
TWILIO_PHONE_NUMBER=your-twilio-phone-number

# Payment Providers
STRIPE_PUBLISHABLE_KEY=your-stripe-publishable-key
STRIPE_SECRET_KEY=your-stripe-secret-key
STRIPE_WEBHOOK_SECRET=your-stripe-webhook-secret

# WebRTC Configuration
STUN_SERVER=stun:stun.l.google.com:19302
TURN_SERVER=turn:your-turn-server.com:3478
TURN_USERNAME=your-turn-username
TURN_PASSWORD=your-turn-password
```

**Frontend Environment (`app/.env.local`):**
```bash
# API Configuration
NEXT_PUBLIC_API_URL=http://localhost:8000/api
NEXT_PUBLIC_WS_URL=ws://localhost:8000/ws

# AWS Cognito
NEXT_PUBLIC_COGNITO_USER_POOL_ID=your-cognito-user-pool-id
NEXT_PUBLIC_COGNITO_CLIENT_ID=your-cognito-client-id
NEXT_PUBLIC_COGNITO_REGION=us-east-1

# Stripe
NEXT_PUBLIC_STRIPE_PUBLISHABLE_KEY=your-stripe-publishable-key

# App Configuration
NEXT_PUBLIC_APP_NAME=Healthcare Platform
NEXT_PUBLIC_APP_URL=http://localhost:3000
```

## Step 2: AWS Services Setup

### 2.1 AWS Cognito Setup
1. Go to AWS Cognito Console
2. Create a new User Pool:
   - **Pool name**: `healthcare-platform-users`
   - **Sign-in options**: Email
   - **Password policy**: Custom (8+ characters)
   - **MFA**: Optional
   - **User pool properties**: Enable email verification
3. Create an App Client:
   - **App client name**: `healthcare-platform-web`
   - **Authentication flows**: ALLOW_USER_SRP_AUTH, ALLOW_REFRESH_TOKEN_AUTH
   - **OAuth 2.0**: Enable
   - **Callback URLs**: `http://localhost:3000/auth/callback`
   - **Sign-out URLs**: `http://localhost:3000/auth/signout`
4. Note down the User Pool ID and Client ID

### 2.2 AWS S3 Setup
1. Create an S3 bucket for file storage
2. Enable versioning and encryption
3. Configure CORS policy:
```json
[
    {
        "AllowedHeaders": ["*"],
        "AllowedMethods": ["GET", "PUT", "POST", "DELETE"],
        "AllowedOrigins": ["http://localhost:3000", "https://yourdomain.com"],
        "ExposeHeaders": []
    }
]
```

### 2.3 AWS RDS Setup (Optional for Production)
1. Create a PostgreSQL RDS instance
2. Configure security groups to allow access from your application
3. Update the DATABASE_URL in your environment file

## Step 3: Database Setup

### 3.1 Start the Development Environment
```bash
# Start all services with Docker Compose
docker-compose up -d

# Or start individual services
docker-compose up -d db redis
```

### 3.2 Run Database Migrations
```bash
# Navigate to API directory
cd api

# Create and apply migrations
docker-compose exec web python manage.py makemigrations
docker-compose exec web python manage.py migrate

# Create a superuser
docker-compose exec web python manage.py createsuperuser
```

## Step 4: Backend Setup

### 4.1 Install Dependencies
```bash
cd api
pip install -r requirements.txt
```

### 4.2 Run the Django Server
```bash
# Using Docker
docker-compose up web

# Or directly with Python
python manage.py runserver 0.0.0.0:8000
```

### 4.3 Verify Backend
- Visit `http://localhost:8000/admin/` to access Django admin
- Visit `http://localhost:8000/api/` to see API endpoints
- Check `http://localhost:8000/api/doctors/` for doctor listing

## Step 5: Frontend Setup

### 5.1 Install Dependencies
```bash
cd app
npm install
```

### 5.2 Configure AWS Amplify
Create `app/lib/aws-config.ts`:
```typescript
import { Amplify } from 'aws-amplify';

const awsConfig = {
  Auth: {
    region: process.env.NEXT_PUBLIC_COGNITO_REGION,
    userPoolId: process.env.NEXT_PUBLIC_COGNITO_USER_POOL_ID,
    userPoolWebClientId: process.env.NEXT_PUBLIC_COGNITO_CLIENT_ID,
  },
};

Amplify.configure(awsConfig);
```

### 5.3 Run the Next.js Server
```bash
npm run dev
```

### 5.4 Verify Frontend
- Visit `http://localhost:3000` to see the landing page
- Test user registration and login
- Navigate through the application

## Step 6: Payment Integration

### 6.1 Stripe Setup
1. Create a Stripe account
2. Get your publishable and secret keys
3. Set up webhook endpoints:
   - **Endpoint URL**: `http://localhost:8000/api/payments/webhooks/`
   - **Events**: `payment_intent.succeeded`, `payment_intent.payment_failed`

### 6.2 Test Payments
1. Use Stripe test cards for development
2. Test payment flow in the application
3. Verify webhook handling

## Step 7: WebRTC Setup

### 7.1 TURN Server Setup
1. Set up a TURN server (coturn) on AWS EC2
2. Configure firewall rules
3. Update TURN server credentials in environment

### 7.2 Test Video Calls
1. Create test appointments
2. Test video call functionality
3. Verify signaling and media flow

## Step 8: Notification Setup

### 8.1 Email Configuration
1. Set up SMTP credentials (Gmail App Password recommended)
2. Test email notifications
3. Configure email templates

### 8.2 SMS Configuration (Optional)
1. Set up Twilio account
2. Configure SMS notifications
3. Test SMS delivery

## Step 9: Testing

### 9.1 Backend Testing
```bash
cd api
python manage.py test
```

### 9.2 Frontend Testing
```bash
cd app
npm test
```

### 9.3 End-to-End Testing
1. Test complete user journey:
   - User registration
   - Doctor onboarding
   - Appointment booking
   - Payment processing
   - Video consultation
   - Prescription generation

## Step 10: Production Deployment

### 10.1 Environment Configuration
1. Update environment variables for production
2. Set `DEBUG=False`
3. Configure production database
4. Set up SSL certificates

### 10.2 Docker Production Build
```bash
# Build production images
docker-compose -f docker-compose.prod.yml build

# Deploy to production
docker-compose -f docker-compose.prod.yml up -d
```

### 10.3 AWS Infrastructure
1. Set up AWS ECS/EKS for container orchestration
2. Configure Application Load Balancer
3. Set up CloudFront for CDN
4. Configure Route 53 for DNS

## Step 11: Monitoring and Maintenance

### 11.1 Set up Monitoring
1. Configure AWS CloudWatch
2. Set up error tracking (Sentry)
3. Monitor application performance

### 11.2 Backup Strategy
1. Set up automated database backups
2. Configure S3 lifecycle policies
3. Test backup restoration

## Common Issues and Solutions

### Issue 1: Database Connection Failed
**Solution**: Check if PostgreSQL container is running and credentials are correct.

### Issue 2: CORS Errors
**Solution**: Verify CORS_ALLOWED_ORIGINS in Django settings.

### Issue 3: AWS Cognito Authentication Issues
**Solution**: Check User Pool configuration and callback URLs.

### Issue 4: WebRTC Connection Failed
**Solution**: Verify TURN server configuration and firewall rules.

### Issue 5: Payment Webhook Issues
**Solution**: Check webhook endpoint URL and signature verification.

## Development Workflow

### Daily Development
1. Start services: `docker-compose up -d`
2. Make code changes
3. Test locally
4. Commit changes to Git

### Feature Development
1. Create feature branch
2. Implement feature
3. Write tests
4. Create pull request
5. Deploy to staging
6. Deploy to production

## Security Checklist

- [ ] HTTPS enabled in production
- [ ] Environment variables secured
- [ ] Database credentials protected
- [ ] API rate limiting configured
- [ ] Input validation implemented
- [ ] Audit logging enabled
- [ ] Regular security updates
- [ ] HIPAA compliance measures

## Support and Documentation

- **API Documentation**: See `api/API_ENDPOINTS.md`
- **Database Schema**: Check model files in each app
- **Frontend Components**: See `app/components/` directory
- **Deployment Guide**: See `infra/` directory (when created)

## Next Steps

After completing the setup:

1. **Customize the UI**: Modify components in `app/components/`
2. **Add Features**: Implement additional functionality
3. **Optimize Performance**: Add caching and optimization
4. **Scale Infrastructure**: Set up auto-scaling and load balancing
5. **Compliance**: Implement HIPAA compliance measures
6. **Analytics**: Add user analytics and reporting

## Getting Help

If you encounter issues:

1. Check the logs: `docker-compose logs [service-name]`
2. Review the API documentation
3. Check environment variable configuration
4. Verify AWS service configurations
5. Test individual components separately

Remember to keep your environment variables secure and never commit them to version control!
