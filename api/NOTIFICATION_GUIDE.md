# 📧 Email/SMS Notifications - Complete Guide

## ✅ **What's Implemented**

### **1. Email Services**
- **Gmail SMTP** - Primary email service
- **SendGrid API** - Alternative email service
- **HTML Templates** - Professional email templates
- **Text Fallback** - Plain text versions

### **2. SMS Services**
- **Twilio Integration** - SMS notifications
- **Phone Number Validation** - Proper formatting
- **Message Templates** - Consistent messaging

### **3. Celery Tasks**
- **Async Processing** - Background task execution
- **Task Queuing** - Reliable message delivery
- **Error Handling** - Retry mechanisms
- **Status Tracking** - Task monitoring

### **4. Notification Types**
- **Appointment Reminders** - Email + SMS
- **Payment Confirmations** - Email receipts
- **Doctor Notifications** - System alerts
- **General Notifications** - Custom messages

## 🚀 **How to Use**

### **Backend API Endpoints**

#### **Test Email**
```bash
POST /api/notifications/test-email/
{
  "to_email": "test@example.com"
}
```

#### **Test SMS**
```bash
POST /api/notifications/test-sms/
{
  "to_phone": "+1234567890"
}
```

#### **Send Appointment Reminder**
```bash
POST /api/notifications/appointment-reminder/
{
  "appointment_id": 1,
  "channels": ["email", "sms"]
}
```

#### **Send Payment Confirmation**
```bash
POST /api/notifications/payment-confirmation/
{
  "payment_id": 1
}
```

### **Frontend Components**

#### **Notification Bell**
```tsx
import { NotificationBell } from '@/components/notifications/notification-bell'

<NotificationBell userId={user.id} />
```

#### **Test Notifications Page**
- Visit: `http://localhost:3000/test-notifications`
- Test email and SMS functionality
- Send appointment reminders

## ⚙️ **Configuration**

### **Environment Variables**

#### **Email (Gmail SMTP)**
```env
EMAIL_HOST_USER=your-email@gmail.com
EMAIL_HOST_PASSWORD=your-app-password
DEFAULT_FROM_EMAIL=your-email@gmail.com
```

#### **SMS (Twilio)**
```env
TWILIO_ACCOUNT_SID=your-account-sid
TWILIO_AUTH_TOKEN=your-auth-token
TWILIO_PHONE_NUMBER=your-phone-number
```

#### **SendGrid (Optional)**
```env
SENDGRID_API_KEY=your-sendgrid-api-key
SENDGRID_FROM_EMAIL=noreply@healthcareplatform.com
```

### **Gmail Setup**
1. Enable 2-Factor Authentication
2. Generate App Password
3. Use App Password in `EMAIL_HOST_PASSWORD`

### **Twilio Setup**
1. Create Twilio Account
2. Get Account SID and Auth Token
3. Purchase Phone Number
4. Configure environment variables

## 📧 **Email Templates**

### **Available Templates**
- `appointment_reminder.html` - Appointment reminders
- `payment_confirmation.html` - Payment receipts
- `doctor_notification.html` - Doctor alerts

### **Template Location**
```
api/templates/emails/
├── appointment_reminder.html
├── appointment_reminder.txt
├── payment_confirmation.html
└── payment_confirmation.txt
```

## 🔄 **Celery Tasks**

### **Available Tasks**
- `send_appointment_reminder_email`
- `send_appointment_reminder_sms`
- `send_payment_confirmation_email`
- `send_doctor_notification_email`

### **Running Celery Worker**
```bash
# Terminal 1: Django Server
py manage.py runserver

# Terminal 2: Celery Worker
celery -A healthcare_platform worker --loglevel=info

# Terminal 3: Celery Beat (Scheduler)
celery -A healthcare_platform beat --loglevel=info
```

## 🧪 **Testing**

### **Test Scripts**
```bash
# Test all notifications
py test_notifications.py

# Test email only
py test_email_simple.py
```

### **Frontend Testing**
1. Open: `http://localhost:3000/test-notifications`
2. Enter email/phone
3. Click test buttons
4. Check your email/phone

## 📱 **Frontend Integration**

### **Notification Bell Component**
- Real-time notification display
- Unread count badge
- Mark as read functionality
- Auto-refresh every 30 seconds

### **Test Page Features**
- Email testing interface
- SMS testing interface
- Appointment reminder testing
- Real-time results display

## 🔧 **Troubleshooting**

### **Common Issues**

#### **Email Not Sending**
- Check Gmail credentials
- Verify App Password
- Check firewall settings
- Test with different email

#### **SMS Not Sending**
- Verify Twilio credentials
- Check phone number format
- Ensure sufficient balance
- Test with different number

#### **Celery Tasks Not Running**
- Start Celery worker
- Check Redis connection
- Verify task imports
- Check task logs

### **Debug Commands**
```bash
# Check Celery status
celery -A healthcare_platform inspect active

# Check task results
celery -A healthcare_platform result <task_id>

# Monitor Celery
celery -A healthcare_platform events
```

## 🎯 **Next Steps**

### **Production Setup**
1. Configure production email service
2. Set up Twilio production account
3. Configure Redis for production
4. Set up monitoring and logging

### **Additional Features**
1. Push notifications (FCM)
2. WhatsApp integration
3. Email templates editor
4. Notification preferences
5. Bulk notification sending

## 📊 **Monitoring**

### **Notification Statistics**
- Total notifications sent
- Success/failure rates
- Channel performance
- User engagement

### **API Endpoint**
```bash
GET /api/notifications/stats/
```

## 🎉 **Success!**

Your notification system is now fully functional with:
- ✅ Email notifications (Gmail SMTP)
- ✅ SMS notifications (Twilio)
- ✅ Celery background tasks
- ✅ Professional email templates
- ✅ Frontend testing interface
- ✅ Real-time notification display

**Test it now at:** `http://localhost:3000/test-notifications`
