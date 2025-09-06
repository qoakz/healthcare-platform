from django.db import models
from users.models import User
from doctors.models import Doctor
from appointments.models import Appointment


class PaymentTransaction(models.Model):
    """
    Payment transactions
    """
    PROVIDER_CHOICES = [
        ('stripe', 'Stripe'),
        ('razorpay', 'Razorpay'),
    ]
    
    STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('processing', 'Processing'),
        ('completed', 'Completed'),
        ('failed', 'Failed'),
        ('cancelled', 'Cancelled'),
        ('refunded', 'Refunded'),
    ]
    
    # Transaction details
    provider = models.CharField(max_length=20, choices=PROVIDER_CHOICES)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    currency = models.CharField(max_length=3, default='USD')
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')
    
    # External provider details
    external_id = models.CharField(max_length=255, unique=True)
    client_secret = models.CharField(max_length=255, blank=True)
    
    # Related entities
    appointment = models.ForeignKey(Appointment, on_delete=models.CASCADE, related_name='payments', null=True, blank=True)
    patient = models.ForeignKey(User, on_delete=models.CASCADE, related_name='payments')
    
    # Metadata
    description = models.TextField(blank=True)
    metadata = models.JSONField(default=dict)
    
    # Timestamps
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    completed_at = models.DateTimeField(null=True, blank=True)
    
    class Meta:
        db_table = 'payments_txn'
        verbose_name = 'Payment Transaction'
        verbose_name_plural = 'Payment Transactions'
    
    def __str__(self):
        return f"Payment {self.external_id} - {self.amount} {self.currency}"


class Refund(models.Model):
    """
    Payment refunds
    """
    STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('processing', 'Processing'),
        ('completed', 'Completed'),
        ('failed', 'Failed'),
    ]
    
    payment = models.ForeignKey(PaymentTransaction, on_delete=models.CASCADE, related_name='refunds')
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    reason = models.TextField()
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')
    
    # External provider details
    external_refund_id = models.CharField(max_length=255, blank=True)
    
    # Metadata
    processed_by = models.ForeignKey(User, on_delete=models.CASCADE, related_name='processed_refunds')
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        db_table = 'payments_refund'
        verbose_name = 'Refund'
        verbose_name_plural = 'Refunds'
    
    def __str__(self):
        return f"Refund for {self.payment.external_id} - {self.amount}"


class DoctorPayout(models.Model):
    """
    Doctor payouts
    """
    STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('processing', 'Processing'),
        ('completed', 'Completed'),
        ('failed', 'Failed'),
    ]
    
    doctor = models.ForeignKey(Doctor, on_delete=models.CASCADE, related_name='payouts')
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')
    
    # Payout period
    period_start = models.DateField()
    period_end = models.DateField()
    
    # Related appointments
    appointments = models.ManyToManyField(Appointment, related_name='payouts')
    
    # External provider details
    external_payout_id = models.CharField(max_length=255, blank=True)
    
    # Metadata
    processed_at = models.DateTimeField(null=True, blank=True)
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        db_table = 'payouts_doctor'
        verbose_name = 'Doctor Payout'
        verbose_name_plural = 'Doctor Payouts'
    
    def __str__(self):
        return f"Payout for Dr. {self.doctor.full_name} - {self.amount}"
