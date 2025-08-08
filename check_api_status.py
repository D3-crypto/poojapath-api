#!/usr/bin/env python3
"""
Quick API Status Check for PoojaPath API
"""

import requests
import time

BASE_URL = "https://poojapath-api.onrender.com"

def check_api_status():
    print("🔍 Checking API Status...")
    print(f"🌐 URL: {BASE_URL}")
    
    endpoints_to_check = [
        "/admin/",
        "/api/user/signup/", 
        "/api/pandit/list/"
    ]
    
    for endpoint in endpoints_to_check:
        try:
            print(f"\n📡 Testing: {endpoint}")
            response = requests.get(f"{BASE_URL}{endpoint}", timeout=15)
            print(f"   Status: {response.status_code}")
            
            if response.status_code == 502:
                print("   ❌ 502 Bad Gateway - Service may be down or restarting")
            elif response.status_code == 200:
                print("   ✅ Service is responding")
            elif response.status_code == 401:
                print("   ✅ Service is up (authentication required)")
            elif response.status_code == 404:
                print("   ⚠️  Endpoint not found but service is responding")
            else:
                print(f"   ℹ️  Status: {response.status_code}")
                
        except requests.exceptions.Timeout:
            print("   ⏰ Timeout - Service may be slow to respond")
        except requests.exceptions.ConnectionError:
            print("   ❌ Connection Error - Service may be down")
        except Exception as e:
            print(f"   ❌ Error: {str(e)}")
    
    print(f"\n💡 If you see 502 errors, this usually means:")
    print("   • Render service is restarting (takes 1-2 minutes)")
    print("   • Service went to sleep and is waking up")
    print("   • Temporary deployment issue")
    print(f"\n🔄 Try again in 2-3 minutes if APIs are showing 502 errors")

if __name__ == "__main__":
    check_api_status()
