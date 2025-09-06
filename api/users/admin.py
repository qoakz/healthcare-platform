from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from .models import User, UserProfile


@admin.register(User)
class UserAdmin(BaseUserAdmin):
    list_display = ('email', 'username', 'first_name', 'last_name', 'role', 'is_active', 'date_joined')
    list_filter = ('role', 'is_active', 'is_staff', 'is_superuser', 'date_joined')
    search_fields = ('email', 'username', 'first_name', 'last_name', 'phone')
    ordering = ('-date_joined',)
    
    fieldsets = BaseUserAdmin.fieldsets + (
        ('Healthcare Info', {
            'fields': ('role', 'phone', 'date_of_birth', 'gender', 'cognito_sub')
        }),
        ('Address', {
            'fields': ('address_line1', 'address_line2', 'city', 'state', 'postal_code', 'country')
        }),
        ('Verification', {
            'fields': ('is_phone_verified', 'is_email_verified', 'is_identity_verified')
        }),
        ('Emergency Contact', {
            'fields': ('emergency_contact_name', 'emergency_contact_phone', 'emergency_contact_relationship')
        }),
    )
    
    add_fieldsets = BaseUserAdmin.add_fieldsets + (
        ('Healthcare Info', {
            'fields': ('role', 'phone', 'date_of_birth', 'gender', 'cognito_sub')
        }),
    )


@admin.register(UserProfile)
class UserProfileAdmin(admin.ModelAdmin):
    list_display = ('user', 'blood_type', 'preferred_language', 'allow_telemedicine')
    list_filter = ('blood_type', 'preferred_language', 'allow_telemedicine', 'share_medical_history')
    search_fields = ('user__email', 'user__first_name', 'user__last_name')
    raw_id_fields = ('user',)
