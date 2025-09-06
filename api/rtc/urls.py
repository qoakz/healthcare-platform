from django.urls import path
from . import views

urlpatterns = [
    # RTC Rooms
    path('rooms/', views.RTCRoomListView.as_view(), name='rtc-room-list'),
    path('rooms/<int:pk>/', views.RTCRoomDetailView.as_view(), name='rtc-room-detail'),
    path('rooms/appointment/<int:appointment_id>/', views.create_room_for_appointment, name='create-room-for-appointment'),
    path('rooms/<str:room_id>/join/', views.join_room, name='join-room'),
    path('rooms/<str:room_id>/start/', views.start_room, name='start-room'),
    path('rooms/<str:room_id>/end/', views.end_room, name='end-room'),
    path('rooms/<str:room_id>/status/', views.room_status, name='room-status'),
    path('rooms/<str:room_id>/signals/', views.room_signals, name='room-signals'),
    
    # RTC Signals
    path('signals/', views.RTCSignalListView.as_view(), name='rtc-signal-list'),
    
    # RTC Join Tokens
    path('join-tokens/', views.RTCJoinTokenListView.as_view(), name='rtc-join-token-list'),
]