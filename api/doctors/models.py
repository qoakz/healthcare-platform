from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator
from users.models import User


class Doctor(models.Model):
    """
    Doctor profile and professional information
    """
    KYC_STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('verified', 'Verified'),
        ('rejected', 'Rejected'),
    ]
    
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='doctor_profile')
    
    # Professional information
    registration_number = models.CharField(max_length=100, unique=True)
    years_of_experience = models.PositiveIntegerField(
        validators=[MinValueValidator(0), MaxValueValidator(50)]
    )
    
    # Specialties (stored as JSON array)
    specialties = models.JSONField(default=list, help_text="List of medical specialties")
    
    # Practice information
    clinic_name = models.CharField(max_length=255, blank=True)
    clinic_address = models.TextField(blank=True)
    consultation_fee = models.DecimalField(max_digits=10, decimal_places=2)
    
    # KYC and verification
    kyc_status = models.CharField(max_length=20, choices=KYC_STATUS_CHOICES, default='pending')
    kyc_documents = models.JSONField(default=list, help_text="List of uploaded KYC document URLs")
    
    # Professional documents
    medical_license_url = models.URLField(blank=True)
    degree_certificates = models.JSONField(default=list, help_text="List of degree certificate URLs")
    
    # Availability and settings
    is_available_for_consultation = models.BooleanField(default=True)
    max_patients_per_day = models.PositiveIntegerField(default=20)
    
    # Rating and reviews
    average_rating = models.DecimalField(max_digits=3, decimal_places=2, default=0.00)
    total_reviews = models.PositiveIntegerField(default=0)
    
    # Timestamps
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        db_table = 'doctors_doctor'
        verbose_name = 'Doctor'
        verbose_name_plural = 'Doctors'
    
    def __str__(self):
        return f"Dr. {self.user.get_full_name()} - {', '.join(self.specialties[:2])}"
    
    @property
    def is_verified(self):
        return self.kyc_status == 'verified'
    
    @property
    def full_name(self):
        return self.user.get_full_name()


class DoctorAvailability(models.Model):
    """
    Doctor's availability schedule
    """
    DAY_CHOICES = [
        (0, 'Monday'),
        (1, 'Tuesday'),
        (2, 'Wednesday'),
        (3, 'Thursday'),
        (4, 'Friday'),
        (5, 'Saturday'),
        (6, 'Sunday'),
    ]
    
    doctor = models.ForeignKey(Doctor, on_delete=models.CASCADE, related_name='availability')
    day_of_week = models.IntegerField(choices=DAY_CHOICES)
    start_time = models.TimeField()
    end_time = models.TimeField()
    is_available = models.BooleanField(default=True)
    
    # Break times (stored as JSON array of time ranges)
    break_times = models.JSONField(
        default=list,
        help_text="List of break time ranges, e.g., [{'start': '12:00', 'end': '13:00'}]"
    )
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        db_table = 'doctors_availability'
        unique_together = ['doctor', 'day_of_week']
        verbose_name = 'Doctor Availability'
        verbose_name_plural = 'Doctor Availabilities'
    
    def __str__(self):
        return f"{self.doctor.full_name} - {self.get_day_of_week_display()} ({self.start_time}-{self.end_time})"


class DoctorReview(models.Model):
    """
    Patient reviews for doctors
    """
    RATING_CHOICES = [
        (1, '1 Star'),
        (2, '2 Stars'),
        (3, '3 Stars'),
        (4, '4 Stars'),
        (5, '5 Stars'),
    ]
    
    doctor = models.ForeignKey(Doctor, on_delete=models.CASCADE, related_name='reviews')
    patient = models.ForeignKey(User, on_delete=models.CASCADE, related_name='doctor_reviews')
    appointment = models.ForeignKey('appointments.Appointment', on_delete=models.CASCADE, related_name='review')
    
    rating = models.IntegerField(choices=RATING_CHOICES)
    comment = models.TextField(blank=True)
    
    # Review categories
    communication_rating = models.IntegerField(choices=RATING_CHOICES, null=True, blank=True)
    treatment_rating = models.IntegerField(choices=RATING_CHOICES, null=True, blank=True)
    punctuality_rating = models.IntegerField(choices=RATING_CHOICES, null=True, blank=True)
    
    is_anonymous = models.BooleanField(default=False)
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        db_table = 'doctors_review'
        unique_together = ['doctor', 'patient', 'appointment']
        verbose_name = 'Doctor Review'
        verbose_name_plural = 'Doctor Reviews'
    
    def __str__(self):
        return f"{self.patient.get_full_name()} - {self.rating} stars for Dr. {self.doctor.full_name}"
