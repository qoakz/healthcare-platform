'use client'
import React, { useState } from 'react'
import { VideoCall } from '@/components/video-call/video-call'
import { Button } from '@/components/ui/button'
import { Input } from '@/components/ui/input'
import { Card } from '@/components/ui/card'

export default function TestVideoPage() {
  const [roomId, setRoomId] = useState('test-room-123')
  const [userId, setUserId] = useState('test-user-456')
  const [isDoctor, setIsDoctor] = useState(false)
  const [startCall, setStartCall] = useState(false)

  if (startCall) {
    return (
      <VideoCall
        roomId={roomId}
        userId={userId}
        isDoctor={isDoctor}
        onEndCall={() => setStartCall(false)}
      />
    )
  }

  return (
    <div className="min-h-screen bg-gray-100 flex items-center justify-center p-4">
      <Card className="w-full max-w-md p-6">
        <h1 className="text-2xl font-bold text-center mb-6">Test Video Call</h1>
        
        <div className="space-y-4">
          <div>
            <label className="block text-sm font-medium text-gray-700 mb-2">
              Room ID
            </label>
            <Input
              value={roomId}
              onChange={(e) => setRoomId(e.target.value)}
              placeholder="Enter room ID"
            />
          </div>
          
          <div>
            <label className="block text-sm font-medium text-gray-700 mb-2">
              User ID
            </label>
            <Input
              value={userId}
              onChange={(e) => setUserId(e.target.value)}
              placeholder="Enter user ID"
            />
          </div>
          
          <div className="flex items-center space-x-2">
            <input
              type="checkbox"
              id="isDoctor"
              checked={isDoctor}
              onChange={(e) => setIsDoctor(e.target.checked)}
              className="rounded"
            />
            <label htmlFor="isDoctor" className="text-sm font-medium text-gray-700">
              I am a doctor
            </label>
          </div>
          
          <Button
            onClick={() => setStartCall(true)}
            className="w-full"
          >
            Start Video Call
          </Button>
        </div>
        
        <div className="mt-6 text-sm text-gray-600">
          <p><strong>Instructions:</strong></p>
          <ul className="list-disc list-inside mt-2 space-y-1">
            <li>Open this page in two different browser tabs</li>
            <li>Use the same Room ID in both tabs</li>
            <li>Set one as doctor, one as patient</li>
            <li>Click "Start Video Call" in both tabs</li>
            <li>Allow camera/microphone permissions</li>
          </ul>
        </div>
      </Card>
    </div>
  )
}

