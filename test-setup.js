#!/usr/bin/env node

const http = require('http');
const https = require('https');

console.log('🧪 Healthcare Platform Setup Test');
console.log('=====================================\n');

// Test function to check if a server is running
function testServer(port, name, isHttps = false) {
  return new Promise((resolve) => {
    const client = isHttps ? https : http;
    const req = client.request({
      hostname: 'localhost',
      port: port,
      path: '/',
      method: 'GET',
      timeout: 3000
    }, (res) => {
      console.log(`✅ ${name} is running on port ${port}`);
      resolve(true);
    });

    req.on('error', (err) => {
      console.log(`❌ ${name} is not running on port ${port}`);
      resolve(false);
    });

    req.on('timeout', () => {
      console.log(`⏰ ${name} timeout on port ${port}`);
      req.destroy();
      resolve(false);
    });

    req.end();
  });
}

// Test API endpoints
async function testAPI() {
  console.log('🔍 Testing API Endpoints...');
  
  const endpoints = [
    { path: '/api/doctors/', name: 'Doctors API' },
    { path: '/api/appointments/', name: 'Appointments API' },
    { path: '/api/auth/', name: 'Auth API' },
    { path: '/admin/', name: 'Django Admin' }
  ];

  for (const endpoint of endpoints) {
    try {
      const response = await fetch(`http://localhost:8000${endpoint.path}`);
      if (response.ok || response.status === 401 || response.status === 403) {
        console.log(`✅ ${endpoint.name} - Status: ${response.status}`);
      } else {
        console.log(`⚠️  ${endpoint.name} - Status: ${response.status}`);
      }
    } catch (error) {
      console.log(`❌ ${endpoint.name} - Error: ${error.message}`);
    }
  }
}

// Test frontend
async function testFrontend() {
  console.log('\n🌐 Testing Frontend...');
  
  try {
    const response = await fetch('http://localhost:3000');
    if (response.ok) {
      console.log('✅ Frontend is running on port 3000');
      return true;
    } else {
      console.log(`⚠️  Frontend returned status: ${response.status}`);
      return false;
    }
  } catch (error) {
    console.log(`❌ Frontend not accessible - Error: ${error.message}`);
    return false;
  }
}

// Main test function
async function runTests() {
  console.log('1. Testing Servers...\n');
  
  const frontendRunning = await testServer(3000, 'Frontend (Next.js)');
  const backendRunning = await testServer(8000, 'Backend (Django)');
  
  if (backendRunning) {
    console.log('\n2. Testing API Endpoints...\n');
    await testAPI();
  }
  
  if (frontendRunning) {
    console.log('\n3. Frontend Status...\n');
    await testFrontend();
  }
  
  console.log('\n📋 Test Summary:');
  console.log('================');
  console.log(`Frontend (Next.js): ${frontendRunning ? '✅ Running' : '❌ Not Running'}`);
  console.log(`Backend (Django): ${backendRunning ? '✅ Running' : '❌ Not Running'}`);
  
  if (frontendRunning && backendRunning) {
    console.log('\n🎉 Setup is working! You can now:');
    console.log('   • Visit http://localhost:3000 for the frontend');
    console.log('   • Visit http://localhost:8000/admin for Django admin');
    console.log('   • Visit http://localhost:8000/api/ for API endpoints');
  } else {
    console.log('\n🔧 To start the servers:');
    if (!frontendRunning) {
      console.log('   Frontend: cd app && npm run dev');
    }
    if (!backendRunning) {
      console.log('   Backend: cd api && python manage.py runserver');
    }
  }
}

// Run the tests
runTests().catch(console.error);
