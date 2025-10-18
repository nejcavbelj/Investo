"""
Test script for the web application
==================================
Simple test to verify the Flask app works correctly.
"""

import requests
import json
import time
import subprocess
import sys
from pathlib import Path

def test_web_app():
    """Test the web application functionality"""
    print("🧪 Testing Investo Web Application...")
    
    # Start the Flask app in the background
    print("Starting Flask app...")
    process = subprocess.Popen([
        sys.executable, "app.py"
    ], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    
    # Wait for the app to start
    time.sleep(3)
    
    try:
        # Test the welcome page
        print("Testing welcome page...")
        response = requests.get("http://localhost:5000/")
        if response.status_code == 200:
            print("✅ Welcome page loads successfully")
        else:
            print(f"❌ Welcome page failed: {response.status_code}")
            
        # Test the analyze endpoint
        print("Testing analyze endpoint...")
        test_data = {"symbol": "AAPL"}
        response = requests.post(
            "http://localhost:5000/analyze",
            json=test_data,
            headers={"Content-Type": "application/json"}
        )
        
        if response.status_code == 200:
            result = response.json()
            if result.get("success"):
                print("✅ Stock analysis endpoint works")
                print(f"   Generated report for: {result.get('symbol')}")
            else:
                print(f"❌ Analysis failed: {result.get('error')}")
        else:
            print(f"❌ Analyze endpoint failed: {response.status_code}")
            
    except requests.exceptions.ConnectionError:
        print("❌ Could not connect to the web app. Make sure it's running.")
    except Exception as e:
        print(f"❌ Test failed with error: {e}")
    finally:
        # Clean up
        process.terminate()
        process.wait()
        print("🔄 Flask app stopped")

if __name__ == "__main__":
    test_web_app()
