'use client'
import React, { useEffect, useState } from 'react'
import { useWebRTC } from '@/hooks/use-webrtc'
import { Button } from '@/components/ui/button'
import { Card } from '@/components/ui/card'
import { Badge } from '@/components/ui/badge'
import { 
  Phone, 
  PhoneOff, 
  Mic, 
  MicOff, 
  Video, 
  VideoOff, 
  Settings,
  Users,
  AlertCircle
} from 'lucide-react'

interface VideoCallProps {
  roomId: string
  userId: string
  isDoctor: boolean
  onEndCall: () => void
}

export const VideoCall: React.FC<VideoCallProps> = ({
  roomId,
  userId,
  isDoctor,
  onEndCall
}) => {
  const [isMuted, setIsMuted] = useState(false)
  const [isVideoOff, setIsVideoOff] = useState(false)
  const [showSettings, setShowSettings] = useState(false)

  const {
    isConnected,
    isCallActive,
    localStream,
    remoteStream,
    connectionState,
    error,
    localVideoRef,
    remoteVideoRef,
    startCall,
    endCall,
    startLocalStream,
    stopLocalStream,
    toggleMute,
    toggleVideo,
    clearError
  } = useWebRTC({
    roomId,
    userId,
    isDoctor
  })

  // Auto-start local stream when component mounts
  useEffect(() => {
    startLocalStream().catch(console.error)
    
    return () => {
      stopLocalStream()
    }
  }, [startLocalStream, stopLocalStream])

  const handleStartCall = async () => {
    try {
      await startCall()
    } catch (err) {
      console.error('Failed to start call:', err)
    }
  }

  const handleEndCall = () => {
    endCall()
    onEndCall()
  }

  const handleToggleMute = () => {
    toggleMute()
    setIsMuted(!isMuted)
  }

  const handleToggleVideo = () => {
    toggleVideo()
    setIsVideoOff(!isVideoOff)
  }

  const getConnectionStatusColor = () => {
    switch (connectionState) {
      case 'connected': return 'bg-green-500'
      case 'connecting': return 'bg-yellow-500'
      case 'disconnected': return 'bg-red-500'
      case 'failed': return 'bg-red-500'
      default: return 'bg-gray-500'
    }
  }

  const getConnectionStatusText = () => {
    switch (connectionState) {
      case 'connected': return 'Connected'
      case 'connecting': return 'Connecting...'
      case 'disconnected': return 'Disconnected'
      case 'failed': return 'Connection Failed'
      default: return 'New'
    }
  }

  return (
    <div className="flex flex-col h-screen bg-gray-900 text-white">
      {/* Header */}
      <div className="flex items-center justify-between p-4 bg-gray-800 border-b border-gray-700">
        <div className="flex items-center space-x-4">
          <div className="flex items-center space-x-2">
            <div className={`w-3 h-3 rounded-full ${getConnectionStatusColor()}`} />
            <span className="text-sm font-medium">{getConnectionStatusText()}</span>
          </div>
          <Badge variant={isDoctor ? "default" : "secondary"}>
            {isDoctor ? 'Doctor' : 'Patient'}
          </Badge>
        </div>
        
        <div className="flex items-center space-x-2">
          <Button
            variant="ghost"
            size="sm"
            onClick={() => setShowSettings(!showSettings)}
          >
            <Settings className="w-4 h-4" />
          </Button>
          <Button
            variant="ghost"
            size="sm"
            onClick={handleEndCall}
            className="text-red-400 hover:text-red-300"
          >
            <PhoneOff className="w-4 h-4" />
          </Button>
        </div>
      </div>

      {/* Error Display */}
      {error && (
        <div className="flex items-center space-x-2 p-4 bg-red-900 border-b border-red-700">
          <AlertCircle className="w-5 h-5 text-red-400" />
          <span className="text-sm">{error}</span>
          <Button
            variant="ghost"
            size="sm"
            onClick={clearError}
            className="text-red-400 hover:text-red-300"
          >
            ×
          </Button>
        </div>
      )}

      {/* Main Video Area */}
      <div className="flex-1 relative">
        {/* Remote Video (Main) */}
        <div className="absolute inset-0 bg-gray-800">
          {remoteStream ? (
            <video
              ref={remoteVideoRef}
              autoPlay
              playsInline
              className="w-full h-full object-cover"
            />
          ) : (
            <div className="flex items-center justify-center h-full">
              <div className="text-center">
                <Users className="w-16 h-16 text-gray-400 mx-auto mb-4" />
                <p className="text-lg text-gray-400">Waiting for {isDoctor ? 'patient' : 'doctor'} to join...</p>
                {!isCallActive && (
                  <Button
                    onClick={handleStartCall}
                    className="mt-4"
                    disabled={!isConnected}
                  >
                    <Phone className="w-4 h-4 mr-2" />
                    Start Call
                  </Button>
                )}
              </div>
            </div>
          )}
        </div>

        {/* Local Video (Picture-in-Picture) */}
        {localStream && (
          <div className="absolute top-4 right-4 w-48 h-36 bg-gray-800 rounded-lg overflow-hidden border-2 border-gray-600">
            <video
              ref={localVideoRef}
              autoPlay
              playsInline
              muted
              className="w-full h-full object-cover"
            />
          </div>
        )}

        {/* Call Controls */}
        <div className="absolute bottom-8 left-1/2 transform -translate-x-1/2">
          <Card className="p-4 bg-gray-800/90 backdrop-blur-sm border-gray-700">
            <div className="flex items-center space-x-4">
              <Button
                variant={isMuted ? "destructive" : "secondary"}
                size="lg"
                onClick={handleToggleMute}
                className="rounded-full w-12 h-12"
              >
                {isMuted ? <MicOff className="w-5 h-5" /> : <Mic className="w-5 h-5" />}
              </Button>

              <Button
                variant="destructive"
                size="lg"
                onClick={handleEndCall}
                className="rounded-full w-14 h-14"
              >
                <PhoneOff className="w-6 h-6" />
              </Button>

              <Button
                variant={isVideoOff ? "destructive" : "secondary"}
                size="lg"
                onClick={handleToggleVideo}
                className="rounded-full w-12 h-12"
              >
                {isVideoOff ? <VideoOff className="w-5 h-5" /> : <Video className="w-5 h-5" />}
              </Button>
            </div>
          </Card>
        </div>
      </div>

      {/* Settings Panel */}
      {showSettings && (
        <div className="absolute top-16 right-4 w-64 bg-gray-800 rounded-lg border border-gray-700 p-4">
          <h3 className="text-lg font-semibold mb-4">Call Settings</h3>
          
          <div className="space-y-4">
            <div>
              <label className="text-sm text-gray-300">Connection Status</label>
              <p className="text-sm">{getConnectionStatusText()}</p>
            </div>
            
            <div>
              <label className="text-sm text-gray-300">Room ID</label>
              <p className="text-sm font-mono">{roomId}</p>
            </div>
            
            <div>
              <label className="text-sm text-gray-300">User ID</label>
              <p className="text-sm font-mono">{userId}</p>
            </div>
          </div>
        </div>
      )}
    </div>
  )
}
