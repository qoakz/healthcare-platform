from django.urls import path
from . import views

urlpatterns = [
    # Medical Records
    path('medical-records/', views.MedicalRecordListView.as_view(), name='medical-record-list'),
    path('medical-records/<uuid:pk>/', views.MedicalRecordDetailView.as_view(), name='medical-record-detail'),
    path('medical-records/<uuid:medical_record_id>/pdf/', views.download_medical_record_pdf, name='medical-record-pdf'),
    
    # Prescriptions
    path('prescriptions/', views.PrescriptionListView.as_view(), name='prescription-list'),
    path('prescriptions/<uuid:pk>/', views.PrescriptionDetailView.as_view(), name='prescription-detail'),
    path('prescriptions/<uuid:prescription_id>/pdf/', views.download_prescription_pdf, name='prescription-pdf'),
    
    # Lab Results
    path('lab-results/', views.LabResultListView.as_view(), name='lab-result-list'),
    path('lab-results/<uuid:pk>/', views.LabResultDetailView.as_view(), name='lab-result-detail'),
    
    # Vital Signs
    path('vital-signs/', views.VitalSignListView.as_view(), name='vital-sign-list'),
    path('vital-signs/<uuid:pk>/', views.VitalSignDetailView.as_view(), name='vital-sign-detail'),
    
    # Allergies
    path('allergies/', views.AllergyListView.as_view(), name='allergy-list'),
    path('allergies/<uuid:pk>/', views.AllergyDetailView.as_view(), name='allergy-detail'),
    
    # Statistics and Analytics
    path('stats/doctor/', views.doctor_emr_stats, name='doctor-emr-stats'),
    path('stats/patient/', views.patient_emr_summary, name='patient-emr-summary'),
]