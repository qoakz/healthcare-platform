from django.db import models
from appointments.models import Appointment
from users.models import User

n the fronend
class RTCRoom(models.Model):
    """
    WebRTC room for video consultations
    """
    STATUS_CHOICES = [
        ('created', 'Created'),
        ('active', 'Active'),
        ('ended', 'Ended'),
        ('expired', 'Expired'),
    ]
    
    appointment = models.OneToOneField(Appointment, on_delete=models.CASCADE, related_name='rtc_room')
    room_id = models.CharField(max_length=255, unique=True)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='created')
    
    # Room configuration
    max_participants = models.PositiveIntegerField(default=2)
    recording_enabled = models.BooleanField(default=False)
    
    # Timestamps
    created_at = models.DateTimeField(auto_now_add=True)
    started_at = models.DateTimeField(null=True, blank=True)
    ended_at = models.DateTimeField(null=True, blank=True)
    expires_at = models.DateTimeField()
    
    class Meta:
        db_table = 'rtc_room'
        verbose_name = 'RTC Room'
        verbose_name_plural = 'RTC Rooms'
    
    def __str__(self):
        return f"Room {self.room_id} - {self.appointment}"


class RTCSignal(models.Model):
    """
    WebRTC signaling messages
    """
    SIGNAL_TYPE_CHOICES = [
        ('offer', 'Offer'),
        ('answer', 'Answer'),
        ('ice_candidate', 'ICE Candidate'),
        ('join', 'Join'),
        ('leave', 'Leave'),
    ]
    
    room = models.ForeignKey(RTCRoom, on_delete=models.CASCADE, related_name='signals')
    sender = models.ForeignKey(User, on_delete=models.CASCADE, related_name='rtc_signals')
    signal_type = models.CharField(max_length=20, choices=SIGNAL_TYPE_CHOICES)
    payload = models.JSONField()
    
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        db_table = 'rtc_signals'
        verbose_name = 'RTC Signal'
        verbose_name_plural = 'RTC Signals'
        ordering = ['-created_at']
    
    def __str__(self):
        return f"{self.signal_type} from {self.sender.get_full_name()} in {self.room.room_id}"


class RTCJoinToken(models.Model):
    """
    Short-lived tokens for joining RTC rooms
    """
    room = models.ForeignKey(RTCRoom, on_delete=models.CASCADE, related_name='join_tokens')
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='rtc_join_tokens')
    token = models.CharField(max_length=500)
    expires_at = models.DateTimeField()
    
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        db_table = 'rtc_join_token'
        verbose_name = 'RTC Join Token'
        verbose_name_plural = 'RTC Join Tokens'
    
    def __str__(self):
        return f"Join token for {self.user.get_full_name()} in {self.room.room_id}"
