#!/bin/bash

# Import Corrected N8N Workflow with HTTP Request Nodes
# This script guides you through importing the corrected workflow

echo "🔄 N8N Workflow Import - HTTP Request Node Version"
echo "================================================="
echo ""

echo "📋 SUMMARY OF FIXES:"
echo "   • Replaced Code nodes with HTTP Request nodes"
echo "   • Hardcoded API key in Authorization headers"
echo "   • Fixed JSON formatting issues"
echo "   • Uses standard N8N HTTP Request approach"
echo ""

echo "🌐 N8N Access:"
echo "   URL: http://localhost:5678"
echo "   Setup: Owner setup flow (first-time login)"
echo ""

echo "📁 STEP 1: Import Workflow"
echo "--------------------------"
echo "1. Open N8N: http://localhost:5678"
echo "2. Click 'Workflows' in left sidebar"
echo "3. Click '+ Add workflow' or import button"
echo "4. Select 'Import from File'"
echo "5. Upload: workflows/personality-chat-workflow-FIXED.json"
echo "6. Click 'Import'"
echo ""

echo "🗄️ STEP 2: Configure PostgreSQL Credentials"
echo "--------------------------------------------"
echo "1. Click 'Settings' → 'Credentials'"
echo "2. Click '+ Add credential'"
echo "3. Search for 'PostgreSQL' and select it"
echo "4. Enter these details:"
echo "   Name: PostgreSQL-PersonalityAI"
echo "   Host: postgres"
echo "   Database: n8n_personality_ai"
echo "   User: n8n_user"
echo "   Password: n8n_password"
echo "   Port: 5432"
echo "5. Click 'Test connection' (should succeed)"
echo "6. Click 'Save'"
echo ""

echo "🔗 STEP 3: Connect Database Nodes to Credentials"
echo "------------------------------------------------"
echo "In the workflow, you need to connect these 5 nodes to PostgreSQL credential:"
echo "   • Get Latest State"
echo "   • Get Conversation History"
echo "   • Save User Turn"
echo "   • Save Assistant Turn"
echo "   • Save State Snapshot"
echo ""
echo "For each node:"
echo "1. Click the node"
echo "2. In the 'Credential to connect with' dropdown"
echo "3. Select 'PostgreSQL-PersonalityAI'"
echo "4. Node should show green checkmark"
echo ""

echo "✅ STEP 4: Activate Workflow"
echo "----------------------------"
echo "1. Toggle the workflow 'Active' switch to ON"
echo "2. Workflow should show as 'Active' with green dot"
echo ""

echo "🧪 STEP 5: Test the Workflow"
echo "----------------------------"
echo "1. Click 'When clicking Test workflow' node"
echo "2. Click 'Execute workflow' button"
echo "3. Check each node for successful execution (green checkmarks)"
echo ""

echo "🌐 STEP 6: Test Webhook (Optional)"
echo "---------------------------------"
echo "Webhook URL: http://localhost:5678/webhook/chat"
echo ""
echo "Test with curl:"
echo "curl -X POST http://localhost:5678/webhook/chat \\"
echo "     -H 'Content-Type: application/json' \\"
echo "     -d '{\"session_id\": \"test-session-123\", \"message\": \"Hello!\"}'"
echo ""

echo "🎯 WHAT'S DIFFERENT IN THIS VERSION:"
echo "   ✅ Uses HTTP Request nodes (standard N8N approach)"
echo "   ✅ Hardcoded API key bypasses environment variable issues"
echo "   ✅ Proper JSON expressions for API body parameters"
echo "   ✅ No Code node dependencies or library requirements"
echo "   ✅ Compatible with N8N v1.111.0"
echo ""

echo "🚨 TROUBLESHOOTING:"
echo "   • If nodes show red: Check PostgreSQL credentials"
echo "   • If API fails: Verify Juguang API key is valid"
echo "   • If import fails: Check JSON syntax in workflow file"
echo "   • If webhook returns empty: Check workflow activation"
echo ""

echo "📞 Ready to test? Run: ./test_personality_chatbot.sh"
echo ""
















