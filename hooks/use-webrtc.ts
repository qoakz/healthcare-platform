'use client'
import { useState, useEffect, useRef, useCallback } from 'react'
// WebSocket connection for Django Channels

interface WebRTCConfig {
  roomId: string
  userId: string
  isDoctor: boolean
}

interface RTCSignal {
  type: 'offer' | 'answer' | 'ice-candidate'
  payload: any
}

export const useWebRTC = (config: WebRTCConfig) => {
  const [isConnected, setIsConnected] = useState(false)
  const [isCallActive, setIsCallActive] = useState(false)
  const [localStream, setLocalStream] = useState<MediaStream | null>(null)
  const [remoteStream, setRemoteStream] = useState<MediaStream | null>(null)
  const [connectionState, setConnectionState] = useState<string>('new')
  const [error, setError] = useState<string | null>(null)

  const socketRef = useRef<WebSocket | null>(null)
  const peerConnectionRef = useRef<RTCPeerConnection | null>(null)
  const localVideoRef = useRef<HTMLVideoElement | null>(null)
  const remoteVideoRef = useRef<HTMLVideoElement | null>(null)

  // WebRTC Configuration
  const rtcConfig = {
    iceServers: [
      { urls: 'stun:stun.l.google.com:19302' },
      { urls: 'stun:stun1.l.google.com:19302' },
      // Add TURN servers for production
      // { urls: 'turn:your-turn-server.com:3478', username: 'user', credential: 'pass' }
    ]
  }

  // Initialize WebSocket connection
  useEffect(() => {
    if (!config.roomId || !config.userId) return

    const wsUrl = `ws://localhost:8000/ws/rtc/${config.roomId}/`
    console.log('Connecting to WebSocket:', wsUrl)
    
    const socket = new WebSocket(wsUrl)
    socketRef.current = socket

    socket.onopen = () => {
      console.log('WebSocket connected successfully')
      setIsConnected(true)
      setError(null)
      
      // Send join message
      socket.send(JSON.stringify({
        type: 'join_room',
        user_id: config.userId,
        is_doctor: config.isDoctor
      }))
    }

    socket.onclose = (event) => {
      console.log('WebSocket disconnected:', event.code, event.reason)
      setIsConnected(false)
      if (event.code !== 1000) {
        setError('WebSocket connection lost')
      }
    }

    socket.onmessage = (event) => {
      try {
        const data = JSON.parse(event.data)
        console.log('WebSocket message received:', data)
        handleWebSocketMessage(data)
      } catch (err) {
        console.error('Error parsing WebSocket message:', err)
      }
    }

    socket.onerror = (error) => {
      console.error('WebSocket error:', error)
      setError('WebSocket connection error')
    }

    return () => {
      if (socket.readyState === WebSocket.OPEN) {
        socket.close()
      }
    }
  }, [config.roomId, config.userId, config.isDoctor])

  // Initialize peer connection
  useEffect(() => {
    if (!isConnected) return

    const peerConnection = new RTCPeerConnection(rtcConfig)
    peerConnectionRef.current = peerConnection

    // Handle ICE candidates
    peerConnection.onicecandidate = (event) => {
      if (event.candidate) {
        sendSignal({
          type: 'ice-candidate',
          payload: event.candidate
        })
      }
    }

    // Handle remote stream
    peerConnection.ontrack = (event) => {
      console.log('Received remote stream')
      setRemoteStream(event.streams[0])
      if (remoteVideoRef.current) {
        remoteVideoRef.current.srcObject = event.streams[0]
      }
    }

    // Handle connection state changes
    peerConnection.onconnectionstatechange = () => {
      setConnectionState(peerConnection.connectionState)
      if (peerConnection.connectionState === 'connected') {
        setIsCallActive(true)
      } else if (peerConnection.connectionState === 'disconnected' || 
                 peerConnection.connectionState === 'failed') {
        setIsCallActive(false)
      }
    }

    return () => {
      peerConnection.close()
    }
  }, [isConnected])

  // Get user media
  const startLocalStream = useCallback(async () => {
    try {
      const stream = await navigator.mediaDevices.getUserMedia({
        video: true,
        audio: true
      })
      
      setLocalStream(stream)
      
      if (localVideoRef.current) {
        localVideoRef.current.srcObject = stream
      }

      // Add tracks to peer connection
      if (peerConnectionRef.current) {
        stream.getTracks().forEach(track => {
          peerConnectionRef.current!.addTrack(track, stream)
        })
      }

      return stream
    } catch (err) {
      console.error('Error accessing media devices:', err)
      setError('Failed to access camera/microphone. Please check permissions.')
      throw err
    }
  }, [])

  // Stop local stream
  const stopLocalStream = useCallback(() => {
    if (localStream) {
      localStream.getTracks().forEach(track => track.stop())
      setLocalStream(null)
    }
  }, [localStream])

  // Handle WebSocket messages
  const handleWebSocketMessage = useCallback((data: any) => {
    switch (data.type) {
      case 'rtc_signal':
        handleRemoteSignal(data)
        break
      case 'user_joined':
        handleUserJoined(data)
        break
      case 'user_left':
        handleUserLeft(data)
        break
      case 'error':
        handleError(data)
        break
    }
  }, [])

  // Send signal through WebSocket
  const sendSignal = useCallback((signal: RTCSignal) => {
    if (socketRef.current && isConnected) {
      socketRef.current.send(JSON.stringify({
        type: 'rtc_signal',
        signal_type: signal.type,
        payload: signal.payload
      }))
    }
  }, [isConnected])

  // Handle remote signals
  const handleRemoteSignal = useCallback(async (data: any) => {
    if (!peerConnectionRef.current) return

    try {
      const { signal_type, payload } = data

      switch (signal_type) {
        case 'offer':
          await peerConnectionRef.current.setRemoteDescription(payload)
          const answer = await peerConnectionRef.current.createAnswer()
          await peerConnectionRef.current.setLocalDescription(answer)
          sendSignal({ type: 'answer', payload: answer })
          break

        case 'answer':
          await peerConnectionRef.current.setRemoteDescription(payload)
          break

        case 'ice-candidate':
          await peerConnectionRef.current.addIceCandidate(payload)
          break
      }
    } catch (err) {
      console.error('Error handling remote signal:', err)
      setError('Failed to process remote signal')
    }
  }, [sendSignal])

  // Handle user joined
  const handleUserJoined = useCallback((data: any) => {
    console.log('User joined:', data.message)
  }, [])

  // Handle user left
  const handleUserLeft = useCallback((data: any) => {
    console.log('User left:', data.message)
    setRemoteStream(null)
    setIsCallActive(false)
  }, [])

  // Handle errors
  const handleError = useCallback((error: any) => {
    console.error('WebSocket error:', error)
    setError(error.message || 'WebSocket connection error')
  }, [])

  // Start call (create offer)
  const startCall = useCallback(async () => {
    if (!peerConnectionRef.current) return

    try {
      await startLocalStream()
      
      const offer = await peerConnectionRef.current.createOffer()
      await peerConnectionRef.current.setLocalDescription(offer)
      sendSignal({ type: 'offer', payload: offer })
    } catch (err) {
      console.error('Error starting call:', err)
      setError('Failed to start call')
    }
  }, [startLocalStream, sendSignal])

  // End call
  const endCall = useCallback(() => {
    if (peerConnectionRef.current) {
      peerConnectionRef.current.close()
    }
    stopLocalStream()
    setRemoteStream(null)
    setIsCallActive(false)
    setConnectionState('closed')
  }, [stopLocalStream])

  // Toggle mute
  const toggleMute = useCallback(() => {
    if (localStream) {
      const audioTrack = localStream.getAudioTracks()[0]
      if (audioTrack) {
        audioTrack.enabled = !audioTrack.enabled
      }
    }
  }, [localStream])

  // Toggle video
  const toggleVideo = useCallback(() => {
    if (localStream) {
      const videoTrack = localStream.getVideoTracks()[0]
      if (videoTrack) {
        videoTrack.enabled = !videoTrack.enabled
      }
    }
  }, [localStream])

  return {
    // State
    isConnected,
    isCallActive,
    localStream,
    remoteStream,
    connectionState,
    error,
    
    // Refs
    localVideoRef,
    remoteVideoRef,
    
    // Actions
    startCall,
    endCall,
    startLocalStream,
    stopLocalStream,
    toggleMute,
    toggleVideo,
    
    // Utils
    clearError: () => setError(null)
  }
}
