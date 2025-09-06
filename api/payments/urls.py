from django.urls import path
from . import views

urlpatterns = [
    # Payment Transactions
    path('transactions/', views.PaymentTransactionListView.as_view(), name='payment-transaction-list'),
    path('transactions/<int:pk>/', views.PaymentTransactionDetailView.as_view(), name='payment-transaction-detail'),
    path('intent/', views.create_payment_intent, name='create-payment-intent'),
    
    # Refunds
    path('refunds/', views.RefundListView.as_view(), name='refund-list'),
    path('refunds/<int:pk>/', views.RefundDetailView.as_view(), name='refund-detail'),
    path('transactions/<int:payment_id>/refund/', views.process_refund, name='process-refund'),
    
    # Doctor Payouts
    path('payouts/', views.DoctorPayoutListView.as_view(), name='doctor-payout-list'),
    path('payouts/<int:pk>/', views.DoctorPayoutDetailView.as_view(), name='doctor-payout-detail'),
    path('payouts/generate/', views.generate_doctor_payout, name='generate-doctor-payout'),
    
    # Doctor Earnings
    path('earnings/', views.doctor_earnings, name='doctor-earnings'),
    
    # Webhooks
    path('webhooks/', views.payment_webhook, name='payment-webhook'),
]