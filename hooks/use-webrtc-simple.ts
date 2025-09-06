'use client'
import { useState, useEffect, useRef, useCallback } from 'react'

interface WebRTCConfig {
  roomId: string
  userId: string
  isDoctor: boolean
}

interface RTCSignal {
  type: 'offer' | 'answer' | 'ice-candidate'
  payload: any
}

export const useWebRTCSimple = (config: WebRTCConfig) => {
  const [isConnected, setIsConnected] = useState(false)
  const [isCallActive, setIsCallActive] = useState(false)
  const [localStream, setLocalStream] = useState<MediaStream | null>(null)
  const [remoteStream, setRemoteStream] = useState<MediaStream | null>(null)
  const [connectionState, setConnectionState] = useState<string>('new')
  const [error, setError] = useState<string | null>(null)

  const peerConnectionRef = useRef<RTCPeerConnection | null>(null)
  const localVideoRef = useRef<HTMLVideoElement | null>(null)
  const remoteVideoRef = useRef<HTMLVideoElement | null>(null)
  const pollingIntervalRef = useRef<NodeJS.Timeout | null>(null)

  // WebRTC Configuration
  const rtcConfig = {
    iceServers: [
      { urls: 'stun:stun.l.google.com:19302' },
      { urls: 'stun:stun1.l.google.com:19302' },
    ]
  }

  // Initialize peer connection
  useEffect(() => {
    const peerConnection = new RTCPeerConnection(rtcConfig)
    peerConnectionRef.current = peerConnection

    // Handle ICE candidates
    peerConnection.onicecandidate = (event) => {
      if (event.candidate) {
        // Store candidate for later sending
        console.log('ICE candidate generated:', event.candidate)
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
        setIsConnected(true)
      } else if (peerConnection.connectionState === 'disconnected' || 
                 peerConnection.connectionState === 'failed') {
        setIsCallActive(false)
      }
    }

    return () => {
      peerConnection.close()
    }
  }, [])

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

  // Start call (create offer)
  const startCall = useCallback(async () => {
    if (!peerConnectionRef.current) return

    try {
      await startLocalStream()
      
      const offer = await peerConnectionRef.current.createOffer()
      await peerConnectionRef.current.setLocalDescription(offer)
      
      console.log('Call started, offer created:', offer)
      setIsConnected(true)
    } catch (err) {
      console.error('Error starting call:', err)
      setError('Failed to start call')
    }
  }, [startLocalStream])

  // End call
  const endCall = useCallback(() => {
    if (peerConnectionRef.current) {
      peerConnectionRef.current.close()
    }
    stopLocalStream()
    setRemoteStream(null)
    setIsCallActive(false)
    setIsConnected(false)
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

