# PoojaPath API

A Django REST API for user authentication, OTP verification, and Pandit management system with MongoDB integration.

## Features

### User Authentication
- **User Signup** with email verification via OTP
- **OTP Verification** for email confirmation
- **User Login** with JWT token authentication and device type tracking
- **Forgot Password** with OTP-based password reset

### Pandit Management
- **Add Pandit** with name, phone, and location
- **Delete Pandit** by name and location
- **List All Pandits**
- **Search Pandits by Location**

## API Endpoints

### Authentication Endpoints

#### 1. User Signup
**POST** `/api/user/signup/`
```json
{
    "user_name": "john_doe",
    "email": "john@example.com",
    "password": "securepassword123",
    "reEnterPassword": "securepassword123"
}
```

#### 2. Verify OTP for Signup
**POST** `/api/user/verify-otp/`
```json
{
    "Email": "john@example.com",
    "otp": "123456"
}
```

#### 3. User Login
**POST** `/api/user/login/`
```json
{
    "email": "john@example.com",
    "password": "securepassword123",
    "deviceType": "mobile"
}
```

#### 4. Forgot Password
**POST** `/api/user/forgot-password/`
```json
{
    "email": "john@example.com"
}
```

#### 5. Reset Password
**POST** `/api/user/reset-password/`
```json
{
    "email": "john@example.com",
    "otp": "123456",
    "new_password": "newsecurepassword123",
    "confirm_password": "newsecurepassword123"
}
```

### Pandit Management Endpoints

#### 1. Add Pandit
**POST** `/api/pandit/add/`
```json
{
    "Pandit_name": "Pandit Sharma",
    "phone": "9876543210",
    "Location": "Delhi"
}
```

#### 2. Delete Pandit
**DELETE** `/api/pandit/delete/`
```json
{
    "Pandit_name": "Pandit Sharma",
    "Location": "Delhi"
}
```

#### 3. List All Pandits
**GET** `/api/pandit/list/`

#### 4. Get Pandits by Location
**GET** `/api/pandit/location/{location}/`

## Installation and Setup

### Prerequisites
- Python 3.8+
- MongoDB
- pip (Python package manager)

### 1. Clone the Repository
```bash
git clone <repository-url>
cd poojapath
```

### 2. Configure Environment Variables
Create a `.env` file in the root directory and configure your settings:
```env
# Django Configuration
SECRET_KEY=your-secret-key-here
DEBUG=True

# Database Configuration
USE_MONGODB=False  # Set to True for MongoDB, False for SQLite
MONGODB_CONNECTION_STRING=mongodb://localhost:27017
MONGODB_DATABASE_NAME=poojapath_db

# Email Configuration (Optional)
EMAIL_BACKEND=django.core.mail.backends.console.EmailBackend
EMAIL_HOST_USER=your-email@gmail.com
EMAIL_HOST_PASSWORD=your-app-password
```

**Note:** See `ENV_CONFIGURATION_GUIDE.md` for detailed configuration instructions.

### 3. Install Dependencies
```bash
pip install -r requirements.txt
```

### 4. Configure Database (Optional - MongoDB)
If you want to use MongoDB instead of SQLite:
1. Install and start MongoDB
2. Update `.env` file:
   ```env
   USE_MONGODB=True
   MONGODB_CONNECTION_STRING=your-mongodb-connection-string
   ```
3. See `MONGODB_SETUP.md` for detailed MongoDB configuration.

### 5. Run Migrations
```bash
python manage.py makemigrations
python manage.py migrate
```

### 6. Create Superuser (Optional)
```bash
python manage.py createsuperuser
```

### 7. Run the Development Server
```bash
python manage.py runserver
```

The API will be available at `http://127.0.0.1:8000/`

## Environment Configuration

The project uses environment variables for configuration. Key settings include:

- `SECRET_KEY` - Django secret key (required)
- `DEBUG` - Debug mode (True/False)
- `USE_MONGODB` - Database choice (True for MongoDB, False for SQLite)
- `MONGODB_CONNECTION_STRING` - MongoDB connection string
- `EMAIL_HOST_USER` - Email configuration for OTP sending

See `ENV_CONFIGURATION_GUIDE.md` for complete configuration details.

## Authentication

Most endpoints require authentication using JWT tokens. After successful login, include the access token in the Authorization header:

```
Authorization: Bearer <your-access-token>
```

## Environment Configuration

For production deployment, create a `.env` file and configure:

```env
SECRET_KEY=your-secret-key
DEBUG=False
MONGODB_CONNECTION_STRING=your-mongodb-connection-string
EMAIL_HOST=smtp.gmail.com
EMAIL_HOST_USER=your-email@gmail.com
EMAIL_HOST_PASSWORD=your-app-password
```

## Error Handling

The API returns appropriate HTTP status codes and error messages:

- `200 OK` - Success
- `201 Created` - Resource created successfully
- `400 Bad Request` - Invalid request data
- `401 Unauthorized` - Authentication required
- `404 Not Found` - Resource not found
- `500 Internal Server Error` - Server error

## Models

### User Model
- `username` - Unique username
- `email` - Unique email address
- `password` - Hashed password
- `is_verified` - Email verification status
- `created_at` - Account creation timestamp
- `updated_at` - Last update timestamp

### OTP Model
- `email` - Email address
- `otp` - 6-digit OTP code
- `purpose` - signup/forgot_password
- `is_used` - Usage status
- `created_at` - Creation timestamp

### Pandit Model
- `Pandit_name` - Pandit's name
- `phone` - Contact phone number
- `Location` - Service location
- `created_at` - Record creation timestamp
- `updated_at` - Last update timestamp

### LoginSession Model
- `user` - Reference to User
- `device_type` - Device type (mobile/web/tablet)
- `login_time` - Login timestamp
- `is_active` - Session status

## Security Features

- JWT token-based authentication
- Password hashing using Django's built-in system
- OTP expiration (10 minutes)
- CORS configuration for frontend integration
- Input validation and sanitization

## Testing

Run the test suite:
```bash
python manage.py test
```

## Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests for new functionality
5. Submit a pull request

## License

This project is licensed under the MIT License.
