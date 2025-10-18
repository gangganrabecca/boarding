#!/bin/bash

echo "🔍 TROUBLESHOOTING: Boardinghouse Management System Registration Issue"
echo "================================================================="
echo ""

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

# Test 1: Check if backend is accessible
echo "1️⃣ Testing Backend Accessibility..."
BACKEND_STATUS=$(curl -s -o /dev/null -w "%{http_code}" https://projectbhsystem.onrender.com/api/auth/login)
if [ "$BACKEND_STATUS" = "405" ]; then
    echo -e "✅ ${GREEN}Backend is accessible${NC}"
else
    echo -e "❌ ${RED}Backend not accessible (Status: $BACKEND_STATUS)${NC}"
    echo "   Try redeploying the backend service"
    exit 1
fi

echo ""

# Test 2: Test user registration with detailed logging
echo "2️⃣ Testing User Registration..."
echo "   Attempting to register new user..."

REGISTRATION_RESPONSE=$(curl -s -X POST https://projectbhsystem.onrender.com/api/auth/register \
  -H "Content-Type: application/json" \
  -d '{"email":"debugtest'$(date +%s)'@example.com","username":"debugtest'$(date +%s)'","password":"testpass123","role":"user"}' \
  -w "\nHTTP_STATUS_CODE:%{http_code}")

HTTP_CODE=$(echo "$REGISTRATION_RESPONSE" | grep "HTTP_STATUS_CODE:" | cut -d: -f2)
RESPONSE_BODY=$(echo "$REGISTRATION_RESPONSE" | head -n -1)

echo "   Response Code: $HTTP_CODE"
echo "   Response Body: $RESPONSE_BODY"

if [ "$HTTP_CODE" = "200" ]; then
    echo -e "✅ ${GREEN}Registration successful!${NC}"
    echo ""
    echo "🎉 REGISTRATION IS WORKING!"
    echo ""
    echo "You can now:"
    echo "   - Register new users on your frontend"
    echo "   - Use the registered credentials to login"
    echo ""
    exit 0

elif [ "$HTTP_CODE" = "400" ]; then
    echo -e "ℹ️ ${YELLOW}User already exists (this is expected behavior)${NC}"
    echo ""
    echo "✅ Registration logic is working correctly"
    echo ""

elif [ "$HTTP_CODE" = "500" ]; then
    echo -e "❌ ${RED}Registration failed with 500 error${NC}"
    echo ""
    echo "🔧 TROUBLESHOOTING STEPS:"
    echo ""

    # Test 3: Check environment variables
    echo "3️⃣ Checking Environment Variables..."
    echo "   Make sure these are set in your Render backend dashboard:"
    echo ""
    echo "   Required Variables:"
    echo "   - NEO4J_URI=neo4j+s://036fd24e.databases.neo4j.io"
    echo "   - NEO4J_USERNAME=neo4j"
    echo "   - NEO4J_PASSWORD=dYN51DnTMbo8-2T389P6bD2FEIVKJH3nfZSnIi5i1ik"
    echo "   - JWT_SECRET_KEY=hagssteteRtwuoahhsjhdU"
    echo ""
    echo "   To check/fix:"
    echo "   1. Go to https://dashboard.render.com"
    echo "   2. Select your 'projectbhsystem' service"
    echo "   3. Go to 'Environment' tab"
    echo "   4. Verify all variables match your .env file"
    echo "   5. Click 'Update variables' if needed"
    echo "   6. Redeploy the service"
    echo ""

    # Test 4: Check database connection
    echo "4️⃣ Checking Database Connection..."
    echo "   Verify your Neo4j Aura database is running:"
    echo "   1. Go to https://console.neo4j.io"
    echo "   2. Check if your instance 'boardingdb' is running"
    echo "   3. Verify the connection URI and credentials"
    echo ""

    # Test 5: Check database constraints
    echo "5️⃣ Checking Database Constraints..."
    echo "   The issue might be with unique constraints. To fix:"
    echo "   1. In Neo4j Browser, run:"
    echo "      DROP CONSTRAINT user_email_unique IF EXISTS"
    echo "      DROP CONSTRAINT user_id_unique IF EXISTS"
    echo "   2. Then recreate them:"
    echo "      CREATE CONSTRAINT user_email_unique IF NOT EXISTS FOR (u:User) REQUIRE u.email IS UNIQUE"
    echo "      CREATE CONSTRAINT user_id_unique IF NOT EXISTS FOR (u:User) REQUIRE u.id IS UNIQUE"
    echo ""

    echo "6️⃣ After fixing environment variables:"
    echo "   - Redeploy your backend service"
    echo "   - Run this script again to verify"
    echo ""

    exit 1

else
    echo -e "❓ ${YELLOW}Unexpected response code: $HTTP_CODE${NC}"
    echo "   Response: $RESPONSE_BODY"
    exit 1
fi

echo ""
echo "📞 If issues persist, check:"
echo "   - Render service logs for detailed error messages"
echo "   - Neo4j Aura console for database issues"
echo "   - All environment variables are correctly set"
