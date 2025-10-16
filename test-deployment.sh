#!/bin/bash

# Test script for Boardinghouse Management System
# Run this after deploying to test if everything is working

echo "🧪 Testing Boardinghouse Management System..."
echo ""

# Test backend health
echo "1. Testing backend health..."
BACKEND_STATUS=$(curl -s -o /dev/null -w "%{http_code}" https://boardinghouse-backend.onrender.com/api/auth/login)
echo "Backend status: $BACKEND_STATUS"

if [ "$BACKEND_STATUS" = "404" ]; then
    echo "❌ Backend is not responding correctly"
    echo "💡 Try redeploying the backend service on Render"
    echo ""
else
    echo "✅ Backend is responding"
fi

# Test frontend
echo ""
echo "2. Testing frontend..."
FRONTEND_STATUS=$(curl -s -o /dev/null -w "%{http_code}" https://boardinghouse-frontend.onrender.com)
echo "Frontend status: $FRONTEND_STATUS"

if [ "$FRONTEND_STATUS" = "200" ]; then
    echo "✅ Frontend is deployed and accessible"
    echo ""
    echo "🌐 You can now access your application at:"
    echo "   Frontend: https://boardinghouse-frontend.onrender.com"
    echo "   Backend API: https://boardinghouse-backend.onrender.com/api"
    echo ""
    echo "📝 To test login:"
    echo "   1. Open the frontend URL in your browser"
    echo "   2. Try registering a new account first (or create one via API)"
    echo "   3. Then try logging in"
    echo ""
    echo "🔧 If login still doesn't work:"
    echo "   - Check that Neo4j database is connected"
    echo "   - Verify JWT_SECRET_KEY is set in Render dashboard"
    echo "   - Check browser console for API errors"
else
    echo "❌ Frontend deployment issue"
    echo "💡 Try redeploying the frontend service on Render"
fi
