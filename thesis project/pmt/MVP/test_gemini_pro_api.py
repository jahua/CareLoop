#!/usr/bin/env python3
"""
Test script for Gemini Pro API with the corrected endpoint
Based on the user's feedback about API issues
"""
import requests
import json
import time

def test_gemini_pro_api():
    """Test the stable Gemini Pro API endpoint"""
    
    api_key = "AIzaSyCu7cMyJAB4ossEePGYQQGpzjlqAfbIG2E"
    
    # Use the stable gemini-pro endpoint as suggested
    url = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-pro:generateContent?key={api_key}"
    
    headers = {
        "Content-Type": "application/json"
    }
    
    # Test prompt for personality detection
    prompt = """Analyze this conversation to infer OCEAN personality traits. Return JSON ONLY with this exact format:
    {
      "ocean_disc": {"O": -1, "C": 0, "E": 1, "A": 1, "N": -1}
    }
    
    Values should be -1, 0, or 1. Base analysis on conversation patterns.
    
    Sample conversation:
    user: "Hello, I'm feeling a bit anxious about my upcoming presentation."
    """
    
    # Proper request structure as suggested
    payload = {
        "contents": [
            {
                "parts": [
                    {
                        "text": prompt
                    }
                ]
            }
        ],
        "generationConfig": {
            "temperature": 0.1,
            "topK": 40,
            "topP": 0.95,
            "maxOutputTokens": 200
        },
        "safetySettings": [
            {
                "category": "HARM_CATEGORY_HARASSMENT",
                "threshold": "BLOCK_MEDIUM_AND_ABOVE"
            },
            {
                "category": "HARM_CATEGORY_HATE_SPEECH",
                "threshold": "BLOCK_MEDIUM_AND_ABOVE"
            },
            {
                "category": "HARM_CATEGORY_SEXUALLY_EXPLICIT",
                "threshold": "BLOCK_MEDIUM_AND_ABOVE"
            },
            {
                "category": "HARM_CATEGORY_DANGEROUS_CONTENT",
                "threshold": "BLOCK_MEDIUM_AND_ABOVE"
            }
        ]
    }
    
    print("🧪 Testing Gemini Pro API (Stable Endpoint)")
    print("=" * 50)
    print(f"🔑 API Key: {api_key[:10]}...")
    print(f"🌐 URL: {url}")
    print(f"🤖 Model: gemini-pro")
    print(f"📝 Prompt length: {len(prompt)} characters")
    print("-" * 50)
    
    try:
        print("🚀 Making API request...")
        start_time = time.time()
        
        response = requests.post(url, headers=headers, json=payload, timeout=30)
        
        end_time = time.time()
        duration = end_time - start_time
        
        print(f"⏱️  Response time: {duration:.2f}s")
        print(f"📊 Status code: {response.status_code}")
        
        if response.status_code == 200:
            data = response.json()
            print("✅ API call successful!")
            print("-" * 30)
            print("📄 Full Response:")
            print(json.dumps(data, indent=2))
            print("-" * 30)
            
            # Extract content as the workflow would
            if "candidates" in data and len(data["candidates"]) > 0:
                content = data["candidates"][0]["content"]["parts"][0]["text"]
                print("📝 Extracted content:")
                print(content)
                
                # Try to parse as JSON
                try:
                    personality_data = json.loads(content)
                    print("\n✅ JSON parsing successful!")
                    print("🧠 Personality data:", personality_data)
                    
                    if "ocean_disc" in personality_data:
                        ocean = personality_data["ocean_disc"]
                        print(f"🎯 OCEAN traits: O={ocean.get('O')}, C={ocean.get('C')}, E={ocean.get('E')}, A={ocean.get('A')}, N={ocean.get('N')}")
                        return True
                    else:
                        print("⚠️  ocean_disc not found in response")
                        
                except json.JSONDecodeError as e:
                    print(f"❌ JSON parsing failed: {e}")
                    print("🔍 Raw content:", repr(content))
                    
            else:
                print("❌ No candidates in response")
                return False
                
        else:
            print(f"❌ API call failed with status {response.status_code}")
            print("📄 Error response:")
            print(response.text)
            return False
            
    except Exception as e:
        print(f"❌ Exception occurred: {e}")
        return False

def test_simple_generation():
    """Test simple response generation"""
    
    api_key = "AIzaSyCu7cMyJAB4ossEePGYQQGpzjlqAfbIG2E"
    url = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-pro:generateContent?key={api_key}"
    
    headers = {
        "Content-Type": "application/json"
    }
    
    prompt = """You are a supportive assistant. Follow these behavior directives strictly: ["offer extra comfort; acknowledge anxieties", "use warm, collaborative language"]. Constraints: stay grounded in the user text only; 1-2 questions max; 70-150 words.

User: Give me a supportive tip for my presentation anxiety."""
    
    payload = {
        "contents": [{"parts": [{"text": prompt}]}],
        "generationConfig": {
            "temperature": 0.7,
            "maxOutputTokens": 220,
            "topK": 40,
            "topP": 0.95
        }
    }
    
    print("\n🧪 Testing Response Generation...")
    print("=" * 50)
    
    try:
        response = requests.post(url, headers=headers, json=payload, timeout=30)
        
        if response.status_code == 200:
            data = response.json()
            if "candidates" in data and len(data["candidates"]) > 0:
                content = data["candidates"][0]["content"]["parts"][0]["text"]
                print("✅ Response generation successful!")
                print(f"📝 Generated response: {content}")
                return True
            else:
                print("❌ No candidates in response")
                return False
        else:
            print(f"❌ Generation failed: {response.status_code}")
            print(response.text)
            return False
            
    except Exception as e:
        print(f"❌ Exception: {e}")
        return False

if __name__ == "__main__":
    print("🚀 Gemini Pro API Test Suite - CORRECTED VERSION")
    print("=" * 60)
    print("📋 Testing fixes suggested by user:")
    print("   1. ✅ Using stable gemini-pro endpoint")
    print("   2. ✅ Properly structured JSON body")
    print("   3. ✅ Correct response parsing")
    print("")
    
    # Test personality detection
    personality_success = test_gemini_pro_api()
    
    # Test response generation
    generation_success = test_simple_generation()
    
    print("\n" + "=" * 60)
    print("📊 TEST RESULTS:")
    print(f"   🧠 Personality Detection: {'✅ PASS' if personality_success else '❌ FAIL'}")
    print(f"   💬 Response Generation: {'✅ PASS' if generation_success else '❌ FAIL'}")
    
    if personality_success and generation_success:
        print("\n🎉 ALL TESTS PASSED!")
        print("✅ Gemini Pro API is working correctly with the fixed implementation")
        print("📋 Ready for N8N workflow integration")
    else:
        print("\n❌ Some tests failed - check API key and implementation")
        
    exit(0 if (personality_success and generation_success) else 1)



















































