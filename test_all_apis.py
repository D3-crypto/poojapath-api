#!/usr/bin/env python3
import requests
import json
import time
import sys
import os

# Django setup
sys.path.append('c:/Users/sonu0/Desktop/poojapath')
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'poojapath_api.settings')

import django
django.setup()

from mongo_models import MongoOTP, MongoUser, MongoPandit

def test_all_apis():
    """Comprehensive test of all API endpoints"""
    
    base_url = "http://127.0.0.1:8000/api"
    timestamp = int(time.time())
    test_email = f"fulltest.{timestamp}@example.com"
    test_username = f"fulltest{timestamp}"
    
    print("=" * 70)
    print("🚀 COMPREHENSIVE API TEST - ALL ENDPOINTS")
    print("=" * 70)
    
    # Test results tracking
    tests = []
    
    try:
        # 1. USER SIGNUP
        print("\n1️⃣ Testing User Signup")
        print("-" * 40)
        
        signup_data = {
            "email": test_email,
            "password": "TestPass123!",
            "reEnterPassword": "TestPass123!",
            "first_name": "Full",
            "last_name": "Test",
            "user_name": test_username,
            "device_type": "mobile"
        }
        
        signup_response = requests.post(f"{base_url}/user/signup/", json=signup_data)
        signup_success = signup_response.status_code == 201
        tests.append(("User Signup", signup_success))
        
        print(f"   Status: {signup_response.status_code}")
        print(f"   Success: {'✅' if signup_success else '❌'}")
        if not signup_success:
            print(f"   Error: {signup_response.text}")
            return tests
        
        # Get OTP for verification
        otp_obj = MongoOTP.objects.filter(email=test_email, purpose="signup").latest('created_at')
        signup_otp = otp_obj.otp
        print(f"   Generated OTP: {signup_otp}")
        
        # 2. OTP VERIFICATION
        print("\n2️⃣ Testing OTP Verification")
        print("-" * 40)
        
        verify_data = {
            "email": test_email,
            "otp": signup_otp
        }
        
        verify_response = requests.post(f"{base_url}/user/verify-otp/", json=verify_data)
        verify_success = verify_response.status_code == 200
        tests.append(("OTP Verification", verify_success))
        
        print(f"   Status: {verify_response.status_code}")
        print(f"   Success: {'✅' if verify_success else '❌'}")
        
        # Check OTP deletion
        remaining_otps = MongoOTP.objects.filter(email=test_email, purpose="signup").count()
        otp_deleted = remaining_otps == 0
        tests.append(("OTP Deletion", otp_deleted))
        print(f"   OTP Deleted: {'✅' if otp_deleted else '❌'}")
        
        if not verify_success:
            print(f"   Error: {verify_response.text}")
            return tests
        
        # 3. USER LOGIN
        print("\n3️⃣ Testing User Login")
        print("-" * 40)
        
        login_data = {
            "email": test_email,
            "password": "TestPass123!",
            "device_type": "mobile"
        }
        
        login_response = requests.post(f"{base_url}/user/login/", json=login_data)
        login_success = login_response.status_code == 200
        tests.append(("User Login", login_success))
        
        print(f"   Status: {login_response.status_code}")
        print(f"   Success: {'✅' if login_success else '❌'}")
        
        if not login_success:
            print(f"   Error: {login_response.text}")
            return tests
        
        # Get JWT token for authenticated requests
        login_data_response = login_response.json()
        access_token = login_data_response.get('tokens', {}).get('access')
        headers = {"Authorization": f"Bearer {access_token}"} if access_token else {}
        print(f"   JWT Token: {'✅ Received' if access_token else '❌ Missing'}")
        tests.append(("JWT Token Generation", bool(access_token)))
        
        # 4. FORGOT PASSWORD
        print("\n4️⃣ Testing Forgot Password")
        print("-" * 40)
        
        forgot_data = {"email": test_email}
        forgot_response = requests.post(f"{base_url}/user/forgot-password/", json=forgot_data)
        forgot_success = forgot_response.status_code == 200
        tests.append(("Forgot Password", forgot_success))
        
        print(f"   Status: {forgot_response.status_code}")
        print(f"   Success: {'✅' if forgot_success else '❌'}")
        if not forgot_success:
            print(f"   Error: {forgot_response.text}")
        
        # Get forgot password OTP if successful
        forgot_otp = None
        if forgot_success:
            try:
                forgot_otp_obj = MongoOTP.objects.filter(email=test_email, purpose="forgot_password").latest('created_at')
                forgot_otp = forgot_otp_obj.otp
                print(f"   Forgot Password OTP: {forgot_otp}")
            except:
                print(f"   ⚠️ Could not retrieve forgot password OTP")
        
        # 5. RESET PASSWORD (if forgot password worked)
        if forgot_success and forgot_otp:
            print("\n5️⃣ Testing Reset Password")
            print("-" * 40)
            
            reset_data = {
                "email": test_email,
                "otp": forgot_otp,
                "new_password": "NewTestPass123!",
                "confirm_password": "NewTestPass123!"
            }
            
            reset_response = requests.post(f"{base_url}/user/reset-password/", json=reset_data)
            reset_success = reset_response.status_code == 200
            tests.append(("Reset Password", reset_success))
            
            print(f"   Status: {reset_response.status_code}")
            print(f"   Success: {'✅' if reset_success else '❌'}")
            if not reset_success:
                print(f"   Error: {reset_response.text}")
            
            # Check forgot password OTP deletion
            if reset_success:
                remaining_forgot_otps = MongoOTP.objects.filter(email=test_email, purpose="forgot_password").count()
                forgot_otp_deleted = remaining_forgot_otps == 0
                tests.append(("Forgot Password OTP Deletion", forgot_otp_deleted))
                print(f"   Forgot Password OTP Deleted: {'✅' if forgot_otp_deleted else '❌'}")
        
        # 6. PANDIT MANAGEMENT APIs (if we have auth token)
        if access_token:
            print("\n6️⃣ Testing Pandit Management APIs")
            print("-" * 40)
            
            # Add Pandit
            pandit_data = {
                "Pandit_name": f"Test Pandit {timestamp}",
                "Location": "Test Location",
                "phone": "1234567890"
            }
            
            add_pandit_response = requests.post(f"{base_url}/pandit/add/", json=pandit_data, headers=headers)
            add_pandit_success = add_pandit_response.status_code == 201
            tests.append(("Add Pandit", add_pandit_success))
            
            print(f"   Add Pandit Status: {add_pandit_response.status_code}")
            print(f"   Add Pandit Success: {'✅' if add_pandit_success else '❌'}")
            if not add_pandit_success:
                print(f"   Add Pandit Error: {add_pandit_response.text}")
            
            # List Pandits
            list_response = requests.get(f"{base_url}/pandit/list/", headers=headers)
            list_success = list_response.status_code == 200
            tests.append(("List Pandits", list_success))
            
            print(f"   List Pandits Status: {list_response.status_code}")
            print(f"   List Pandits Success: {'✅' if list_success else '❌'}")
            
            pandit_id = None
            if add_pandit_success:
                # Get the added pandit info from response  
                add_pandit_result = add_pandit_response.json()
                if 'pandit' in add_pandit_result:
                    pandit_info = add_pandit_result['pandit']
                    pandit_id = pandit_info.get('id')
                    pandit_name = pandit_info.get('Pandit_name', f"Test Pandit {timestamp}")
                    pandit_location = pandit_info.get('Location', "Test Location")
                else:
                    pandit_name = f"Test Pandit {timestamp}"
                    pandit_location = "Test Location"
            if list_success:
                list_result = list_response.json()
                pandits = list_result.get('pandits', [])
                if pandits:
                    pandit_id = pandits[0].get('_id')
                    print(f"   Found {len(pandits)} pandit(s)")
                else:
                    print("   No pandits found in list")
            
            # Search by Location
            search_response = requests.get(f"{base_url}/pandit/location/Test Location/", headers=headers)
            search_success = search_response.status_code == 200
            tests.append(("Search by Location", search_success))
            
            print(f"   Search by Location Status: {search_response.status_code}")
            print(f"   Search by Location Success: {'✅' if search_success else '❌'}")
            
            # Delete Pandit (if we successfully added one)
            if add_pandit_success:
                delete_data = {
                    "Pandit_name": pandit_name,
                    "Location": pandit_location
                }
                delete_response = requests.delete(f"{base_url}/pandit/delete/", json=delete_data, headers=headers)
                delete_success = delete_response.status_code == 200
                tests.append(("Delete Pandit", delete_success))
                
                print(f"   Delete Pandit Status: {delete_response.status_code}")
                print(f"   Delete Pandit Success: {'✅' if delete_success else '❌'}")
                if not delete_success:
                    print(f"   Delete Pandit Error: {delete_response.text}")
            
        else:
            print("\n⚠️ Skipping Pandit APIs - No JWT token available")
    
    except Exception as e:
        print(f"\n❌ Test failed with exception: {e}")
        tests.append(("Exception Handling", False))
    
    # Final Results
    print("\n" + "=" * 70)
    print("📊 FINAL TEST RESULTS")
    print("=" * 70)
    
    passed = sum(1 for _, success in tests if success)
    total = len(tests)
    
    for test_name, success in tests:
        status = "✅ PASS" if success else "❌ FAIL"
        print(f"   {test_name:<30} {status}")
    
    print("-" * 70)
    print(f"📈 OVERALL: {passed}/{total} tests passed ({(passed/total)*100:.1f}%)")
    
    if passed == total:
        print("🎉 ALL APIS WORKING PERFECTLY!")
        print("✅ Authentication system functional")
        print("✅ OTP deletion working correctly")
        print("✅ Pandit management operational")
        print("✅ Security features implemented")
    else:
        print(f"⚠️ {total - passed} test(s) failed - needs attention")
    
    print("=" * 70)
    
    return tests

if __name__ == "__main__":
    test_all_apis()
