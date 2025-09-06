from django.urls import path
from . import views

urlpatterns = [
    path('', views.AppointmentListView.as_view(), name='appointment-list'),
    path('upcoming/', views.upcoming_appointments, name='upcoming-appointments'),
    path('<int:pk>/', views.AppointmentDetailView.as_view(), name='appointment-detail'),
    path('<int:appointment_id>/cancel/', views.cancel_appointment, name='cancel-appointment'),
    path('<int:appointment_id>/reschedule/', views.AppointmentRescheduleView.as_view(), name='reschedule-appointment'),
    path('<int:appointment_id>/start/', views.start_appointment, name='start-appointment'),
    path('<int:appointment_id>/end/', views.end_appointment, name='end-appointment'),
    path('<int:appointment_id>/reminders/', views.appointment_reminders, name='appointment-reminders'),
    path('slots/', views.ScheduleSlotListView.as_view(), name='schedule-slot-list'),
]
