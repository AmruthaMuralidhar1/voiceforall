"""
Test script for VoiceTech for All TTS API
"""

import requests
import json
import time
from pathlib import Path

BASE_URL = "http://localhost:8000"

def test_health():
    """Test health endpoint"""
    print("\n🏥 Testing Health Endpoint...")
    try:
        response = requests.get(f"{BASE_URL}/health")
        print(f"✅ Status: {response.status_code}")
        print(f"   Response: {response.json()}")
        return response.status_code == 200
    except Exception as e:
        print(f"❌ Error: {e}")
        return False


def test_info():
    """Test info endpoint"""
    print("\n📋 Testing Info Endpoint...")
    try:
        response = requests.get(f"{BASE_URL}/info")
        print(f"✅ Status: {response.status_code}")
        data = response.json()
        print(f"   Model: {data.get('name')}")
        print(f"   Version: {data.get('version')}")
        print(f"   Languages: {len(data.get('languages', []))}")
        print(f"   Accents: {data.get('accents')}")
        print(f"   Styles: {data.get('styles')}")
        return response.status_code == 200
    except Exception as e:
        print(f"❌ Error: {e}")
        return False


def test_languages():
    """Test languages endpoint"""
    print("\n🗣️ Testing Languages Endpoint...")
    try:
        response = requests.get(f"{BASE_URL}/languages")
        print(f"✅ Status: {response.status_code}")
        data = response.json()
        print(f"   Supported languages: {data.get('count')}")
        for code, name in list(data.get('languages', {}).items())[:5]:
            print(f"     - {code}: {name}")
        return response.status_code == 200
    except Exception as e:
        print(f"❌ Error: {e}")
        return False


def test_inference():
    """Test main inference endpoint"""
    print("\n🎤 Testing Inference Endpoint...")
    try:
        payload = {
            "text": "नमस्ते दुनिया",
            "language": "hi",
            "accent_id": 0,
            "style_id": 0
        }
        
        print(f"   Request: {json.dumps(payload, ensure_ascii=False)}")
        
        response = requests.post(
            f"{BASE_URL}/Get_Inference",
            json=payload,
            timeout=30
        )
        
        print(f"✅ Status: {response.status_code}")
        
        if response.status_code == 200:
            # Save audio
            output_path = Path("test_output.wav")
            with open(output_path, "wb") as f:
                f.write(response.content)
            print(f"   Audio saved: {output_path}")
            print(f"   File size: {output_path.stat().st_size} bytes")
            return True
        else:
            print(f"   Error: {response.text}")
            return False
    
    except Exception as e:
        print(f"❌ Error: {e}")
        return False


def test_synthesize():
    """Test synthesize endpoint"""
    print("\n🎵 Testing Synthesize Endpoint...")
    try:
        payload = {
            "text": "नमस्ते दुनिया",
            "language": "hi",
            "accent_id": 1,
            "style_id": 1
        }
        
        response = requests.post(
            f"{BASE_URL}/synthesize",
            json=payload,
            timeout=30
        )
        
        print(f"✅ Status: {response.status_code}")
        
        if response.status_code == 200:
            data = response.json()
            print(f"   Status: {data.get('status')}")
            print(f"   Message: {data.get('message')}")
            print(f"   Audio URL: {data.get('audio_url')}")
            print(f"   Duration: {data.get('duration')}s")
            return True
        else:
            print(f"   Error: {response.text}")
            return False
    
    except Exception as e:
        print(f"❌ Error: {e}")
        return False


def test_invalid_language():
    """Test error handling"""
    print("\n⚠️ Testing Error Handling (Invalid Language)...")
    try:
        payload = {
            "text": "Hello",
            "language": "xx",
            "accent_id": 0,
            "style_id": 0
        }
        
        response = requests.post(
            f"{BASE_URL}/Get_Inference",
            json=payload
        )
        
        if response.status_code == 400:
            print(f"✅ Correctly rejected invalid language")
            print(f"   Error: {response.json().get('detail')}")
            return True
        else:
            print(f"❌ Should have returned 400")
            return False
    
    except Exception as e:
        print(f"❌ Error: {e}")
        return False


def run_all_tests():
    """Run all tests"""
    print("=" * 70)
    print("VoiceTech for All - API Test Suite")
    print("=" * 70)
    
    tests = [
        ("Health Check", test_health),
        ("Model Info", test_info),
        ("Languages", test_languages),
        ("Error Handling", test_invalid_language),
        ("Inference", test_inference),
        ("Synthesize", test_synthesize),
    ]
    
    results = []
    for name, test_func in tests:
        try:
            result = test_func()
            results.append((name, result))
        except Exception as e:
            print(f"❌ Test failed: {e}")
            results.append((name, False))
        
        time.sleep(1)  # Rate limiting
    
    # Summary
    print("\n" + "=" * 70)
    print("📊 Test Summary")
    print("=" * 70)
    
    passed = sum(1 for _, result in results if result)
    total = len(results)
    
    for name, result in results:
        status = "✅ PASS" if result else "❌ FAIL"
        print(f"{status}: {name}")
    
    print(f"\nTotal: {passed}/{total} tests passed")
    print("=" * 70)
    
    return passed == total


if __name__ == "__main__":
    import sys
    
    print("\n⏳ Waiting for API to be ready...")
    print(f"   Make sure API is running at {BASE_URL}")
    print("   Run: python app.py\n")
    
    time.sleep(2)
    
    success = run_all_tests()
    sys.exit(0 if success else 1)

