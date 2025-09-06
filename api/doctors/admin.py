from django.contrib import admin
from .models import Doctor, DoctorAvailability, DoctorReview


@admin.register(Doctor)
class DoctorAdmin(admin.ModelAdmin):
    list_display = ('user', 'registration_number', 'specialties', 'consultation_fee', 'kyc_status', 'average_rating')
    list_filter = ('kyc_status', 'is_available_for_consultation', 'specialties')
    search_fields = ('user__first_name', 'user__last_name', 'registration_number', 'clinic_name')
    raw_id_fields = ('user',)
    
    fieldsets = (
        ('Basic Information', {
            'fields': ('user', 'registration_number', 'years_of_experience', 'specialties')
        }),
        ('Practice Information', {
            'fields': ('clinic_name', 'clinic_address', 'consultation_fee', 'max_patients_per_day')
        }),
        ('Verification', {
            'fields': ('kyc_status', 'kyc_documents', 'medical_license_url', 'degree_certificates')
        }),
        ('Settings', {
            'fields': ('is_available_for_consultation',)
        }),
        ('Ratings', {
            'fields': ('average_rating', 'total_reviews'),
            'classes': ('collapse',)
        }),
    )


@admin.register(DoctorAvailability)
class DoctorAvailabilityAdmin(admin.ModelAdmin):
    list_display = ('doctor', 'day_of_week', 'start_time', 'end_time', 'is_available')
    list_filter = ('day_of_week', 'is_available')
    search_fields = ('doctor__user__first_name', 'doctor__user__last_name')
    raw_id_fields = ('doctor',)


@admin.register(DoctorReview)
class DoctorReviewAdmin(admin.ModelAdmin):
    list_display = ('doctor', 'patient', 'rating', 'created_at')
    list_filter = ('rating', 'created_at', 'is_anonymous')
    search_fields = ('doctor__user__first_name', 'patient__first_name', 'comment')
    raw_id_fields = ('doctor', 'patient', 'appointment')
