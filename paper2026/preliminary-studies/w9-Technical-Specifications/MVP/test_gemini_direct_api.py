#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import requests
import time
import json
import os

def test_gemini_direct_api():
    """Test Gemini Pro API directly with timing"""
    # Direct Gemini API key
    api_key = "AIzaSyCu7cMyJAB4ossEePGYQQGpzjlqAfbIG2E"
    
    if not api_key:
        print("❌ No Gemini API key found")
        return False
    
    url = "https://generativelanguage.googleapis.com/v1beta/models/gemini-2.0-flash-exp:generateContent"
    headers = {
        "Content-Type": "application/json"
    }
    
    # Test prompt for personality detection
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
            "temperature": 0.3,
            "topK": 40,
            "topP": 0.95,
            "maxOutputTokens": 500,
            "candidateCount": 1
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
    
    print("🧪 Testing Direct Gemini Pro API for Personality AI MVP...")
    print(f"🔑 API Key: {api_key[:10]}...")
    print(f"🌐 URL: {url}")
    print(f"🤖 Model: gemini-2.0-flash-exp")
    print(f"📝 Prompt length: {len(prompt)} characters")
    print("-" * 60)
    
    # Test multiple times for reliability
    times = []
    success_count = 0
    
    for i in range(3):
        try:
            print(f"Test {i+1}/3: ", end="", flush=True)
            start_time = time.time()
            
            # Add API key to URL
            test_url = f"{url}?key={api_key}"
            response = requests.post(test_url, headers=headers, json=payload, timeout=30)
            end_time = time.time()
            
            duration = end_time - start_time
            times.append(duration)
            
            if response.status_code == 200:
                success_count += 1
                data = response.json()
                
                # Extract content from Gemini response format
                if "candidates" in data and len(data["candidates"]) > 0:
                    content = data["candidates"][0]["content"]["parts"][0]["text"]
                    
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
                    print(f"⚠️  {duration:.2f}s - Empty response from API")
                    
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
    
    return success_count > 0

def test_gemini_generation():
    """Test simple text generation with Gemini Pro API"""
    api_key = "AIzaSyCu7cMyJAB4ossEePGYQQGpzjlqAfbIG2E"
    url = "https://generativelanguage.googleapis.com/v1beta/models/gemini-2.0-flash-exp:generateContent"
    headers = {
        "Content-Type": "application/json"
    }
    
    payload = {
        "contents": [
            {
                "parts": [
                    {
                        "text": "Generate a helpful response following these behavioral directives: ['validate concerns warmly', 'use gentle language', 'ask one supportive question']. User said: 'I'm worried about my job interview tomorrow.' Stay grounded in this context only."
                    }
                ]
            }
        ],
        "generationConfig": {
            "temperature": 0.7,
            "maxOutputTokens": 150
        }
    }
    
    print(f"\n🧪 Testing Direct Gemini Response Generation...")
    
    try:
        test_url = f"{url}?key={api_key}"
        response = requests.post(test_url, headers=headers, json=payload, timeout=15)
        if response.status_code == 200:
            data = response.json()
            if "candidates" in data and len(data["candidates"]) > 0:
                content = data["candidates"][0]["content"]["parts"][0]["text"]
                print(f"✅ Generated response:")
                print(f"   📝 {content}")
                return True
        else:
            print(f"❌ Generation failed: {response.status_code}")
            print(f"   Error: {response.text}")
            return False
    except Exception as e:
        print(f"❌ Exception: {e}")
        return False

def test_juguang_fallback():
    """Test Juguang API as fallback"""
    api_key = "sk-nU7RSKnbZIOwH607r3MfbW5HmP6NIaj1aGVPFGcNDDiL0h5u"
    url = "https://ai.juguang.chat/v1/chat/completions"
    headers = {
        "Authorization": f"Bearer {api_key}",
        "Content-Type": "application/json"
    }
    
    payload = {
        "model": "gemini-1.5-flash",
        "messages": [{"role": "user", "content": "Say 'Juguang fallback is working'"}],
        "max_tokens": 50,
        "temperature": 0.3
    }
    
    print(f"\n🧪 Testing Juguang Fallback...")
    
    try:
        response = requests.post(url, headers=headers, json=payload, timeout=15)
        if response.status_code == 200:
            content = response.json()["choices"][0]["message"]["content"]
            print(f"✅ Fallback working: {content}")
            return True
        else:
            print(f"❌ Fallback failed: {response.status_code}")
            return False
    except Exception as e:
        print(f"❌ Fallback exception: {e}")
        return False

if __name__ == "__main__":
    print("🚀 Gemini Pro Direct API Test Suite for Personality AI MVP")
    print("=" * 60)
    
    # Test direct Gemini Pro API
    gemini_success = test_gemini_direct_api()
    gemini_gen_success = test_gemini_generation()
    
    # Test Juguang fallback
    juguang_success = test_juguang_fallback()
    
    print("\n" + "=" * 60)
    print(f"📊 Test Results:")
    print(f"   🟢 Gemini Direct API: {'✅ Working' if gemini_success else '❌ Failed'}")
    print(f"   🟢 Gemini Generation: {'✅ Working' if gemini_gen_success else '❌ Failed'}")
    print(f"   🟡 Juguang Fallback: {'✅ Working' if juguang_success else '❌ Failed'}")
    
    if gemini_success and gemini_gen_success:
        print("\n🎉 PRIMARY API (Gemini Direct) IS READY!")
        print("📋 Next steps:")
        print("   1. Add GEMINI_API_KEY to your .env file")
        print("   2. Update N8N workflow to use dual API system")
        print("   3. Start the MVP with: docker-compose up -d")
        print("   4. Test the chat interface at http://localhost:3000")
        
        if juguang_success:
            print("   💡 Juguang fallback is also available for redundancy")
        else:
            print("   ⚠️  Juguang fallback not working - only direct Gemini will work")
    elif juguang_success:
        print("\n⚠️  Only fallback API working - will use Juguang")
    else:
        print("\n❌ No APIs working - check keys and network connection")
