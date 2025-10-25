"""
Test script for the /analyze endpoint
Run this to test if the Flask app is working correctly
"""

import requests
import json

# Test locally or on Railway
BASE_URL = "http://localhost:5000"  # Change to your Railway URL to test deployment
# BASE_URL = "https://your-app.railway.app"

def test_health():
    """Test health endpoint"""
    print("\n" + "="*60)
    print("Testing /health endpoint")
    print("="*60)
    try:
        response = requests.get(f"{BASE_URL}/health")
        print(f"Status Code: {response.status_code}")
        print(f"Response: {response.json()}")
        return response.status_code == 200
    except Exception as e:
        print(f"ERROR: {e}")
        return False

def test_status():
    """Test status endpoint"""
    print("\n" + "="*60)
    print("Testing /status endpoint")
    print("="*60)
    try:
        response = requests.get(f"{BASE_URL}/status")
        print(f"Status Code: {response.status_code}")
        print(f"Response: {json.dumps(response.json(), indent=2)}")
        return response.status_code == 200
    except Exception as e:
        print(f"ERROR: {e}")
        return False

def test_analyze(symbol="AAPL"):
    """Test analyze endpoint"""
    print("\n" + "="*60)
    print(f"Testing /analyze endpoint with symbol: {symbol}")
    print("="*60)
    try:
        response = requests.post(
            f"{BASE_URL}/analyze",
            json={"symbol": symbol},
            headers={"Content-Type": "application/json"}
        )
        print(f"Status Code: {response.status_code}")
        print(f"Response: {json.dumps(response.json(), indent=2)}")
        return True
    except Exception as e:
        print(f"ERROR: {e}")
        return False

def test_invalid_analyze():
    """Test analyze endpoint with invalid data"""
    print("\n" + "="*60)
    print("Testing /analyze endpoint with empty symbol")
    print("="*60)
    try:
        response = requests.post(
            f"{BASE_URL}/analyze",
            json={"symbol": ""},
            headers={"Content-Type": "application/json"}
        )
        print(f"Status Code: {response.status_code}")
        print(f"Response: {json.dumps(response.json(), indent=2)}")
        return True
    except Exception as e:
        print(f"ERROR: {e}")
        return False

if __name__ == "__main__":
    print("\n🔍 Starting Flask App Tests")
    print(f"Base URL: {BASE_URL}")
    
    results = {
        "Health Check": test_health(),
        "Status Check": test_status(),
        "Analyze (valid)": test_analyze("AAPL"),
        "Analyze (invalid)": test_invalid_analyze(),
    }
    
    print("\n" + "="*60)
    print("📊 Test Results Summary")
    print("="*60)
    for test_name, passed in results.items():
        status = "✅ PASSED" if passed else "❌ FAILED"
        print(f"{test_name}: {status}")
    
    all_passed = all(results.values())
    print("\n" + "="*60)
    if all_passed:
        print("🎉 All tests passed!")
    else:
        print("⚠️  Some tests failed. Check the output above.")
    print("="*60)

