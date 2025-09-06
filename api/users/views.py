from rest_framework import generics, status, permissions
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from rest_framework.views import APIView
from django.contrib.auth import get_user_model
from .models import User, UserProfile
from .serializers import UserSerializer, UserRegistrationSerializer, CognitoAuthSerializer
from .permissions import IsOwnerOrReadOnly

User = get_user_model()


class UserRegistrationView(generics.CreateAPIView):
    """
    User registration endpoint
    """
    queryset = User.objects.all()
    serializer_class = UserRegistrationSerializer
    permission_classes = [permissions.AllowAny]


class UserProfileView(generics.RetrieveUpdateAPIView):
    """
    Get and update user profile
    """
    serializer_class = UserSerializer
    permission_classes = [permissions.IsAuthenticated]
    
    def get_object(self):
        return self.request.user


class UserListView(generics.ListAPIView):
    """
    List users (admin only)
    """
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [permissions.IsAdminUser]


@api_view(['POST'])
@permission_classes([permissions.AllowAny])
def cognito_callback(request):
    """
    Handle AWS Cognito OIDC callback
    """
    serializer = CognitoAuthSerializer(data=request.data)
    if serializer.is_valid():
        user = serializer.save()
        return Response({
            'user': UserSerializer(user).data,
            'message': 'User authenticated successfully'
        }, status=status.HTTP_200_OK)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['GET'])
@permission_classes([permissions.IsAuthenticated])
def me(request):
    """
    Get current user profile
    """
    serializer = UserSerializer(request.user)
    return Response(serializer.data)


@api_view(['POST'])
@permission_classes([permissions.IsAuthenticated])
def verify_phone(request):
    """
    Verify phone number (placeholder for SMS verification)
    """
    # TODO: Implement SMS verification logic
    user = request.user
    user.is_phone_verified = True
    user.save()
    
    return Response({
        'message': 'Phone number verified successfully'
    }, status=status.HTTP_200_OK)


@api_view(['POST'])
@permission_classes([permissions.IsAuthenticated])
def verify_identity(request):
    """
    Verify identity documents (placeholder for KYC)
    """
    # TODO: Implement identity verification logic
    user = request.user
    user.is_identity_verified = True
    user.save()
    
    return Response({
        'message': 'Identity verified successfully'
    }, status=status.HTTP_200_OK)
