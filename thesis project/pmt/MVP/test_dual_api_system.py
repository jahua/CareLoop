#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Comprehensive test suite for dual API system (Gemini Direct + Juguang Fallback)
Tests both personality detection and response generation workflows
"""
import requests
import time
import json
import os

class DualAPITester:
    def __init__(self):
        self.gemini_api_key = "AIzaSyCu7cMyJAB4ossEePGYQQGpzjlqAfbIG2E"
        self.juguang_api_key = "sk-nU7RSKnbZIOwH607r3MfbW5HmP6NIaj1aGVPFGcNDDiL0h5u"
        self.test_results = {}
        
    def call_gemini_direct(self, prompt, temperature=0.7, max_tokens=500):
        """Call Gemini Pro API directly"""
        url = "https://generativelanguage.googleapis.com/v1beta/models/gemini-2.0-flash-exp:generateContent"
        headers = {"Content-Type": "application/json"}
        
        payload = {
            "contents": [{"parts": [{"text": prompt}]}],
            "generationConfig": {
                "temperature": temperature,
                "maxOutputTokens": max_tokens,
                "topK": 40,
                "topP": 0.95
            },
            "safetySettings": [
                {"category": "HARM_CATEGORY_HARASSMENT", "threshold": "BLOCK_MEDIUM_AND_ABOVE"},
                {"category": "HARM_CATEGORY_HATE_SPEECH", "threshold": "BLOCK_MEDIUM_AND_ABOVE"},
                {"category": "HARM_CATEGORY_SEXUALLY_EXPLICIT", "threshold": "BLOCK_MEDIUM_AND_ABOVE"},
                {"category": "HARM_CATEGORY_DANGEROUS_CONTENT", "threshold": "BLOCK_MEDIUM_AND_ABOVE"}
            ]
        }
        
        test_url = f"{url}?key={self.gemini_api_key}"
        response = requests.post(test_url, headers=headers, json=payload, timeout=30)
        
        if response.status_code == 200:
            data = response.json()
            if "candidates" in data and len(data["candidates"]) > 0:
                content = data["candidates"][0]["content"]["parts"][0]["text"]
                return content, "gemini_direct", response.status_code
        
        raise Exception(f"Gemini API failed: {response.status_code} - {response.text}")
    
    def call_juguang_fallback(self, prompt, temperature=0.7, max_tokens=500):
        """Call Juguang API as fallback"""
        url = "https://ai.juguang.chat/v1/chat/completions"
        headers = {
            "Authorization": f"Bearer {self.juguang_api_key}",
            "Content-Type": "application/json"
        }
        
        payload = {
            "model": "gemini-1.5-flash",
            "messages": [{"role": "user", "content": prompt}],
            "temperature": temperature,
            "max_tokens": max_tokens
        }
        
        response = requests.post(url, headers=headers, json=payload, timeout=30)
        
        if response.status_code == 200:
            content = response.json()["choices"][0]["message"]["content"]
            return content, "juguang_fallback", response.status_code
            
        raise Exception(f"Juguang API failed: {response.status_code} - {response.text}")
    
    def dual_api_call(self, prompt, temperature=0.7, max_tokens=500):
        """Try Gemini first, fallback to Juguang if needed"""
        try:
            return self.call_gemini_direct(prompt, temperature, max_tokens)
        except Exception as gemini_error:
            print(f"   ⚠️ Gemini failed: {gemini_error}")
            try:
                return self.call_juguang_fallback(prompt, temperature, max_tokens)
            except Exception as juguang_error:
                raise Exception(f"Both APIs failed - Gemini: {gemini_error}, Juguang: {juguang_error}")
    
    def test_personality_detection(self):
        """Test personality detection with both APIs"""
        print("\n🧠 Testing Personality Detection...")
        
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
        
        results = {
            "gemini_direct": {"success": False, "time": 0, "error": None},
            "juguang_fallback": {"success": False, "time": 0, "error": None},
            "dual_system": {"success": False, "time": 0, "api_used": None, "error": None}
        }
        
        # Test Gemini Direct
        try:
            start_time = time.time()
            content, api_used, status = self.call_gemini_direct(prompt, 0.3, 500)
            results["gemini_direct"]["time"] = time.time() - start_time
            results["gemini_direct"]["success"] = True
            
            # Try to parse JSON
            personality_data = json.loads(content)
            ocean_traits = personality_data.get("ocean", {})
            print(f"   ✅ Gemini Direct: {results['gemini_direct']['time']:.2f}s")
            print(f"      🧠 OCEAN: O={ocean_traits.get('O', 'N/A'):.2f}, C={ocean_traits.get('C', 'N/A'):.2f}, E={ocean_traits.get('E', 'N/A'):.2f}, A={ocean_traits.get('A', 'N/A'):.2f}, N={ocean_traits.get('N', 'N/A'):.2f}")
            
        except Exception as e:
            results["gemini_direct"]["error"] = str(e)
            print(f"   ❌ Gemini Direct failed: {e}")
        
        # Test Juguang Fallback
        try:
            start_time = time.time()
            content, api_used, status = self.call_juguang_fallback(prompt, 0.3, 500)
            results["juguang_fallback"]["time"] = time.time() - start_time
            results["juguang_fallback"]["success"] = True
            
            # Try to parse JSON
            personality_data = json.loads(content)
            ocean_traits = personality_data.get("ocean", {})
            print(f"   ✅ Juguang Fallback: {results['juguang_fallback']['time']:.2f}s")
            print(f"      🧠 OCEAN: O={ocean_traits.get('O', 'N/A'):.2f}, C={ocean_traits.get('C', 'N/A'):.2f}, E={ocean_traits.get('E', 'N/A'):.2f}, A={ocean_traits.get('A', 'N/A'):.2f}, N={ocean_traits.get('N', 'N/A'):.2f}")
            
        except Exception as e:
            results["juguang_fallback"]["error"] = str(e)
            print(f"   ❌ Juguang Fallback failed: {e}")
        
        # Test Dual System
        try:
            start_time = time.time()
            content, api_used, status = self.dual_api_call(prompt, 0.3, 500)
            results["dual_system"]["time"] = time.time() - start_time
            results["dual_system"]["success"] = True
            results["dual_system"]["api_used"] = api_used
            
            print(f"   ✅ Dual System: {results['dual_system']['time']:.2f}s using {api_used}")
            
        except Exception as e:
            results["dual_system"]["error"] = str(e)
            print(f"   ❌ Dual System failed: {e}")
        
        self.test_results["personality_detection"] = results
        return results
    
    def test_response_generation(self):
        """Test response generation with both APIs"""
        print("\n💬 Testing Response Generation...")
        
        policy_plan = ['validate concerns warmly', 'use gentle language', 'ask one supportive question']
        conversation_context = "user: I'm worried about my job interview tomorrow."
        
        prompt = f"""Generate a helpful response following these behavioral directives: {json.dumps(policy_plan)}. CRITICAL REQUIREMENTS: 1) Only reference information explicitly mentioned in the conversation - do not introduce external facts or knowledge. 2) All statements must be grounded in the dialog context. 3) Cap questions at 1-2 maximum. 4) Keep response length appropriate (50-150 words typically). 5) Follow the personality-adapted directives while maintaining therapeutic helpfulness.

Recent conversation:
{conversation_context}

Generate an appropriate response that follows the behavioral directives and stays grounded in the conversation context."""
        
        results = {
            "gemini_direct": {"success": False, "time": 0, "response": None, "error": None},
            "juguang_fallback": {"success": False, "time": 0, "response": None, "error": None},
            "dual_system": {"success": False, "time": 0, "api_used": None, "response": None, "error": None}
        }
        
        # Test Gemini Direct
        try:
            start_time = time.time()
            content, api_used, status = self.call_gemini_direct(prompt, 0.7, 150)
            results["gemini_direct"]["time"] = time.time() - start_time
            results["gemini_direct"]["success"] = True
            results["gemini_direct"]["response"] = content[:100] + "..." if len(content) > 100 else content
            print(f"   ✅ Gemini Direct: {results['gemini_direct']['time']:.2f}s")
            print(f"      📝 Response: {results['gemini_direct']['response']}")
            
        except Exception as e:
            results["gemini_direct"]["error"] = str(e)
            print(f"   ❌ Gemini Direct failed: {e}")
        
        # Test Juguang Fallback
        try:
            start_time = time.time()
            content, api_used, status = self.call_juguang_fallback(prompt, 0.7, 150)
            results["juguang_fallback"]["time"] = time.time() - start_time
            results["juguang_fallback"]["success"] = True
            results["juguang_fallback"]["response"] = content[:100] + "..." if len(content) > 100 else content
            print(f"   ✅ Juguang Fallback: {results['juguang_fallback']['time']:.2f}s")
            print(f"      📝 Response: {results['juguang_fallback']['response']}")
            
        except Exception as e:
            results["juguang_fallback"]["error"] = str(e)
            print(f"   ❌ Juguang Fallback failed: {e}")
        
        # Test Dual System
        try:
            start_time = time.time()
            content, api_used, status = self.dual_api_call(prompt, 0.7, 150)
            results["dual_system"]["time"] = time.time() - start_time
            results["dual_system"]["success"] = True
            results["dual_system"]["api_used"] = api_used
            results["dual_system"]["response"] = content[:100] + "..." if len(content) > 100 else content
            
            print(f"   ✅ Dual System: {results['dual_system']['time']:.2f}s using {api_used}")
            print(f"      📝 Response: {results['dual_system']['response']}")
            
        except Exception as e:
            results["dual_system"]["error"] = str(e)
            print(f"   ❌ Dual System failed: {e}")
        
        self.test_results["response_generation"] = results
        return results
    
    def run_comprehensive_test(self):
        """Run all tests and provide summary"""
        print("🚀 Comprehensive Dual API System Test Suite")
        print("=" * 60)
        
        personality_results = self.test_personality_detection()
        generation_results = self.test_response_generation()
        
        # Summary
        print("\n" + "=" * 60)
        print("📊 COMPREHENSIVE TEST RESULTS")
        print("=" * 60)
        
        # Personality Detection Summary
        print("\n🧠 Personality Detection:")
        for api_type, result in personality_results.items():
            status = "✅ PASS" if result["success"] else "❌ FAIL"
            time_info = f"({result['time']:.2f}s)" if result["success"] else ""
            api_used_info = f" via {result.get('api_used', '')}" if result.get('api_used') else ""
            print(f"   {api_type.replace('_', ' ').title()}: {status} {time_info}{api_used_info}")
        
        # Response Generation Summary
        print("\n💬 Response Generation:")
        for api_type, result in generation_results.items():
            status = "✅ PASS" if result["success"] else "❌ FAIL"
            time_info = f"({result['time']:.2f}s)" if result["success"] else ""
            api_used_info = f" via {result.get('api_used', '')}" if result.get('api_used') else ""
            print(f"   {api_type.replace('_', ' ').title()}: {status} {time_info}{api_used_info}")
        
        # Overall System Health
        gemini_working = personality_results["gemini_direct"]["success"] and generation_results["gemini_direct"]["success"]
        juguang_working = personality_results["juguang_fallback"]["success"] and generation_results["juguang_fallback"]["success"]
        dual_system_working = personality_results["dual_system"]["success"] and generation_results["dual_system"]["success"]
        
        print(f"\n🔧 System Health:")
        print(f"   Primary API (Gemini Direct): {'✅ Healthy' if gemini_working else '❌ Issues'}")
        print(f"   Fallback API (Juguang): {'✅ Healthy' if juguang_working else '❌ Issues'}")
        print(f"   Dual System: {'✅ Healthy' if dual_system_working else '❌ Issues'}")
        
        # Recommendations
        print(f"\n💡 Recommendations:")
        if dual_system_working:
            print("   🎉 Dual API system is fully operational!")
            print("   📋 Ready for N8N workflow integration")
            print("   🚀 Use the dual API JavaScript files for maximum reliability")
        elif gemini_working:
            print("   ⚠️  Only Gemini Direct is working - no fallback available")
            print("   🔧 Check Juguang API key and network connectivity")
        elif juguang_working:
            print("   ⚠️  Only Juguang fallback is working")
            print("   🔧 Check Gemini API key and quota limits")
        else:
            print("   ❌ No APIs are working - check all keys and network")
        
        return {
            "gemini_working": gemini_working,
            "juguang_working": juguang_working,
            "dual_system_working": dual_system_working,
            "test_results": self.test_results
        }

if __name__ == "__main__":
    tester = DualAPITester()
    final_results = tester.run_comprehensive_test()
    
    # Exit with appropriate code
    if final_results["dual_system_working"]:
        exit(0)
    elif final_results["gemini_working"] or final_results["juguang_working"]:
        exit(1)  # Partial functionality
    else:
        exit(2)  # No APIs working
