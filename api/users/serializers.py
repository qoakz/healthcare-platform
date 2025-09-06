from rest_framework import serializers
from django.contrib.auth import authenticate
from .models import User, UserProfile


class UserProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserProfile
        fields = [
            'profile_image', 'blood_type', 'allergies', 'medical_conditions',
            'current_medications', 'preferred_language', 'timezone',
            'share_medical_history', 'allow_telemedicine'
        ]


class UserSerializer(serializers.ModelSerializer):
    profile = UserProfileSerializer(read_only=True)
    
    class Meta:
        model = User
        fields = [
            'id', 'username', 'email', 'first_name', 'last_name', 'role',
            'phone', 'date_of_birth', 'gender', 'address_line1', 'address_line2',
            'city', 'state', 'postal_code', 'country', 'is_phone_verified',
            'is_email_verified', 'is_identity_verified', 'emergency_contact_name',
            'emergency_contact_phone', 'emergency_contact_relationship',
            'date_joined', 'profile'
        ]
        read_only_fields = ['id', 'date_joined', 'is_phone_verified', 'is_email_verified', 'is_identity_verified']


class UserRegistrationSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True, min_length=8)
    password_confirm = serializers.CharField(write_only=True)
    
    class Meta:
        model = User
        fields = [
            'username', 'email', 'password', 'password_confirm', 'first_name',
            'last_name', 'phone', 'date_of_birth', 'gender', 'role'
        ]
    
    def validate(self, attrs):
        if attrs['password'] != attrs['password_confirm']:
            raise serializers.ValidationError("Passwords don't match")
        return attrs
    
    def create(self, validated_data):
        validated_data.pop('password_confirm')
        user = User.objects.create_user(**validated_data)
        # Create user profile
        UserProfile.objects.create(user=user)
        return user


class CognitoAuthSerializer(serializers.Serializer):
    """
    Serializer for AWS Cognito authentication
    """
    cognito_sub = serializers.CharField()
    email = serializers.EmailField()
    first_name = serializers.CharField(required=False, allow_blank=True)
    last_name = serializers.CharField(required=False, allow_blank=True)
    phone = serializers.CharField(required=False, allow_blank=True)
    
    def create(self, validated_data):
        cognito_sub = validated_data['cognito_sub']
        email = validated_data['email']
        
        # Check if user exists
        try:
            user = User.objects.get(cognito_sub=cognito_sub)
            # Update user info if needed
            user.email = email
            user.first_name = validated_data.get('first_name', user.first_name)
            user.last_name = validated_data.get('last_name', user.last_name)
            user.phone = validated_data.get('phone', user.phone)
            user.save()
        except User.DoesNotExist:
            # Create new user
            user = User.objects.create(
                cognito_sub=cognito_sub,
                email=email,
                username=email,  # Use email as username
                first_name=validated_data.get('first_name', ''),
                last_name=validated_data.get('last_name', ''),
                phone=validated_data.get('phone', ''),
                is_active=True
            )
            # Create user profile
            UserProfile.objects.create(user=user)
        
        return user
