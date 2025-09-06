from django.urls import path
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView
from . import views

urlpatterns = [
    path('register/', views.UserRegistrationView.as_view(), name='user-register'),
    path('login/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('me/', views.me, name='user-me'),
    path('profile/', views.UserProfileView.as_view(), name='user-profile'),
    path('list/', views.UserListView.as_view(), name='user-list'),
    path('cognito/callback/', views.cognito_callback, name='cognito-callback'),
    path('verify/phone/', views.verify_phone, name='verify-phone'),
    path('verify/identity/', views.verify_identity, name='verify-identity'),
]
