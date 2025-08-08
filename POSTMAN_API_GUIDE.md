# Postman API Testing Guide for PoojaPath API

This guide shows you how to test all your API endpoints using Postman.

## 🚀 Setup

### 1. Base URL
```
http://127.0.0.1:8000
```

### 2. Server Status
Make sure your Django server is running:
```bash
python manage.py runserver
```

## 📋 API Endpoints for Postman

### **1. User Signup** 
**POST** `http://127.0.0.1:8000/api/user/signup/`

**Headers:**
```
Content-Type: application/json
```

**Body (JSON):**
```json
{
    "user_name": "john_doe",
    "email": "john@example.com",
    "password": "securepassword123",
    "reEnterPassword": "securepassword123"
}
```

**Expected Response (201):**
```json
{
    "message": "User created successfully. OTP sent to email.",
    "email": "john@example.com"
}
```

---

### **2. Verify OTP**
**POST** `http://127.0.0.1:8000/api/user/verify-otp/`

**Headers:**
```
Content-Type: application/json
```

**Body (JSON):**
```json
{
    "email": "john@example.com",
    "otp": "123456"
}
```
*Note: Check your console/terminal for the actual OTP after signup*

**Expected Response (200):**
```json
{
    "message": "Email verified successfully"
}
```

---

### **3. User Login**
**POST** `http://127.0.0.1:8000/api/user/login/`

**Headers:**
```
Content-Type: application/json
```

**Body (JSON):**
```json
{
    "email": "john@example.com",
    "password": "securepassword123",
    "deviceType": "postman"
}
```

**Expected Response (200):**
```json
{
    "message": "Login successful",
    "user": {
        "id": "user_id_here",
        "username": "john_doe",
        "email": "john@example.com"
    },
    "tokens": {
        "refresh": "refresh_token_here",
        "access": "access_token_here"
    }
}
```

**🔑 Important:** Copy the `access_token` for authenticated endpoints!

---

### **4. Forgot Password**
**POST** `http://127.0.0.1:8000/api/user/forgot-password/`

**Headers:**
```
Content-Type: application/json
```

**Body (JSON):**
```json
{
    "email": "john@example.com"
}
```

**Expected Response (200):**
```json
{
    "message": "OTP sent to email for password reset"
}
```

---

### **5. Reset Password**
**POST** `http://127.0.0.1:8000/api/user/reset-password/`

**Headers:**
```
Content-Type: application/json
```

**Body (JSON):**
```json
{
    "email": "john@example.com",
    "otp": "123456",
    "new_password": "newsecurepassword123",
    "confirm_password": "newsecurepassword123"
}
```

**Expected Response (200):**
```json
{
    "message": "Password reset successfully"
}
```

---

## 🔐 Authenticated Endpoints (Require JWT Token)

For the following endpoints, add this header:

**Headers:**
```
Content-Type: application/json
Authorization: Bearer YOUR_ACCESS_TOKEN_HERE
```

### **6. Add Pandit**
**POST** `http://127.0.0.1:8000/api/pandit/add/`

**Body (JSON):**
```json
{
    "Pandit_name": "Pandit Sharma",
    "phone": "9876543210",
    "Location": "Delhi"
}
```

**Expected Response (201):**
```json
{
    "message": "Pandit added successfully",
    "pandit": {
        "id": "pandit_id_here",
        "Pandit_name": "Pandit Sharma",
        "phone": "9876543210",
        "Location": "Delhi",
        "created_at": "2025-08-08T16:30:00Z",
        "updated_at": "2025-08-08T16:30:00Z"
    }
}
```

---

### **7. List All Pandits**
**GET** `http://127.0.0.1:8000/api/pandit/list/`

**Headers:**
```
Authorization: Bearer YOUR_ACCESS_TOKEN_HERE
```

**Expected Response (200):**
```json
{
    "message": "Pandits retrieved successfully",
    "pandits": [
        {
            "id": "pandit_id_here",
            "Pandit_name": "Pandit Sharma",
            "phone": "9876543210",
            "Location": "Delhi",
            "created_at": "2025-08-08T16:30:00Z",
            "updated_at": "2025-08-08T16:30:00Z"
        }
    ],
    "count": 1
}
```

---

### **8. Search Pandits by Location**
**GET** `http://127.0.0.1:8000/api/pandit/location/Delhi/`

**Headers:**
```
Authorization: Bearer YOUR_ACCESS_TOKEN_HERE
```

**Expected Response (200):**
```json
{
    "message": "Pandits in Delhi retrieved successfully",
    "pandits": [
        {
            "id": "pandit_id_here",
            "Pandit_name": "Pandit Sharma",
            "phone": "9876543210",
            "Location": "Delhi",
            "created_at": "2025-08-08T16:30:00Z",
            "updated_at": "2025-08-08T16:30:00Z"
        }
    ],
    "count": 1,
    "location": "Delhi"
}
```

---

### **9. Delete Pandit**
**DELETE** `http://127.0.0.1:8000/api/pandit/delete/`

**Headers:**
```
Content-Type: application/json
Authorization: Bearer YOUR_ACCESS_TOKEN_HERE
```

**Body (JSON):**
```json
{
    "Pandit_name": "Pandit Sharma",
    "Location": "Delhi"
}
```

**Expected Response (200):**
```json
{
    "message": "Pandit deleted successfully"
}
```

---

## 🧪 Testing Flow in Postman

### Step-by-Step Testing:

1. **Create a new Collection** in Postman called "PoojaPath API"

2. **Test User Flow:**
   ```
   ① Signup → ② Verify OTP → ③ Login → ④ Copy access token
   ```

3. **Test Pandit Management:**
   ```
   ⑤ Add Pandit → ⑥ List Pandits → ⑦ Search by Location → ⑧ Delete Pandit
   ```

4. **Test Password Reset:**
   ```
   ⑨ Forgot Password → ⑩ Reset Password
   ```

### Environment Variables in Postman:

Create these variables in your Postman environment:

```
base_url: http://127.0.0.1:8000
access_token: (paste your token here after login)
```

Then use `{{base_url}}` and `{{access_token}}` in your requests.

## 🔍 Debugging Tips

### Common Issues:

1. **Server not running:**
   ```
   Error: Could not get any response
   Solution: Run python manage.py runserver
   ```

2. **401 Unauthorized:**
   ```
   Error: Authentication credentials not provided
   Solution: Add Authorization: Bearer YOUR_TOKEN
   ```

3. **OTP not found:**
   ```
   Check your terminal/console for the OTP after signup/forgot password
   ```

### Where to find OTPs:
- Check your terminal/console where Django server is running
- Look for email output like: "Your OTP for email verification is: 123456"

## 📊 Response Status Codes

- `200` - Success
- `201` - Created successfully
- `400` - Bad request (invalid data)
- `401` - Unauthorized (missing/invalid token)
- `404` - Not found
- `500` - Server error

## 🎯 Sample Test Data

Use these test users for consistent testing:

```json
{
    "user_name": "testuser1",
    "email": "test1@example.com",
    "password": "testpass123",
    "reEnterPassword": "testpass123"
}
```

```json
{
    "user_name": "testuser2", 
    "email": "test2@example.com",
    "password": "testpass456",
    "reEnterPassword": "testpass456"
}
```

Happy testing! 🚀
