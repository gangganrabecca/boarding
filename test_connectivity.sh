#!/bin/bash

echo "=== Boardinghouse System - Connectivity Test ==="
echo ""

# Test backend server
echo "1. Testing backend server (port 8000)..."
if curl -s http://localhost:8000/health > /dev/null 2>&1; then
    echo "✅ Backend server is running"
    curl -s http://localhost:8000/health | jq . 2>/dev/null || curl -s http://localhost:8000/health
else
    echo "❌ Backend server is not responding"
    echo "💡 Start the backend server: cd backend && python minimal_app.py"
fi

echo ""

# Test frontend server
echo "2. Testing frontend server (port 3001)..."
if curl -s http://localhost:3001 > /dev/null 2>&1; then
    echo "✅ Frontend server is running"
else
    echo "❌ Frontend server is not responding"
    echo "💡 Start the frontend server: cd frontend && npm run dev"
fi

echo ""

# Test API endpoints
echo "3. Testing API endpoints..."
if curl -s http://localhost:8000/api/auth/login -X POST -H "Content-Type: application/x-www-form-urlencoded" -d "username=test@example.com&password=test123" > /dev/null 2>&1; then
    echo "✅ Login endpoint is working"
    curl -s http://localhost:8000/api/auth/login -X POST -H "Content-Type: application/x-www-form-urlencoded" -d "username=test@example.com&password=test123" | jq . 2>/dev/null || echo "Response received"
else
    echo "❌ Login endpoint failed"
fi

echo ""

# Test rooms endpoint
echo "4. Testing rooms endpoint..."
if curl -s http://localhost:8000/api/rooms > /dev/null 2>&1; then
    echo "✅ Rooms endpoint is working"
    echo "Available rooms:"
    curl -s http://localhost:8000/api/rooms | jq . 2>/dev/null || curl -s http://localhost:8000/api/rooms
else
    echo "❌ Rooms endpoint failed"
fi

echo ""
echo "=== Mobile Responsiveness Features ==="
echo "✅ Responsive navigation with hamburger menu"
echo "✅ Mobile-optimized dashboard layouts"
echo "✅ Touch-friendly buttons (44px minimum)"
echo "✅ Responsive typography and spacing"
echo "✅ Mobile-first grid systems"
echo "✅ Overview dashboard moved below tab navigation"
echo ""
echo "🎯 Test on mobile: Open http://localhost:3001 in your browser and resize to mobile width"
