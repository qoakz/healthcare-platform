from django.contrib import admin
from .models import Appointment, ScheduleSlot, AppointmentReminder, AppointmentReschedule


@admin.register(Appointment)
class AppointmentAdmin(admin.ModelAdmin):
    list_display = ('patient', 'doctor', 'scheduled_at', 'status', 'appointment_type', 'consultation_fee')
    list_filter = ('status', 'appointment_type', 'scheduled_at', 'created_at')
    search_fields = ('patient__first_name', 'patient__last_name', 'doctor__user__first_name', 'reason')
    raw_id_fields = ('patient', 'doctor', 'slot')
    date_hierarchy = 'scheduled_at'
    
    fieldsets = (
        ('Basic Information', {
            'fields': ('patient', 'doctor', 'slot', 'appointment_type', 'status')
        }),
        ('Consultation Details', {
            'fields': ('reason', 'symptoms', 'medical_history')
        }),
        ('Video Call', {
            'fields': ('video_room_id', 'video_join_token', 'video_join_token_expires'),
            'classes': ('collapse',)
        }),
        ('Payment', {
            'fields': ('consultation_fee', 'payment_status', 'payment_id'),
            'classes': ('collapse',)
        }),
        ('Timestamps', {
            'fields': ('scheduled_at', 'started_at', 'ended_at'),
            'classes': ('collapse',)
        }),
        ('Notes & Feedback', {
            'fields': ('doctor_notes', 'patient_feedback', 'requires_follow_up', 'follow_up_date'),
            'classes': ('collapse',)
        }),
    )


@admin.register(ScheduleSlot)
class ScheduleSlotAdmin(admin.ModelAdmin):
    list_display = ('doctor', 'start_time', 'end_time', 'status', 'duration_minutes')
    list_filter = ('status', 'start_time', 'doctor')
    search_fields = ('doctor__user__first_name', 'doctor__user__last_name', 'notes')
    raw_id_fields = ('doctor',)
    date_hierarchy = 'start_time'


@admin.register(AppointmentReminder)
class AppointmentReminderAdmin(admin.ModelAdmin):
    list_display = ('appointment', 'reminder_type', 'channel', 'sent_at', 'delivery_status')
    list_filter = ('reminder_type', 'channel', 'delivery_status', 'sent_at')
    search_fields = ('appointment__patient__first_name', 'appointment__doctor__user__first_name')
    raw_id_fields = ('appointment',)
    date_hierarchy = 'created_at'


@admin.register(AppointmentReschedule)
class AppointmentRescheduleAdmin(admin.ModelAdmin):
    list_display = ('appointment', 'old_slot', 'new_slot', 'requested_by', 'created_at')
    list_filter = ('created_at',)
    search_fields = ('appointment__patient__first_name', 'appointment__doctor__user__first_name', 'reason')
    raw_id_fields = ('appointment', 'old_slot', 'new_slot', 'requested_by')
    date_hierarchy = 'created_at'
