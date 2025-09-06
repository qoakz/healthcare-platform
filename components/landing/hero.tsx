'use client'
import Link from 'next/link'
import { ArrowRight, Play, Shield, Clock, Users, Sparkles, Heart, Stethoscope, Star, Zap, Award, Globe } from 'lucide-react'
import { useEffect, useState } from 'react'

export function Hero() {
  const [isVisible, setIsVisible] = useState(false)

  useEffect(() => {
    setIsVisible(true)
  }, [])

  return (
    <section className="relative min-h-screen bg-gradient-to-br from-slate-900 via-purple-900 to-slate-900 overflow-hidden">
      {/* Modern Animated Background */}
      <div className="absolute inset-0">
        {/* Gradient Mesh */}
        <div className="absolute inset-0 bg-gradient-to-br from-indigo-500/20 via-purple-500/20 to-pink-500/20"></div>
        
        {/* Animated Orbs */}
        <div className="absolute -top-40 -right-40 w-96 h-96 bg-gradient-to-r from-cyan-400 to-blue-500 rounded-full mix-blend-multiply filter blur-3xl opacity-30 animate-pulse"></div>
        <div className="absolute -bottom-40 -left-40 w-96 h-96 bg-gradient-to-r from-purple-400 to-pink-500 rounded-full mix-blend-multiply filter blur-3xl opacity-30 animate-pulse"></div>
        <div className="absolute top-1/2 left-1/2 transform -translate-x-1/2 -translate-y-1/2 w-80 h-80 bg-gradient-to-r from-yellow-400 to-orange-500 rounded-full mix-blend-multiply filter blur-3xl opacity-20 animate-pulse"></div>
        
        {/* Grid Pattern */}
        <div className="absolute inset-0 bg-[linear-gradient(rgba(255,255,255,0.1)_1px,transparent_1px),linear-gradient(90deg,rgba(255,255,255,0.1)_1px,transparent_1px)] bg-[size:50px_50px]"></div>
      </div>

      {/* Floating Elements */}
      <div className="absolute inset-0 overflow-hidden pointer-events-none">
        <div className="absolute top-20 left-10 animate-float">
          <div className="w-16 h-16 bg-gradient-to-r from-pink-500 to-rose-500 rounded-2xl flex items-center justify-center shadow-2xl">
            <Heart className="h-8 w-8 text-white" />
          </div>
        </div>
        <div className="absolute top-40 right-20 animate-float-delayed">
          <div className="w-20 h-20 bg-gradient-to-r from-blue-500 to-cyan-500 rounded-2xl flex items-center justify-center shadow-2xl">
            <Stethoscope className="h-10 w-10 text-white" />
          </div>
        </div>
        <div className="absolute bottom-40 left-20 animate-float-slow">
          <div className="w-12 h-12 bg-gradient-to-r from-purple-500 to-indigo-500 rounded-2xl flex items-center justify-center shadow-2xl">
            <Sparkles className="h-6 w-6 text-white" />
          </div>
        </div>
        <div className="absolute bottom-20 right-10 animate-float">
          <div className="w-14 h-14 bg-gradient-to-r from-yellow-500 to-orange-500 rounded-2xl flex items-center justify-center shadow-2xl">
            <Star className="h-7 w-7 text-white" />
          </div>
        </div>
        <div className="absolute top-1/3 left-1/4 animate-float-delayed">
          <div className="w-10 h-10 bg-gradient-to-r from-emerald-500 to-teal-500 rounded-xl flex items-center justify-center shadow-xl">
            <Zap className="h-5 w-5 text-white" />
          </div>
        </div>
        <div className="absolute bottom-1/3 right-1/4 animate-float-slow">
          <div className="w-12 h-12 bg-gradient-to-r from-violet-500 to-purple-500 rounded-xl flex items-center justify-center shadow-xl">
            <Award className="h-6 w-6 text-white" />
          </div>
        </div>
      </div>

      <div className="relative max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-20">
        <div className="text-center">
          {/* Badge */}
          <div className={`inline-flex items-center px-4 py-2 rounded-full bg-white/10 backdrop-blur-sm border border-white/20 text-white text-sm font-medium mb-8 transition-all duration-1000 ${isVisible ? 'opacity-100 translate-y-0' : 'opacity-0 translate-y-10'}`}>
            <Sparkles className="h-4 w-4 mr-2 text-yellow-400" />
            Trusted by 50,000+ patients worldwide
          </div>

          {/* Main Heading with Animation */}
          <div className={`transition-all duration-1000 ${isVisible ? 'opacity-100 translate-y-0' : 'opacity-0 translate-y-10'}`}>
            <h1 className="text-6xl md:text-8xl font-black mb-8 leading-tight">
              <span className="bg-gradient-to-r from-cyan-400 via-blue-500 to-purple-600 bg-clip-text text-transparent animate-gradient">
                Future of
              </span>
              <br />
              <span className="text-white">
                Healthcare{' '}
                <span className="bg-gradient-to-r from-pink-400 to-rose-500 bg-clip-text text-transparent animate-gradient">
                  is Here
                </span>
              </span>
            </h1>
          </div>

          {/* Subtitle with Animation */}
          <div className={`transition-all duration-1000 delay-300 ${isVisible ? 'opacity-100 translate-y-0' : 'opacity-0 translate-y-10'}`}>
            <p className="text-2xl md:text-3xl text-gray-300 mb-12 max-w-5xl mx-auto leading-relaxed font-light">
              Experience the next generation of healthcare with AI-powered diagnostics, 
              virtual consultations, and personalized treatment plans.
            </p>
          </div>
          
          {/* CTA Buttons with Animation */}
          <div className={`flex flex-col sm:flex-row gap-8 justify-center mb-20 transition-all duration-1000 delay-500 ${isVisible ? 'opacity-100 translate-y-0' : 'opacity-0 translate-y-10'}`}>
            <Link
              href="/auth/register"
              className="group relative px-10 py-5 bg-gradient-to-r from-cyan-500 via-blue-500 to-purple-600 text-white font-bold text-xl rounded-2xl shadow-2xl hover:shadow-cyan-500/25 transition-all duration-500 transform hover:scale-110 hover:-translate-y-2"
            >
              <span className="relative z-10 flex items-center">
                Start Your Journey
                <ArrowRight className="ml-3 h-6 w-6 group-hover:translate-x-2 transition-transform duration-300" />
              </span>
              <div className="absolute inset-0 bg-gradient-to-r from-cyan-400 via-blue-400 to-purple-500 rounded-2xl opacity-0 group-hover:opacity-100 transition-opacity duration-500"></div>
            </Link>
            <Link
              href="/doctors"
              className="group px-10 py-5 bg-white/10 backdrop-blur-md text-white font-bold text-xl rounded-2xl shadow-2xl hover:shadow-white/25 transition-all duration-500 transform hover:scale-110 hover:-translate-y-2 border border-white/20 hover:border-white/40"
            >
              <span className="flex items-center">
                <Play className="mr-3 h-6 w-6 group-hover:scale-125 transition-transform duration-300" />
                Explore Doctors
              </span>
            </Link>
          </div>

          {/* Modern Stats Grid */}
          <div className={`grid grid-cols-1 md:grid-cols-4 gap-6 max-w-6xl mx-auto transition-all duration-1000 delay-700 ${isVisible ? 'opacity-100 translate-y-0' : 'opacity-0 translate-y-10'}`}>
            <div className="group text-center p-8 bg-white/5 backdrop-blur-md rounded-3xl border border-white/10 hover:bg-white/10 transition-all duration-500 transform hover:scale-105 hover:-translate-y-2">
              <div className="w-16 h-16 bg-gradient-to-r from-emerald-500 to-teal-500 rounded-2xl flex items-center justify-center mx-auto mb-4 group-hover:scale-110 transition-transform duration-300">
                <Shield className="h-8 w-8 text-white" />
              </div>
              <div className="text-3xl font-black text-white mb-2">100%</div>
              <div className="text-gray-300 font-semibold">HIPAA Compliant</div>
              <div className="text-sm text-gray-400 mt-1">Bank-level security</div>
            </div>
            
            <div className="group text-center p-8 bg-white/5 backdrop-blur-md rounded-3xl border border-white/10 hover:bg-white/10 transition-all duration-500 transform hover:scale-105 hover:-translate-y-2">
              <div className="w-16 h-16 bg-gradient-to-r from-blue-500 to-cyan-500 rounded-2xl flex items-center justify-center mx-auto mb-4 group-hover:scale-110 transition-transform duration-300">
                <Clock className="h-8 w-8 text-white" />
              </div>
              <div className="text-3xl font-black text-white mb-2">24/7</div>
              <div className="text-gray-300 font-semibold">Always Available</div>
              <div className="text-sm text-gray-400 mt-1">Round-the-clock care</div>
            </div>
            
            <div className="group text-center p-8 bg-white/5 backdrop-blur-md rounded-3xl border border-white/10 hover:bg-white/10 transition-all duration-500 transform hover:scale-105 hover:-translate-y-2">
              <div className="w-16 h-16 bg-gradient-to-r from-purple-500 to-pink-500 rounded-2xl flex items-center justify-center mx-auto mb-4 group-hover:scale-110 transition-transform duration-300">
                <Users className="h-8 w-8 text-white" />
              </div>
              <div className="text-3xl font-black text-white mb-2">500+</div>
              <div className="text-gray-300 font-semibold">Expert Doctors</div>
              <div className="text-sm text-gray-400 mt-1">Verified specialists</div>
            </div>
            
            <div className="group text-center p-8 bg-white/5 backdrop-blur-md rounded-3xl border border-white/10 hover:bg-white/10 transition-all duration-500 transform hover:scale-105 hover:-translate-y-2">
              <div className="w-16 h-16 bg-gradient-to-r from-yellow-500 to-orange-500 rounded-2xl flex items-center justify-center mx-auto mb-4 group-hover:scale-110 transition-transform duration-300">
                <Globe className="h-8 w-8 text-white" />
              </div>
              <div className="text-3xl font-black text-white mb-2">50K+</div>
              <div className="text-gray-300 font-semibold">Happy Patients</div>
              <div className="text-sm text-gray-400 mt-1">Worldwide trust</div>
            </div>
          </div>

          {/* Additional Features */}
          <div className={`mt-16 transition-all duration-1000 delay-1000 ${isVisible ? 'opacity-100 translate-y-0' : 'opacity-0 translate-y-10'}`}>
            <div className="flex flex-wrap justify-center gap-4">
              <div className="px-6 py-3 bg-white/10 backdrop-blur-sm rounded-full border border-white/20 text-white text-sm font-medium">
                🤖 AI-Powered Diagnostics
              </div>
              <div className="px-6 py-3 bg-white/10 backdrop-blur-sm rounded-full border border-white/20 text-white text-sm font-medium">
                📱 Mobile App Available
              </div>
              <div className="px-6 py-3 bg-white/10 backdrop-blur-sm rounded-full border border-white/20 text-white text-sm font-medium">
                💊 Prescription Management
              </div>
              <div className="px-6 py-3 bg-white/10 backdrop-blur-sm rounded-full border border-white/20 text-white text-sm font-medium">
                🏥 Hospital Integration
              </div>
            </div>
          </div>
        </div>
      </div>
    </section>
  )
}
