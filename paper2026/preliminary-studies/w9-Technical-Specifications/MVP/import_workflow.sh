#!/bin/bash

echo "🚀 N8N Workflow Import & MVP Setup Assistant"
echo "============================================="

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Check if N8N is running
echo -e "${BLUE}🔍 Checking N8N status...${NC}"
N8N_STATUS=$(curl -s -o /dev/null -w "%{http_code}" http://localhost:5678)
if [ "$N8N_STATUS" -eq 200 ]; then
    echo -e "${GREEN}✅ N8N is accessible at http://localhost:5678${NC}"
else
    echo -e "${RED}❌ N8N is not accessible. Please start services first.${NC}"
    exit 1
fi

# Check workflow file exists
echo -e "${BLUE}🔍 Checking workflow file...${NC}"
if [ -f "workflows/personality-chat-workflow.json" ]; then
    echo -e "${GREEN}✅ Workflow file found${NC}"
    WORKFLOW_SIZE=$(wc -c < "workflows/personality-chat-workflow.json")
    echo -e "   📄 Size: $WORKFLOW_SIZE bytes"
else
    echo -e "${RED}❌ Workflow file not found${NC}"
    exit 1
fi

echo ""
echo -e "${YELLOW}📋 MANUAL IMPORT STEPS REQUIRED:${NC}"
echo -e "${YELLOW}=================================${NC}"
echo ""
echo -e "${BLUE}1. Open N8N in your browser:${NC}"
echo -e "   🌐 http://localhost:5678"
echo -e "   👤 Username: admin"
echo -e "   🔑 Password: admin123"
echo ""
echo -e "${BLUE}2. Import the workflow:${NC}"
echo -e "   📁 Go to 'Workflows' → 'Import from file'"
echo -e "   📂 Select: $(pwd)/workflows/personality-chat-workflow.json"
echo -e "   💾 Click 'Import'"
echo ""
echo -e "${BLUE}3. Configure PostgreSQL credentials:${NC}"
echo -e "   🔧 Go to 'Settings' → 'Credentials' → 'Add Credential'"
echo -e "   🗄️  Select 'PostgreSQL'"
echo -e "   📝 Enter these details:"
echo -e "      Host: postgres"
echo -e "      Database: n8n_personality_ai" 
echo -e "      User: n8n_user"
echo -e "      Password: n8n_password"
echo -e "      Port: 5432"
echo -e "   💾 Save as 'PostgreSQL-PersonalityAI'"
echo ""
echo -e "${BLUE}4. Update workflow nodes:${NC}"
echo -e "   🔧 Open the imported workflow"
echo -e "   📊 Click each 'Postgres' node"
echo -e "   🔗 Set credential to 'PostgreSQL-PersonalityAI'"
echo ""
echo -e "${BLUE}5. Activate the workflow:${NC}"
echo -e "   🟢 Toggle the 'Active' switch ON"
echo ""

# Wait for user confirmation
echo -e "${YELLOW}⏳ Press Enter when you have completed the import...${NC}"
read -r

# Test the webhook endpoint
echo -e "${BLUE}🧪 Testing webhook endpoint...${NC}"
WEBHOOK_RESPONSE=$(curl -s -w "HTTPSTATUS:%{http_code}" \
  -X POST http://localhost:5678/webhook/chat \
  -H "Content-Type: application/json" \
  -d '{
    "session_id": "test-import-123",
    "message": "Hello, I am feeling excited about this new AI system!"
  }')

HTTP_CODE=$(echo "$WEBHOOK_RESPONSE" | tr -d '\n' | sed -e 's/.*HTTPSTATUS://')
RESPONSE_BODY=$(echo "$WEBHOOK_RESPONSE" | sed -e 's/HTTPSTATUS:.*//')

echo -e "${BLUE}📡 Webhook Response:${NC}"
echo -e "   Status Code: $HTTP_CODE"

if [ "$HTTP_CODE" -eq 200 ]; then
    echo -e "${GREEN}✅ Webhook is working!${NC}"
    echo -e "${BLUE}📄 Response:${NC}"
    echo "$RESPONSE_BODY" | jq . 2>/dev/null || echo "$RESPONSE_BODY"
    
    echo ""
    echo -e "${GREEN}🎉 SUCCESS! Your N8N Personality AI MVP is ready!${NC}"
    echo -e "${GREEN}===============================================${NC}"
    echo ""
    echo -e "${BLUE}🔗 Access Points:${NC}"
    echo -e "   🌐 N8N Editor: http://localhost:5678"
    echo -e "   📡 Webhook API: http://localhost:5678/webhook/chat"
    echo -e "   🗄️  Database: localhost:5432 (n8n_personality_ai)"
    echo ""
    echo -e "${BLUE}📊 Test Commands:${NC}"
    echo -e "   # Test personality detection:"
    echo -e "   curl -X POST http://localhost:5678/webhook/chat \\"
    echo -e "     -H 'Content-Type: application/json' \\"
    echo -e "     -d '{\"session_id\":\"demo-123\",\"message\":\"I love trying new adventures and meeting people!\"}'"
    echo ""
    echo -e "   # Test different personality:"
    echo -e "   curl -X POST http://localhost:5678/webhook/chat \\"
    echo -e "     -H 'Content-Type: application/json' \\"
    echo -e "     -d '{\"session_id\":\"demo-456\",\"message\":\"I prefer quiet environments and careful planning.\"}'"
    
elif [ "$HTTP_CODE" -eq 404 ]; then
    echo -e "${YELLOW}⚠️  Webhook endpoint not found${NC}"
    echo -e "${BLUE}💡 This means the workflow might not be imported or activated yet.${NC}"
    echo -e "${BLUE}   Please complete the manual steps above.${NC}"
else
    echo -e "${RED}❌ Webhook test failed${NC}"
    echo -e "${BLUE}💡 Check the N8N workflow is imported and activated.${NC}"
    echo -e "${BLUE}   Response: $RESPONSE_BODY${NC}"
fi

echo ""
echo -e "${BLUE}📚 For detailed documentation, see README.md${NC}"
echo -e "${BLUE}🔧 For troubleshooting, check Docker logs: docker-compose logs n8n${NC}"



































































