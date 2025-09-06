import json
from channels.generic.websocket import AsyncWebsocketConsumer
from channels.db import database_sync_to_async
from django.contrib.auth.models import AnonymousUser
from .models import RTCRoom, RTCSignal


class RTCConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        self.room_id = self.scope['url_route']['kwargs']['room_id']
        self.room_group_name = f'rtc_room_{self.room_id}'
        
        # For now, accept all connections (in production, add proper authentication)
        # TODO: Add JWT token validation here
        
        # Join room group
        await self.channel_layer.group_add(
            self.room_group_name,
            self.channel_name
        )
        
        await self.accept()
        
        # Send join message
        await self.channel_layer.group_send(
            self.room_group_name,
            {
                'type': 'user_joined',
                'message': f'User joined room {self.room_id}'
            }
        )
    
    async def disconnect(self, close_code):
        # Leave room group
        await self.channel_layer.group_discard(
            self.room_group_name,
            self.channel_name
        )
    
    async def receive(self, text_data):
        try:
            data = json.loads(text_data)
            message_type = data.get('type')
            
            if message_type == 'rtc_signal':
                await self.handle_rtc_signal(data)
            elif message_type == 'join_room':
                await self.handle_join_room(data)
            elif message_type == 'leave_room':
                await self.handle_leave_room(data)
            
        except json.JSONDecodeError:
            await self.send(text_data=json.dumps({
                'type': 'error',
                'message': 'Invalid JSON'
            }))
    
    async def handle_rtc_signal(self, data):
        """Handle WebRTC signaling messages"""
        signal_type = data.get('signal_type')
        payload = data.get('payload')
        
        if not signal_type or not payload:
            await self.send(text_data=json.dumps({
                'type': 'error',
                'message': 'Missing signal_type or payload'
            }))
            return
        
        # Save signal to database
        await self.save_rtc_signal(signal_type, payload)
        
        # Broadcast to room group
        await self.channel_layer.group_send(
            self.room_group_name,
            {
                'type': 'rtc_signal',
                'signal_type': signal_type,
                'payload': payload,
                'sender_id': self.scope['user'].id if self.scope['user'] != AnonymousUser() else None
            }
        )
    
    async def handle_join_room(self, data):
        """Handle user joining the room"""
        user_id = self.scope['user'].id if self.scope['user'] != AnonymousUser() else None
        
        await self.channel_layer.group_send(
            self.room_group_name,
            {
                'type': 'user_joined',
                'user_id': user_id,
                'message': f'User {user_id} joined the room'
            }
        )
    
    async def handle_leave_room(self, data):
        """Handle user leaving the room"""
        user_id = self.scope['user'].id if self.scope['user'] != AnonymousUser() else None
        
        await self.channel_layer.group_send(
            self.room_group_name,
            {
                'type': 'user_left',
                'user_id': user_id,
                'message': f'User {user_id} left the room'
            }
        )
    
    async def rtc_signal(self, event):
        """Receive RTC signal from room group"""
        # Don't send the signal back to the sender
        sender_id = event.get('sender_id')
        current_user_id = self.scope['user'].id if self.scope['user'] != AnonymousUser() else None
        
        if sender_id != current_user_id:
            await self.send(text_data=json.dumps({
                'type': 'rtc_signal',
                'signal_type': event['signal_type'],
                'payload': event['payload']
            }))
    
    async def user_joined(self, event):
        """Handle user joined event"""
        await self.send(text_data=json.dumps({
            'type': 'user_joined',
            'message': event['message']
        }))
    
    async def user_left(self, event):
        """Handle user left event"""
        await self.send(text_data=json.dumps({
            'type': 'user_left',
            'message': event['message']
        }))
    
    @database_sync_to_async
    def save_rtc_signal(self, signal_type, payload):
        """Save RTC signal to database"""
        try:
            room = RTCRoom.objects.get(room_id=self.room_id)
            user = self.scope['user']
            
            if user != AnonymousUser():
                RTCSignal.objects.create(
                    room=room,
                    sender=user,
                    signal_type=signal_type,
                    payload=payload
                )
        except RTCRoom.DoesNotExist:
            pass
