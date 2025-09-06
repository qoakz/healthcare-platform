from django.urls import path
from . import views

urlpatterns = [
    path('', views.DoctorListView.as_view(), name='doctor-list'),
    path('register/', views.DoctorRegistrationView.as_view(), name='doctor-register'),
    path('profile/', views.DoctorProfileView.as_view(), name='doctor-profile'),
    path('<int:pk>/', views.DoctorDetailView.as_view(), name='doctor-detail'),
    path('<int:doctor_id>/availability/', views.doctor_availability_slots, name='doctor-availability-slots'),
    path('<int:doctor_id>/reviews/', views.DoctorReviewsView.as_view(), name='doctor-reviews'),
    path('<int:doctor_id>/reviews/create/', views.CreateDoctorReviewView.as_view(), name='create-doctor-review'),
    path('availability/', views.DoctorAvailabilityView.as_view(), name='doctor-availability'),
    path('availability/<int:pk>/', views.DoctorAvailabilityDetailView.as_view(), name='doctor-availability-detail'),
    path('kyc/update/', views.update_kyc_status, name='update-kyc-status'),
]
