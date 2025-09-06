'use client'
import React, { useState, useEffect } from 'react'
import { Button } from '@/components/ui/button'
import { Card } from '@/components/ui/card'

export default function WebSocketTestPage() {
  const [status, setStatus] = useState('Disconnected')
  const [messages, setMessages] = useState<string[]>([])
  const [ws, setWs] = useState<WebSocket | null>(null)
  const [roomId, setRoomId] = useState('test-room-123')

  const connectWebSocket = () => {
    if (ws) {
      ws.close()
    }

    const wsUrl = `ws://localhost:8000/ws/rtc/${roomId}/`
    console.log('Connecting to:', wsUrl)
    
    const socket = new WebSocket(wsUrl)
    setWs(socket)

    socket.onopen = () => {
      setStatus('Connected')
      addMessage('WebSocket connected successfully')
      
      // Send join message
      socket.send(JSON.stringify({
        type: 'join_room',
        user_id: 'test-user-456',
        is_doctor: false
      }))
    }

    socket.onclose = (event) => {
      setStatus('Disconnected')
      addMessage(`WebSocket disconnected: ${event.code} ${event.reason}`)
    }

    socket.onmessage = (event) => {
      try {
        const data = JSON.parse(event.data)
        addMessage(`Received: ${JSON.stringify(data)}`)
      } catch (err) {
        addMessage(`Raw message: ${event.data}`)
      }
    }

    socket.onerror = (error) => {
      setStatus('Error')
      addMessage(`WebSocket error: ${error}`)
    }
  }

  const disconnectWebSocket = () => {
    if (ws) {
      ws.close()
      setWs(null)
    }
  }

  const sendTestMessage = () => {
    if (ws && ws.readyState === WebSocket.OPEN) {
      ws.send(JSON.stringify({
        type: 'rtc_signal',
        signal_type: 'test',
        payload: 'hello from frontend'
      }))
    }
  }

  const addMessage = (message: string) => {
    setMessages(prev => [...prev, `${new Date().toLocaleTimeString()}: ${message}`])
  }

  const clearMessages = () => {
    setMessages([])
  }

  return (
    <div className="min-h-screen bg-gray-100 p-8">
      <div className="max-w-4xl mx-auto">
        <h1 className="text-3xl font-bold mb-8">WebSocket Test</h1>
        
        <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
          {/* Connection Controls */}
          <Card className="p-6">
            <h2 className="text-xl font-semibold mb-4">Connection</h2>
            
            <div className="space-y-4">
              <div>
                <label className="block text-sm font-medium mb-2">Room ID</label>
                <input
                  type="text"
                  value={roomId}
                  onChange={(e) => setRoomId(e.target.value)}
                  className="w-full p-2 border rounded"
                />
              </div>
              
              <div className="flex space-x-2">
                <Button onClick={connectWebSocket} disabled={ws?.readyState === WebSocket.OPEN}>
                  Connect
                </Button>
                <Button onClick={disconnectWebSocket} variant="destructive">
                  Disconnect
                </Button>
              </div>
              
              <div className="flex items-center space-x-2">
                <div className={`w-3 h-3 rounded-full ${
                  status === 'Connected' ? 'bg-green-500' : 
                  status === 'Error' ? 'bg-red-500' : 'bg-gray-500'
                }`} />
                <span className="font-medium">Status: {status}</span>
              </div>
            </div>
          </Card>

          {/* Message Controls */}
          <Card className="p-6">
            <h2 className="text-xl font-semibold mb-4">Messages</h2>
            
            <div className="space-y-4">
              <Button onClick={sendTestMessage} disabled={ws?.readyState !== WebSocket.OPEN}>
                Send Test Message
              </Button>
              <Button onClick={clearMessages} variant="outline">
                Clear Messages
              </Button>
            </div>
          </Card>
        </div>

        {/* Message Log */}
        <Card className="p-6 mt-6">
          <h2 className="text-xl font-semibold mb-4">Message Log</h2>
          <div className="bg-gray-900 text-green-400 p-4 rounded h-64 overflow-y-auto font-mono text-sm">
            {messages.length === 0 ? (
              <div className="text-gray-500">No messages yet...</div>
            ) : (
              messages.map((msg, index) => (
                <div key={index} className="mb-1">{msg}</div>
              ))
            )}
          </div>
        </Card>

        {/* Instructions */}
        <Card className="p-6 mt-6">
          <h2 className="text-xl font-semibold mb-4">Instructions</h2>
          <ol className="list-decimal list-inside space-y-2 text-gray-700">
            <li>Click "Connect" to establish WebSocket connection</li>
            <li>Check the status indicator (should turn green)</li>
            <li>Click "Send Test Message" to test communication</li>
            <li>Open another browser tab and repeat to test peer-to-peer</li>
            <li>Check the message log for real-time communication</li>
          </ol>
        </Card>
      </div>
    </div>
  )
}

