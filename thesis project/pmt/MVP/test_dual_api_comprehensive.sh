#!/bin/bash
# Comprehensive Dual API System Test for Personality AI MVP
# Tests both Gemini Direct and Juguang Fallback APIs with full integration

echo "🚀 PERSONALITY AI MVP - DUAL API COMPREHENSIVE TEST SUITE"
echo "=========================================================="

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
PURPLE='\033[0;35m'
NC='\033[0m' # No Color

# Test configuration
TEST_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
LOG_FILE="$TEST_DIR/dual_api_test_results.log"

# Initialize log file
echo "Dual API Test Suite - $(date)" > "$LOG_FILE"
echo "=================================" >> "$LOG_FILE"

# Function to log and display
log_and_echo() {
    echo -e "$1"
    echo -e "$1" | sed 's/\x1b\[[0-9;]*m//g' >> "$LOG_FILE"
}

# Function to check if command exists
command_exists() {
    command -v "$1" >/dev/null 2>&1
}

log_and_echo "${BLUE}🔍 Environment Check${NC}"
echo "-------------------"

# Check Python
if command_exists python3; then
    PYTHON_VERSION=$(python3 --version)
    log_and_echo "${GREEN}✅ Python3: $PYTHON_VERSION${NC}"
else
    log_and_echo "${RED}❌ Python3 not found${NC}"
    exit 1
fi

# Check pip and required packages
log_and_echo "${BLUE}📦 Checking Python packages...${NC}"
if python3 -c "import requests" 2>/dev/null; then
    log_and_echo "${GREEN}✅ requests package available${NC}"
else
    log_and_echo "${YELLOW}⚠️  Installing requests package...${NC}"
    pip3 install requests || {
        log_and_echo "${RED}❌ Failed to install requests${NC}"
        exit 1
    }
fi

# Test API Connectivity
log_and_echo "\n${PURPLE}🌐 API Connectivity Tests${NC}"
echo "=========================="

# Test Gemini Direct API
log_and_echo "${BLUE}Testing Gemini Pro Direct API...${NC}"
python3 -c "
import requests
try:
    response = requests.get('https://generativelanguage.googleapis.com', timeout=5)
    print('✅ Gemini API endpoint reachable')
except:
    print('❌ Gemini API endpoint not reachable')
"

# Test Juguang Fallback API
log_and_echo "${BLUE}Testing Juguang Fallback API...${NC}"
python3 -c "
import requests
try:
    response = requests.get('https://ai.juguang.chat', timeout=5)
    print('✅ Juguang API endpoint reachable')
except:
    print('❌ Juguang API endpoint not reachable')
"

# Run comprehensive API tests
log_and_echo "\n${PURPLE}🧪 Dual API System Tests${NC}"
echo "========================"

if [ -f "$TEST_DIR/test_dual_api_system.py" ]; then
    log_and_echo "${BLUE}Running comprehensive dual API tests...${NC}"
    
    # Make script executable
    chmod +x "$TEST_DIR/test_dual_api_system.py"
    
    # Run the comprehensive test
    python3 "$TEST_DIR/test_dual_api_system.py" 2>&1 | tee -a "$LOG_FILE"
    DUAL_API_EXIT_CODE=${PIPESTATUS[0]}
    
    case $DUAL_API_EXIT_CODE in
        0)
            log_and_echo "\n${GREEN}🎉 ALL DUAL API TESTS PASSED${NC}"
            log_and_echo "${GREEN}✅ Both Gemini Direct and Juguang Fallback are working${NC}"
            ;;
        1)
            log_and_echo "\n${YELLOW}⚠️  PARTIAL API FUNCTIONALITY${NC}"
            log_and_echo "${YELLOW}Some APIs are working but not all${NC}"
            ;;
        2)
            log_and_echo "\n${RED}❌ ALL APIS FAILED${NC}"
            log_and_echo "${RED}Neither Gemini nor Juguang APIs are working${NC}"
            ;;
        *)
            log_and_echo "\n${RED}❌ UNKNOWN ERROR${NC}"
            ;;
    esac
else
    log_and_echo "${RED}❌ test_dual_api_system.py not found${NC}"
    exit 1
fi

# Test individual API files if they exist
log_and_echo "\n${PURPLE}🔧 Individual API Tests${NC}"
echo "======================"

# Test Gemini Direct API
if [ -f "$TEST_DIR/test_gemini_direct_api.py" ]; then
    log_and_echo "${BLUE}Testing Gemini Direct API individually...${NC}"
    chmod +x "$TEST_DIR/test_gemini_direct_api.py"
    python3 "$TEST_DIR/test_gemini_direct_api.py" 2>&1 | tee -a "$LOG_FILE"
else
    log_and_echo "${YELLOW}⚠️  test_gemini_direct_api.py not found${NC}"
fi

# Test Juguang API
if [ -f "$TEST_DIR/test_juguang_clean.py" ]; then
    log_and_echo "${BLUE}Testing Juguang API individually...${NC}"
    python3 "$TEST_DIR/test_juguang_clean.py" 2>&1 | tee -a "$LOG_FILE"
else
    log_and_echo "${YELLOW}⚠️  test_juguang_clean.py not found${NC}"
fi

# Check N8N workflow files
log_and_echo "\n${PURPLE}📄 N8N Workflow File Check${NC}"
echo "=========================="

WORKFLOW_FILES=(
    "generate_response_code_dual_api.js"
    "refine_response_code_dual_api.js"
    "generate_response_code.js"
    "refine_response_code.js"
)

for file in "${WORKFLOW_FILES[@]}"; do
    if [ -f "$TEST_DIR/$file" ]; then
        log_and_echo "${GREEN}✅ $file${NC}"
    else
        log_and_echo "${YELLOW}⚠️  $file not found${NC}"
    fi
done

# Environment file check
log_and_echo "\n${PURPLE}⚙️  Environment Configuration${NC}"
echo "============================="

if [ -f "$TEST_DIR/.env" ]; then
    log_and_echo "${GREEN}✅ .env file exists${NC}"
    
    # Check for required keys (without showing values)
    if grep -q "GEMINI_API_KEY" "$TEST_DIR/.env"; then
        log_and_echo "${GREEN}✅ GEMINI_API_KEY configured${NC}"
    else
        log_and_echo "${RED}❌ GEMINI_API_KEY not found in .env${NC}"
    fi
    
    if grep -q "JUGUANG_API_KEY" "$TEST_DIR/.env"; then
        log_and_echo "${GREEN}✅ JUGUANG_API_KEY configured${NC}"
    else
        log_and_echo "${RED}❌ JUGUANG_API_KEY not found in .env${NC}"
    fi
else
    log_and_echo "${YELLOW}⚠️  .env file not found${NC}"
    if [ -f "$TEST_DIR/env.example" ]; then
        log_and_echo "${BLUE}📋 env.example available as template${NC}"
    fi
fi

# Final summary
log_and_echo "\n${PURPLE}📊 FINAL TEST SUMMARY${NC}"
echo "====================="

# Determine overall status
if [ $DUAL_API_EXIT_CODE -eq 0 ]; then
    log_and_echo "${GREEN}🎉 DUAL API SYSTEM: FULLY OPERATIONAL${NC}"
    log_and_echo "${GREEN}✅ Primary API (Gemini Direct): Working${NC}"
    log_and_echo "${GREEN}✅ Fallback API (Juguang): Working${NC}"
    log_and_echo "${GREEN}✅ Redundancy: Available${NC}"
    
    log_and_echo "\n${BLUE}📋 Next Steps:${NC}"
    log_and_echo "   1. Update your N8N workflow with dual API JavaScript files"
    log_and_echo "   2. Use: generate_response_code_dual_api.js"
    log_and_echo "   3. Use: refine_response_code_dual_api.js"
    log_and_echo "   4. Start MVP: docker-compose up -d"
    log_and_echo "   5. Test at: http://localhost:3000"
    
elif [ $DUAL_API_EXIT_CODE -eq 1 ]; then
    log_and_echo "${YELLOW}⚠️  DUAL API SYSTEM: PARTIAL FUNCTIONALITY${NC}"
    log_and_echo "${YELLOW}Some APIs working, check individual test results above${NC}"
    
    log_and_echo "\n${BLUE}📋 Recommended Actions:${NC}"
    log_and_echo "   1. Check API keys and quotas"
    log_and_echo "   2. Verify network connectivity"
    log_and_echo "   3. Use working API until issues resolved"
    
else
    log_and_echo "${RED}❌ DUAL API SYSTEM: NOT OPERATIONAL${NC}"
    log_and_echo "${RED}Neither primary nor fallback APIs working${NC}"
    
    log_and_echo "\n${BLUE}📋 Troubleshooting Steps:${NC}"
    log_and_echo "   1. Verify API keys are correct"
    log_and_echo "   2. Check quota limits"
    log_and_echo "   3. Test network connectivity"
    log_and_echo "   4. Review error logs above"
fi

log_and_echo "\n${BLUE}📄 Full test results saved to: $LOG_FILE${NC}"
log_and_echo "${BLUE}🕐 Test completed at: $(date)${NC}"

exit $DUAL_API_EXIT_CODE



















































