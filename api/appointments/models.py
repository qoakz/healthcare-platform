from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator
from users.models import User
from doctors.models import Doctor


class ScheduleSlot(models.Model):
    """
    Available time slots for doctors
    """
    STATUS_CHOICES = [
        ('open', 'Open'),
        ('booked', 'Booked'),
        ('blocked', 'Blocked'),
    ]
    
    doctor = models.ForeignKey(Doctor, on_delete=models.CASCADE, related_name='schedule_slots')
    start_time = models.DateTimeField()
    end_time = models.DateTimeField()
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='open')
    
    # Slot duration in minutes (default 30)
    duration_minutes = models.PositiveIntegerField(default=30)
    
    # Notes for blocked slots
    notes = models.TextField(blank=True)
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        db_table = 'schedule_slot'
        unique_together = ['doctor', 'start_time']
        verbose_name = 'Schedule Slot'
        verbose_name_plural = 'Schedule Slots'
    
    def __str__(self):
        return f"{self.doctor.full_name} - {self.start_time.strftime('%Y-%m-%d %H:%M')}"
    
    @property
    def is_available(self):
        return self.status == 'open'


class Appointment(models.Model):
    """
    Patient appointments with doctors
    """
    STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('confirmed', 'Confirmed'),
        ('in_progress', 'In Progress'),
        ('completed', 'Completed'),
        ('cancelled', 'Cancelled'),
        ('no_show', 'No Show'),
        ('refunded', 'Refunded'),
    ]
    
    APPOINTMENT_TYPE_CHOICES = [
        ('video', 'Video Consultation'),
        ('in_person', 'In-Person Visit'),
    ]
    
    patient = models.ForeignKey(User, on_delete=models.CASCADE, related_name='appointments')
    doctor = models.ForeignKey(Doctor, on_delete=models.CASCADE, related_name='appointments')
    slot = models.ForeignKey(ScheduleSlot, on_delete=models.CASCADE, related_name='appointment')
    
    # Appointment details
    appointment_type = models.CharField(max_length=20, choices=APPOINTMENT_TYPE_CHOICES, default='video')
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')
    
    # Consultation details
    reason = models.TextField(help_text="Reason for consultation")
    symptoms = models.TextField(blank=True)
    medical_history = models.TextField(blank=True)
    
    # Video call information
    video_room_id = models.CharField(max_length=255, blank=True)
    video_join_token = models.TextField(blank=True)
    video_join_token_expires = models.DateTimeField(null=True, blank=True)
    
    # Payment information
    consultation_fee = models.DecimalField(max_digits=10, decimal_places=2)
    payment_status = models.CharField(max_length=20, default='pending')
    payment_id = models.CharField(max_length=255, blank=True)
    
    # Timestamps
    scheduled_at = models.DateTimeField()
    started_at = models.DateTimeField(null=True, blank=True)
    ended_at = models.DateTimeField(null=True, blank=True)
    
    # Notes and feedback
    doctor_notes = models.TextField(blank=True)
    patient_feedback = models.TextField(blank=True)
    
    # Follow-up
    requires_follow_up = models.BooleanField(default=False)
    follow_up_date = models.DateTimeField(null=True, blank=True)
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        db_table = 'appointments_appt'
        verbose_name = 'Appointment'
        verbose_name_plural = 'Appointments'
        ordering = ['-scheduled_at']
    
    def __str__(self):
        return f"{self.patient.get_full_name()} with Dr. {self.doctor.full_name} - {self.scheduled_at.strftime('%Y-%m-%d %H:%M')}"
    
    @property
    def duration_minutes(self):
        if self.started_at and self.ended_at:
            delta = self.ended_at - self.started_at
            return int(delta.total_seconds() / 60)
        return None
    
    @property
    def is_upcoming(self):
        from django.utils import timezone
        return self.scheduled_at > timezone.now() and self.status in ['pending', 'confirmed']
    
    @property
    def can_be_cancelled(self):
        from django.utils import timezone
        from datetime import timedelta
        # Can cancel up to 2 hours before appointment
        return (self.scheduled_at - timezone.now()) > timedelta(hours=2) and self.status in ['pending', 'confirmed']
    
    @property
    def can_be_rescheduled(self):
        from django.utils import timezone
        from datetime import timedelta
        # Can reschedule up to 24 hours before appointment
        return (self.scheduled_at - timezone.now()) > timedelta(hours=24) and self.status in ['pending', 'confirmed']


class AppointmentReminder(models.Model):
    """
    Track appointment reminders sent to patients
    """
    REMINDER_TYPE_CHOICES = [
        ('booking_confirmation', 'Booking Confirmation'),
        ('24_hour', '24 Hour Reminder'),
        ('1_hour', '1 Hour Reminder'),
        ('15_minute', '15 Minute Reminder'),
        ('post_visit', 'Post-Visit Follow-up'),
    ]
    
    CHANNEL_CHOICES = [
        ('email', 'Email'),
        ('sms', 'SMS'),
        ('push', 'Push Notification'),
    ]
    
    appointment = models.ForeignKey(Appointment, on_delete=models.CASCADE, related_name='reminders')
    reminder_type = models.CharField(max_length=20, choices=REMINDER_TYPE_CHOICES)
    channel = models.CharField(max_length=10, choices=CHANNEL_CHOICES)
    
    # Delivery tracking
    sent_at = models.DateTimeField(null=True, blank=True)
    delivery_status = models.CharField(max_length=20, default='pending')
    delivery_id = models.CharField(max_length=255, blank=True)  # External service ID
    
    # Content
    message_content = models.TextField()
    
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        db_table = 'appointments_reminder'
        verbose_name = 'Appointment Reminder'
        verbose_name_plural = 'Appointment Reminders'
    
    def __str__(self):
        return f"{self.appointment} - {self.get_reminder_type_display()} via {self.get_channel_display()}"


class AppointmentReschedule(models.Model):
    """
    Track appointment rescheduling history
    """
    appointment = models.ForeignKey(Appointment, on_delete=models.CASCADE, related_name='reschedules')
    old_slot = models.ForeignKey(ScheduleSlot, on_delete=models.CASCADE, related_name='old_reschedules')
    new_slot = models.ForeignKey(ScheduleSlot, on_delete=models.CASCADE, related_name='new_reschedules')
    
    reason = models.TextField()
    requested_by = models.ForeignKey(User, on_delete=models.CASCADE)
    
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        db_table = 'appointments_reschedule'
        verbose_name = 'Appointment Reschedule'
        verbose_name_plural = 'Appointment Reschedules'
    
    def __str__(self):
        return f"{self.appointment} rescheduled from {self.old_slot.start_time} to {self.new_slot.start_time}"
