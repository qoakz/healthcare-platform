from django.db import models
from django.contrib.auth import get_user_model
from django.core.validators import MinValueValidator, MaxValueValidator
from decimal import Decimal
import uuid

User = get_user_model()

class MedicalRecord(models.Model):
    """Main medical record for a patient"""
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    patient = models.ForeignKey(User, on_delete=models.CASCADE, related_name='medical_records')
    doctor = models.ForeignKey(User, on_delete=models.CASCADE, related_name='created_medical_records')
    appointment = models.ForeignKey('appointments.Appointment', on_delete=models.CASCADE, null=True, blank=True)
    
    # Record details
    chief_complaint = models.TextField(help_text="Primary reason for visit")
    history_of_present_illness = models.TextField(help_text="Detailed history of current condition")
    past_medical_history = models.TextField(blank=True, help_text="Previous medical conditions")
    family_history = models.TextField(blank=True, help_text="Family medical history")
    social_history = models.TextField(blank=True, help_text="Lifestyle factors, smoking, alcohol, etc.")
    
    # Physical examination
    vital_signs = models.JSONField(default=dict, help_text="Blood pressure, temperature, pulse, etc.")
    physical_examination = models.TextField(help_text="Physical examination findings")
    diagnosis = models.TextField(help_text="Primary and secondary diagnoses")
    treatment_plan = models.TextField(help_text="Treatment recommendations")
    
    # Additional notes
    notes = models.TextField(blank=True, help_text="Additional clinical notes")
    follow_up_required = models.BooleanField(default=False)
    follow_up_date = models.DateField(null=True, blank=True)
    
    # Metadata
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    is_active = models.BooleanField(default=True)
    
    class Meta:
        ordering = ['-created_at']
        verbose_name = "Medical Record"
        verbose_name_plural = "Medical Records"
    
    def __str__(self):
        return f"Medical Record for {self.patient.get_full_name()} - {self.created_at.strftime('%Y-%m-%d')}"

class Prescription(models.Model):
    """Prescription model for medications"""
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    medical_record = models.ForeignKey(MedicalRecord, on_delete=models.CASCADE, related_name='prescriptions')
    patient = models.ForeignKey(User, on_delete=models.CASCADE, related_name='prescriptions')
    doctor = models.ForeignKey(User, on_delete=models.CASCADE, related_name='issued_prescriptions', null=True, blank=True)
    
    # Prescription details
    medication_name = models.CharField(max_length=200)
    generic_name = models.CharField(max_length=200, blank=True)
    dosage = models.CharField(max_length=100, help_text="e.g., 500mg, 10ml")
    frequency = models.CharField(max_length=100, help_text="e.g., Twice daily, Every 8 hours")
    duration = models.CharField(max_length=100, help_text="e.g., 7 days, 2 weeks")
    quantity = models.PositiveIntegerField(help_text="Total quantity to dispense")
    instructions = models.TextField(help_text="Special instructions for patient")
    
    # Prescription status
    STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('filled', 'Filled'),
        ('cancelled', 'Cancelled'),
        ('expired', 'Expired'),
    ]
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')
    
    # Additional details
    refills_allowed = models.PositiveIntegerField(default=0)
    refills_used = models.PositiveIntegerField(default=0)
    expiry_date = models.DateField(null=True, blank=True)
    
    # Metadata
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        ordering = ['-created_at']
        verbose_name = "Prescription"
        verbose_name_plural = "Prescriptions"
    
    def __str__(self):
        return f"{self.medication_name} - {self.patient.get_full_name()}"
    
    @property
    def is_expired(self):
        if self.expiry_date:
            from django.utils import timezone
            return timezone.now().date() > self.expiry_date
        return False

class LabResult(models.Model):
    """Lab test results"""
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    medical_record = models.ForeignKey(MedicalRecord, on_delete=models.CASCADE, related_name='lab_results')
    patient = models.ForeignKey(User, on_delete=models.CASCADE, related_name='lab_results')
    doctor = models.ForeignKey(User, on_delete=models.CASCADE, related_name='ordered_lab_results', null=True, blank=True)
    
    # Lab details
    test_name = models.CharField(max_length=200)
    test_type = models.CharField(max_length=100, help_text="e.g., Blood Test, Urine Test, X-Ray")
    lab_name = models.CharField(max_length=200, blank=True)
    test_date = models.DateField()
    result_date = models.DateField(null=True, blank=True)
    
    # Results
    results = models.JSONField(default=dict, help_text="Test results with values and units")
    normal_range = models.CharField(max_length=200, blank=True)
    interpretation = models.TextField(blank=True, help_text="Doctor's interpretation of results")
    notes = models.TextField(blank=True)
    
    # File attachments
    result_file = models.FileField(upload_to='lab_results/', null=True, blank=True)
    
    # Status
    STATUS_CHOICES = [
        ('ordered', 'Ordered'),
        ('in_progress', 'In Progress'),
        ('completed', 'Completed'),
        ('cancelled', 'Cancelled'),
    ]
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='ordered')
    
    # Metadata
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        ordering = ['-test_date']
        verbose_name = "Lab Result"
        verbose_name_plural = "Lab Results"
    
    def __str__(self):
        return f"{self.test_name} - {self.patient.get_full_name()}"

class VitalSign(models.Model):
    """Patient vital signs"""
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    patient = models.ForeignKey(User, on_delete=models.CASCADE, related_name='vital_signs')
    recorded_by = models.ForeignKey(User, on_delete=models.CASCADE, related_name='recorded_vital_signs', null=True, blank=True)
    medical_record = models.ForeignKey(MedicalRecord, on_delete=models.CASCADE, related_name='record_vital_signs', null=True, blank=True)
    
    # Vital signs
    blood_pressure_systolic = models.PositiveIntegerField(null=True, blank=True, validators=[MinValueValidator(50), MaxValueValidator(300)])
    blood_pressure_diastolic = models.PositiveIntegerField(null=True, blank=True, validators=[MinValueValidator(30), MaxValueValidator(200)])
    heart_rate = models.PositiveIntegerField(null=True, blank=True, validators=[MinValueValidator(30), MaxValueValidator(300)])
    temperature = models.DecimalField(max_digits=4, decimal_places=1, null=True, blank=True, validators=[MinValueValidator(Decimal('90.0')), MaxValueValidator(Decimal('110.0'))])
    respiratory_rate = models.PositiveIntegerField(null=True, blank=True, validators=[MinValueValidator(5), MaxValueValidator(60)])
    oxygen_saturation = models.PositiveIntegerField(null=True, blank=True, validators=[MinValueValidator(50), MaxValueValidator(100)])
    weight = models.DecimalField(max_digits=5, decimal_places=2, null=True, blank=True, validators=[MinValueValidator(Decimal('0.1')), MaxValueValidator(Decimal('1000.0'))])
    height = models.DecimalField(max_digits=5, decimal_places=2, null=True, blank=True, validators=[MinValueValidator(Decimal('0.1')), MaxValueValidator(Decimal('300.0'))])
    
    # Additional measurements
    bmi = models.DecimalField(max_digits=4, decimal_places=1, null=True, blank=True)
    pain_level = models.PositiveIntegerField(null=True, blank=True, validators=[MinValueValidator(0), MaxValueValidator(10)])
    
    # Metadata
    recorded_at = models.DateTimeField(auto_now_add=True)
    notes = models.TextField(blank=True)
    
    class Meta:
        ordering = ['-recorded_at']
        verbose_name = "Vital Sign"
        verbose_name_plural = "Vital Signs"
    
    def __str__(self):
        return f"Vital Signs - {self.patient.get_full_name()} - {self.recorded_at.strftime('%Y-%m-%d %H:%M')}"
    
    def save(self, *args, **kwargs):
        # Calculate BMI if weight and height are provided
        if self.weight and self.height:
            height_m = float(self.height) / 100  # Convert cm to meters
            self.bmi = round(float(self.weight) / (height_m ** 2), 1)
        super().save(*args, **kwargs)

class Allergy(models.Model):
    """Patient allergies"""
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    patient = models.ForeignKey(User, on_delete=models.CASCADE, related_name='allergies')
    recorded_by = models.ForeignKey(User, on_delete=models.CASCADE, related_name='recorded_allergies', null=True, blank=True)
    
    # Allergy details
    allergen = models.CharField(max_length=200, help_text="Substance causing allergy")
    allergy_type = models.CharField(max_length=100, help_text="e.g., Drug, Food, Environmental")
    severity = models.CharField(max_length=50, choices=[
        ('mild', 'Mild'),
        ('moderate', 'Moderate'),
        ('severe', 'Severe'),
        ('life_threatening', 'Life-threatening'),
    ])
    reaction = models.TextField(help_text="Description of allergic reaction")
    notes = models.TextField(blank=True)
    
    # Status
    is_active = models.BooleanField(default=True)
    confirmed_date = models.DateField()
    
    # Metadata
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        ordering = ['-confirmed_date']
        verbose_name = "Allergy"
        verbose_name_plural = "Allergies"
        unique_together = ['patient', 'allergen']
    
    def __str__(self):
        return f"{self.allergen} - {self.patient.get_full_name()}"