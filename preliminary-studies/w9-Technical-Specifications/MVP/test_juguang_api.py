#!/usr/bin/env python3
import requests
import time
import json
import os

def test_juguang_api_performance():
    """Test Juguang API performance with timing"""
    # Use hardcoded key from test_juguang_api.py
    api_key = "sk-GI12C0yPZGsxkTaKsV7pxHOpDKPSFslQ3yZjSFwO6Ms2cXls"
    
    if not api_key:
        print("❌ No API key found")
        return
    
    url = "https://ai.juguang.chat/v1/chat/completions"
    headers = {
        "Authorization": f"Bearer {api_key}",
        "Content-Type": "application/json"
    }
    
    # Test prompt for personality detection (similar to N8N workflow)
    prompt = """Analyze this conversation to infer OCEAN personality traits. Return JSON only with this exact format:
    {
      "ocean": {"O": float, "C": float, "E": float, "A": float, "N": float},
      "trait_conf": {"O": float, "C": float, "E": float, "A": float, "N": float},
      "evidence_quotes": [string, string, ...]
    }
    
    Values in [-1,1], confidence in [0,1]. Base analysis on conversation patterns, word choice, and communication style. No prose commentary.
    
    Sample conversation:
    user: "Hello, I'm feeling a bit anxious about my upcoming presentation."
    assistant: "I understand that presentations can feel overwhelming. What specific aspects are making you feel most anxious?"
    user: "I worry about forgetting what to say and stumbling over my words."
    """
    
    payload = {
        "model": "gemini-1.5-flash",
        "messages": [{"role": "user", "content": prompt}],
        "max_tokens": 500,
        "temperature": 0.3
    }
    
    print("🧪 Testing Juguang API for Personality AI MVP...")
    print(f"🔑 API Key: {api_key[:10]}...")
    print(f"🌐 URL: {url}")
    print(f"🤖 Model: gemini-1.5-flash")
    print(f"📝 Prompt length: {len(prompt)} characters")
    print("-" * 60)
    
    # Test multiple times for reliability
    times = []
    success_count = 0
    
    for i in range(3):
        try:
            print(f"Test {i+1}/3: ", end="", flush=True)
            start_time = time.time()
            response = requests.post(url, headers=headers, json=payload, timeout=30)
            end_time = time.time()
            
            duration = end_time - start_time
            times.append(duration)
            
            if response.status_code == 200:
                success_count += 1
                data = response.json()
                content = data["choices"][0]["message"]["content"]
                
                # Try to parse JSON response
                try:
                    personality_data = json.loads(content)
                    ocean_traits = personality_data.get("ocean", {})
                    confidence_scores = personality_data.get("trait_conf", {})
                    
                    print(f"✅ {duration:.2f}s - Status: {response.status_code}")
                    print(f"     🧠 OCEAN Traits: O={ocean_traits.get('O', 'N/A'):.2f}, C={ocean_traits.get('C', 'N/A'):.2f}, E={ocean_traits.get('E', 'N/A'):.2f}, A={ocean_traits.get('A', 'N/A'):.2f}, N={ocean_traits.get('N', 'N/A'):.2f}")
                    print(f"     📊 Avg Confidence: {sum(confidence_scores.values())/len(confidence_scores.values()) if confidence_scores else 0:.2f}")
                    
                except json.JSONDecodeError:
                    print(f"⚠️  {duration:.2f}s - Valid response but non-JSON content")
                    print(f"     📝 Content preview: {content[:100]}...")
                    
            else:
                print(f"❌ {duration:.2f}s - Status: {response.status_code}")
                print(f"     Error: {response.text[:100]}...")
                
        except Exception as e:
            print(f"❌ Exception - {e}")
            times.append(30)  # timeout value
    
    print("-" * 60)
    print(f"📊 Performance Results:")
    print(f"   ✅ Success rate: {success_count}/3 ({success_count*33:.0f}%)")
    print(f"   ⏱️  Average time: {sum(times)/len(times):.2f}s")
    print(f"   🚀 Min time: {min(times):.2f}s")
    print(f"   🐌 Max time: {max(times):.2f}s")
    
    if success_count > 0:
        print(f"\n🎉 Juguang API is working correctly!")
        print(f"💡 Ready to use in N8N workflow")
        print(f"🔗 Add this key to your .env file:")
        print(f"   JUGUANG_API_KEY={api_key}")
    else:
        print(f"\n❌ API is not working - check key and network")
        
    return success_count > 0

def test_simple_generation():
    """Test simple text generation"""
    api_key = "sk-GI12C0yPZGsxkTaKsV7pxHOpDKPSFslQ3yZjSFwO6Ms2cXls"
    url = "https://ai.juguang.chat/v1/chat/completions"
    headers = {
        "Authorization": f"Bearer {api_key}",
        "Content-Type": "application/json"
    }
    
    payload = {
        "model": "gemini-1.5-flash",
        "messages": [
            {
                "role": "user", 
                "content": "Generate a helpful response following these behavioral directives: ['validate concerns warmly', 'use gentle language', 'ask one supportive question']. User said: 'I'm worried about my job interview tomorrow.' Stay grounded in this context only."
            }
        ],
        "max_tokens": 150,
        "temperature": 0.7
    }
    
    print(f"\n🧪 Testing Response Generation...")
    
    try:
        response = requests.post(url, headers=headers, json=payload, timeout=15)
        if response.status_code == 200:
            content = response.json()["choices"][0]["message"]["content"]
            print(f"✅ Generated response:")
            print(f"   📝 {content}")
            return True
        else:
            print(f"❌ Generation failed: {response.status_code}")
            return False
    except Exception as e:
        print(f"❌ Exception: {e}")
        return False

if __name__ == "__main__":
    print("🚀 Juguang Gemini API Test Suite for Personality AI MVP")
    print("=" * 60)
    
    # Test personality detection
    detection_success = test_juguang_api_performance()
    
    # Test response generation
    generation_success = test_simple_generation()
    
    print("\n" + "=" * 60)
    if detection_success and generation_success:
        print("🎉 ALL TESTS PASSED - Ready for N8N integration!")
        print("📋 Next steps:")
        print("   1. Add JUGUANG_API_KEY to your .env file")
        print("   2. Start the MVP with: docker-compose up -d")
        print("   3. Import the N8N workflow")
        print("   4. Test the chat interface at http://localhost:3000")
    else:
        print("❌ Some tests failed - check API key and network connection")
