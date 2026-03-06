#!/usr/bin/env python3
"""
Check available Gemini models to find the correct endpoint
"""
import requests
import json

def check_available_models():
    """Check what models are available"""
    
    api_key = "AIzaSyCu7cMyJAB4ossEePGYQQGpzjlqAfbIG2E"
    url = f"https://generativelanguage.googleapis.com/v1beta/models?key={api_key}"
    
    print("🔍 Checking Available Gemini Models...")
    print("=" * 50)
    
    try:
        response = requests.get(url, timeout=10)
        
        if response.status_code == 200:
            data = response.json()
            models = data.get('models', [])
            
            gemini_models = [model for model in models if 'gemini' in model.get('name', '').lower()]
            
            print(f"📊 Found {len(gemini_models)} Gemini models:")
            print("-" * 50)
            
            for model in gemini_models:
                name = model.get('name', '')
                display_name = model.get('displayName', '')
                supported_methods = model.get('supportedGenerationMethods', [])
                
                print(f"🤖 {name}")
                print(f"   Display Name: {display_name}")
                print(f"   Methods: {', '.join(supported_methods)}")
                print()
                
                # Check if this model supports generateContent
                if 'generateContent' in supported_methods:
                    print(f"   ✅ Supports generateContent - CAN BE USED!")
                else:
                    print(f"   ❌ Does not support generateContent")
                print("-" * 30)
            
            # Find the best model to use
            content_models = [m for m in gemini_models if 'generateContent' in m.get('supportedGenerationMethods', [])]
            
            if content_models:
                best_model = content_models[0]  # Take the first available one
                model_name = best_model['name']
                
                print(f"🎯 RECOMMENDED MODEL TO USE:")
                print(f"   Name: {model_name}")
                print(f"   Display: {best_model.get('displayName', '')}")
                print(f"   URL: https://generativelanguage.googleapis.com/v1beta/{model_name}:generateContent")
                
                # Test this model
                test_model(model_name, api_key)
                
            else:
                print("❌ No models found that support generateContent")
                
        else:
            print(f"❌ Failed to get models: {response.status_code}")
            print(response.text)
            
    except Exception as e:
        print(f"❌ Error: {e}")

def test_model(model_name, api_key):
    """Test a specific model"""
    
    url = f"https://generativelanguage.googleapis.com/v1beta/{model_name}:generateContent?key={api_key}"
    
    headers = {
        "Content-Type": "application/json"
    }
    
    payload = {
        "contents": [{"parts": [{"text": "Say 'Hello, this model is working!'"}]}],
        "generationConfig": {
            "temperature": 0.1,
            "maxOutputTokens": 50
        }
    }
    
    print(f"\n🧪 Testing {model_name}...")
    print("-" * 30)
    
    try:
        response = requests.post(url, headers=headers, json=payload, timeout=15)
        
        if response.status_code == 200:
            data = response.json()
            if "candidates" in data and len(data["candidates"]) > 0:
                content = data["candidates"][0]["content"]["parts"][0]["text"]
                print(f"✅ {model_name} is working!")
                print(f"📝 Response: {content}")
                return True
            else:
                print(f"⚠️  {model_name} responded but no candidates")
                return False
        else:
            print(f"❌ {model_name} failed: {response.status_code}")
            print(f"   Error: {response.text}")
            return False
            
    except Exception as e:
        print(f"❌ {model_name} exception: {e}")
        return False

if __name__ == "__main__":
    check_available_models()



















































