#!/usr/bin/env python3
"""
Validation script for Discrete_workflow_dual_api.json
Verifies that the dual API system has been properly implemented
"""
import json
import os

def validate_dual_api_workflow():
    """Validate that the dual API workflow has been properly configured"""
    
    workflow_path = "workflows/Discrete_workflow_dual_api.json"
    
    if not os.path.exists(workflow_path):
        print("❌ Workflow file not found:", workflow_path)
        return False
    
    print("🔍 Validating Dual API Workflow Configuration...")
    print("=" * 50)
    
    try:
        with open(workflow_path, 'r') as f:
            workflow = json.load(f)
        
        print("✅ JSON is valid and loadable")
        
        # Check workflow name
        workflow_name = workflow.get('name', '')
        if 'Dual API' in workflow_name:
            print("✅ Workflow name indicates dual API:", workflow_name)
        else:
            print("⚠️  Workflow name doesn't indicate dual API:", workflow_name)
        
        # Find the relevant nodes
        nodes = workflow.get('nodes', [])
        print(f"\n📊 Found {len(nodes)} nodes in workflow")
        
        detect_ocean_node = None
        generate_response_node = None
        
        for node in nodes:
            node_name = node.get('name', '')
            if 'Detect OCEAN' in node_name:
                detect_ocean_node = node
                print(f"✅ Found OCEAN detection node: '{node_name}'")
            elif 'Generate Response' in node_name:
                generate_response_node = node
                print(f"✅ Found response generation node: '{node_name}'")
        
        # Validate OCEAN detection node
        print(f"\n🧠 Validating OCEAN Detection Node...")
        if detect_ocean_node:
            js_code = detect_ocean_node.get('parameters', {}).get('jsCode', '')
            
            checks = [
                ('GEMINI_API_KEY', 'AIzaSyCu7cMyJAB4ossEePGYQQGpzjlqAfbIG2E' in js_code),
                ('JUGUANG_API_KEY', 'sk-nU7RSKnbZIOwH607r3MfbW5HmP6NIaj1aGVPFGcNDDiL0h5u' in js_code),
                ('callGeminiDirect function', 'async function callGeminiDirect()' in js_code),
                ('callJuguangFallback function', 'async function callJuguangFallback()' in js_code),
                ('Gemini API URL', 'generativelanguage.googleapis.com' in js_code),
                ('Juguang API URL', 'ai.juguang.chat' in js_code),
                ('Error handling', 'try {' in js_code and 'catch' in js_code),
                ('Console logging', 'console.log' in js_code),
                ('API usage tracking', 'api_used' in js_code)
            ]
            
            for check_name, passed in checks:
                status = "✅" if passed else "❌"
                print(f"   {status} {check_name}")
        else:
            print("❌ OCEAN detection node not found")
        
        # Validate Response Generation node
        print(f"\n💬 Validating Response Generation Node...")
        if generate_response_node:
            js_code = generate_response_node.get('parameters', {}).get('jsCode', '')
            
            checks = [
                ('GEMINI_API_KEY', 'AIzaSyCu7cMyJAB4ossEePGYQQGpzjlqAfbIG2E' in js_code),
                ('JUGUANG_API_KEY', 'sk-nU7RSKnbZIOwH607r3MfbW5HmP6NIaj1aGVPFGcNDDiL0h5u' in js_code),
                ('callGeminiDirect function', 'async function callGeminiDirect()' in js_code),
                ('callJuguangFallback function', 'async function callJuguangFallback()' in js_code),
                ('Session data preservation', 'session_id' in js_code and 'turn_text' in js_code),
                ('Directive handling', 'directives' in js_code),
                ('Error handling', 'try {' in js_code and 'catch' in js_code),
                ('Console logging', 'console.log' in js_code),
                ('Fallback message', 'temporarily unavailable' in js_code)
            ]
            
            for check_name, passed in checks:
                status = "✅" if passed else "❌"
                print(f"   {status} {check_name}")
        else:
            print("❌ Response generation node not found")
        
        # Overall validation
        print(f"\n📋 Overall Validation Summary:")
        
        has_dual_api_detection = (detect_ocean_node and 
                                'callGeminiDirect' in detect_ocean_node.get('parameters', {}).get('jsCode', ''))
        has_dual_api_generation = (generate_response_node and 
                                 'callGeminiDirect' in generate_response_node.get('parameters', {}).get('jsCode', ''))
        
        print(f"   {'✅' if has_dual_api_detection else '❌'} OCEAN Detection has dual API")
        print(f"   {'✅' if has_dual_api_generation else '❌'} Response Generation has dual API")
        print(f"   {'✅' if workflow_name else '❌'} Workflow has descriptive name")
        
        overall_success = has_dual_api_detection and has_dual_api_generation and workflow_name
        
        print(f"\n{'🎉' if overall_success else '❌'} Overall Status: {'PASSED' if overall_success else 'FAILED'}")
        
        if overall_success:
            print("\n✅ Workflow is ready for N8N import and testing!")
            print("📋 Next steps:")
            print("   1. Import Discrete_workflow_dual_api.json into N8N")
            print("   2. Test the workflow to verify dual API behavior")
            print("   3. Monitor console logs to see which APIs are used")
            print("   4. Replace your production workflow when satisfied")
        
        return overall_success
        
    except json.JSONDecodeError as e:
        print(f"❌ JSON parsing error: {e}")
        return False
    except Exception as e:
        print(f"❌ Validation error: {e}")
        return False

if __name__ == "__main__":
    print("🚀 N8N Dual API Workflow Validator")
    print("=" * 40)
    
    success = validate_dual_api_workflow()
    
    if success:
        exit(0)
    else:
        exit(1)



















































