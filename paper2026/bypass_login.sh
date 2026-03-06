#!/bin/bash

echo "🛠️  N8N Login Bypass & Direct Setup"
echo "==================================="

# Colors
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m'

echo -e "${BLUE}🔍 Testing N8N API endpoints...${NC}"

# Test if N8N needs setup
echo -e "${YELLOW}1. Checking setup status:${NC}"
SETUP_STATUS=$(curl -s http://localhost:5678/rest/settings | jq -r '.data.userManagement.isInstanceOwnerSetUp // "unknown"' 2>/dev/null)
echo "   Owner setup status: $SETUP_STATUS"

# Test login endpoint
echo -e "${YELLOW}2. Testing login endpoint:${NC}"
LOGIN_RESPONSE=$(curl -s -o /dev/null -w "%{http_code}" http://localhost:5678/rest/login 2>/dev/null)
echo "   Login endpoint: HTTP $LOGIN_RESPONSE"

# Test if we can access without auth
echo -e "${YELLOW}3. Testing direct access:${NC}"
DIRECT_ACCESS=$(curl -s -o /dev/null -w "%{http_code}" http://localhost:5678/workflows 2>/dev/null)
echo "   Workflows endpoint: HTTP $DIRECT_ACCESS"

echo ""
echo -e "${BLUE}🔧 Alternative Solutions:${NC}"
echo ""

if [[ "$SETUP_STATUS" == "false" || "$SETUP_STATUS" == "null" ]]; then
    echo -e "${GREEN}✅ N8N needs owner setup - this is normal!${NC}"
    echo -e "${YELLOW}Try these URLs directly in your browser:${NC}"
    echo -e "   🔗 http://localhost:5678/setup"
    echo -e "   🔗 http://localhost:5678/#/setup"  
    echo -e "   🔗 http://localhost:5678/signin?redirect=/"
    echo ""
    echo -e "${BLUE}💡 Setup Instructions:${NC}"
    echo -e "   1. Open incognito/private browser window"
    echo -e "   2. Go to one of the URLs above"
    echo -e "   3. Create owner account with these details:"
    echo -e "      📧 Email: admin@personality-ai.local"
    echo -e "      🔑 Password: admin123"
    echo -e "      👤 Name: Admin User"
else
    echo -e "${YELLOW}⚠️  Owner might already be set up${NC}"
    echo -e "${BLUE}Try logging in with:${NC}"
    echo -e "   📧 Email: admin@personality-ai.local"
    echo -e "   🔑 Password: admin123"
fi

echo ""
echo -e "${BLUE}🚨 Nuclear Option - Complete Reset:${NC}"
echo -e "${YELLOW}If nothing works, run this to reset N8N completely:${NC}"
echo -e "   docker-compose down"
echo -e "   docker volume rm mvp_n8n_data"
echo -e "   docker-compose up -d"
echo ""
echo -e "${GREEN}🎯 This will give you a fresh N8N installation!${NC}"



































































