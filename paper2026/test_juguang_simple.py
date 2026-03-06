#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import requests
import json

def test_juguang_api_simple():
    """Simple test to check if API key is working"""
    api_key = "sk-GI12C0yPZGsxkTaKsV7pxHOpDKPSFslQ3yZjSFwO6Ms2cXls"
    
    url = "https://ai.juguang.chat/v1/chat/completions"
    headers = {
        "Authorization": f"Bearer {api_key}",
        "Content-Type": "application/json"
    }
    
    # Try different models
    models_to_test = [
        "gemini-1.5-flash",
        "gemini-1.5-pro", 
        "gemini-2.0-flash-exp",
        "gpt-3.5-turbo",
        "gpt-4"
    ]
    
    print("🔍 Testing Juguang API Key with Different Models...")
    print(f"🔑 API Key: {api_key[:10]}...")
    print(f"🌐 URL: {url}")
    print("-" * 60)
    
    for model in models_to_test:
        print(f"Testing model: {model}")
        
        payload = {
            "model": model,
            "messages": [{"role": "user", "content": "Hello, test message"}],
            "max_tokens": 50,
            "temperature": 0.3
        }
        
        try:
            response = requests.post(url, headers=headers, json=payload, timeout=10)
            print(f"  Status: {response.status_code}")
            
            if response.status_code == 200:
                data = response.json()
                content = data["choices"][0]["message"]["content"]
                print(f"  ✅ SUCCESS - Response: {content[:50]}...")
                return True, model
            else:
                error_data = response.json() if response.headers.get('content-type', '').startswith('application/json') else {}
                error_msg = error_data.get('error', {}).get('message', response.text[:100])
                print(f"  ❌ FAILED - {error_msg}")
                
        except Exception as e:
            print(f"  ❌ EXCEPTION - {e}")
    
    print("-" * 60)
    print("❌ No working models found")
    return False, None

def test_api_key_validity():
    """Test if API key is valid by checking authentication"""
    api_key = "sk-GI12C0yPZGsxkTaKsV7pxHOpDKPSFslQ3yZjSFwO6Ms2cXls"
    
    # Test with a simple request to see if we get auth errors
    url = "https://ai.juguang.chat/v1/chat/completions"
    headers = {
        "Authorization": f"Bearer {api_key}",
        "Content-Type": "application/json"
    }
    
    payload = {
        "model": "gpt-3.5-turbo",  # Try a common model
        "messages": [{"role": "user", "content": "test"}],
        "max_tokens": 10
    }
    
    print("🔐 Testing API Key Authentication...")
    
    try:
        response = requests.post(url, headers=headers, json=payload, timeout=10)
        
        if response.status_code == 401:
            print("❌ API Key is INVALID - Authentication failed")
            return False
        elif response.status_code == 403:
            print("❌ API Key is VALID but access is FORBIDDEN")
            return False
        elif response.status_code == 400:
            print("⚠️  API Key is VALID but request format is wrong")
            return True
        elif response.status_code == 503:
            print("⚠️  API Key is VALID but service/model unavailable")
            return True
        elif response.status_code == 200:
            print("✅ API Key is VALID and working!")
            return True
        else:
            print(f"⚠️  API Key status unclear - Status: {response.status_code}")
            return True
            
    except Exception as e:
        print(f"❌ Network error: {e}")
        return False

if __name__ == "__main__":
    print("🚀 Juguang API Key Validation Test")
    print("=" * 50)
    
    # Test API key validity
    key_valid = test_api_key_validity()
    
    if key_valid:
        print("\n" + "=" * 50)
        # Test with different models
        success, working_model = test_juguang_api_simple()
        
        if success:
            print(f"\n🎉 API KEY IS WORKING!")
            print(f"✅ Working model: {working_model}")
            print(f"💡 You can use this model in your N8N workflow")
        else:
            print(f"\n⚠️  API KEY IS VALID but no models are currently available")
            print(f"💡 This might be due to:")
            print(f"   - Geographic restrictions")
            print(f"   - Model availability issues")
            print(f"   - Account limitations")
    else:
        print(f"\n❌ API KEY IS NOT WORKING")
        print(f"💡 Check your API key or account status")







































