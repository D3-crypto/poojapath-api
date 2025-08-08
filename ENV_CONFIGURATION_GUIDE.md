# Environment Configuration Guide for PoojaPath API

This guide explains how to configure the `.env` file for your PoojaPath API project.

## .env File Location
The `.env` file should be placed in the root directory of your project:
```
poojapath/
├── .env                    # <- Place it here
├── manage.py
├── poojapath_api/
├── authentication/
└── pandit_management/
```

## Configuration Options

### 1. Django Security Configuration

#### SECRET_KEY (Required)
Your Django secret key for cryptographic signing.
```env
SECRET_KEY=your-very-secure-secret-key-here-make-it-long-and-random
```

**How to generate a secure secret key:**
- Run: `python -c "from django.core.management.utils import get_random_secret_key; print(get_random_secret_key())"`
- Or use online generators (ensure they're secure)

#### DEBUG (Required)
Controls Django debug mode.
```env
DEBUG=True   # For development
DEBUG=False  # For production
```

### 2. Database Configuration

#### USE_MONGODB (Required)
Switch between SQLite and MongoDB.
```env
USE_MONGODB=False  # Use SQLite (default, good for development)
USE_MONGODB=True   # Use MongoDB (for production or if you prefer MongoDB)
```

#### MongoDB Settings (Required if USE_MONGODB=True)
```env
MONGODB_CONNECTION_STRING=mongodb://localhost:27017
MONGODB_DATABASE_NAME=poojapath_db
```

**MongoDB Connection String Examples:**
- Local: `mongodb://localhost:27017`
- With auth: `mongodb://username:password@localhost:27017`
- MongoDB Atlas: `mongodb+srv://username:password@cluster.mongodb.net/dbname?retryWrites=true&w=majority`
- Docker: `mongodb://localhost:27017` (if MongoDB runs on default port)

### 3. Email Configuration (Optional)

#### Email Backend
```env
EMAIL_BACKEND=django.core.mail.backends.console.EmailBackend  # Development (prints to console)
EMAIL_BACKEND=django.core.mail.backends.smtp.EmailBackend     # Production (sends real emails)
```

#### SMTP Settings (Required for production email)
```env
EMAIL_HOST=smtp.gmail.com
EMAIL_PORT=587
EMAIL_USE_TLS=True
EMAIL_HOST_USER=your-email@gmail.com
EMAIL_HOST_PASSWORD=your-app-password
```

**For Gmail:**
1. Enable 2-factor authentication
2. Generate an "App Password" in your Google Account settings
3. Use the app password (not your regular password)

### 4. CORS Configuration (Optional)
```env
CORS_ALLOW_ALL_ORIGINS=True   # Development (allows all origins)
CORS_ALLOW_ALL_ORIGINS=False  # Production (only allowed origins)
```

### 5. JWT Token Configuration (Optional)
```env
JWT_ACCESS_TOKEN_LIFETIME_MINUTES=60  # Access token expires in 60 minutes
JWT_REFRESH_TOKEN_LIFETIME_DAYS=1     # Refresh token expires in 1 day
```

## Example .env Files

### Development Configuration
```env
# Django Configuration
SECRET_KEY=django-insecure-development-key-change-in-production
DEBUG=True

# Database Configuration (SQLite for development)
USE_MONGODB=False
MONGODB_CONNECTION_STRING=mongodb://localhost:27017
MONGODB_DATABASE_NAME=poojapath_db

# Email Configuration (Console backend for development)
EMAIL_BACKEND=django.core.mail.backends.console.EmailBackend
EMAIL_HOST=smtp.gmail.com
EMAIL_PORT=587
EMAIL_USE_TLS=True
EMAIL_HOST_USER=
EMAIL_HOST_PASSWORD=

# CORS Configuration
CORS_ALLOW_ALL_ORIGINS=True

# JWT Configuration
JWT_ACCESS_TOKEN_LIFETIME_MINUTES=60
JWT_REFRESH_TOKEN_LIFETIME_DAYS=1
```

### Production Configuration
```env
# Django Configuration
SECRET_KEY=your-super-secret-production-key-here-very-long-and-random
DEBUG=False

# Database Configuration (MongoDB for production)
USE_MONGODB=True
MONGODB_CONNECTION_STRING=mongodb+srv://username:password@cluster.mongodb.net/poojapath_db?retryWrites=true&w=majority
MONGODB_DATABASE_NAME=poojapath_db

# Email Configuration (SMTP for production)
EMAIL_BACKEND=django.core.mail.backends.smtp.EmailBackend
EMAIL_HOST=smtp.gmail.com
EMAIL_PORT=587
EMAIL_USE_TLS=True
EMAIL_HOST_USER=your-production-email@gmail.com
EMAIL_HOST_PASSWORD=your-gmail-app-password

# CORS Configuration
CORS_ALLOW_ALL_ORIGINS=False

# JWT Configuration
JWT_ACCESS_TOKEN_LIFETIME_MINUTES=30
JWT_REFRESH_TOKEN_LIFETIME_DAYS=7
```

## Quick Setup Steps

1. **Copy the template:**
   ```bash
   cp .env.example .env  # If you have a template
   ```

2. **Edit the .env file:**
   - Add your secret key
   - Set DEBUG=True for development
   - Choose database (SQLite or MongoDB)
   - Configure email if needed

3. **Test your configuration:**
   ```bash
   python manage.py check
   python manage.py runserver
   ```

## Security Best Practices

1. **Never commit .env to version control:**
   Add `.env` to your `.gitignore` file:
   ```gitignore
   .env
   .env.local
   .env.production
   ```

2. **Use strong secret keys:**
   - At least 50 characters long
   - Mix of letters, numbers, and symbols
   - Different for each environment

3. **Production settings:**
   - Always set `DEBUG=False`
   - Use secure database connections
   - Configure proper CORS settings
   - Use real email backend for notifications

## Troubleshooting

### Common Issues:

1. **SECRET_KEY not found:**
   - Ensure `.env` file exists in root directory
   - Check that `SECRET_KEY` is properly set

2. **Database connection errors:**
   - Verify MongoDB is running (if USE_MONGODB=True)
   - Check connection string format
   - Ensure database credentials are correct

3. **Email not sending:**
   - Check EMAIL_BACKEND setting
   - Verify SMTP credentials
   - For Gmail, use app passwords

4. **Environment variables not loading:**
   - Ensure python-decouple is installed: `pip install python-decouple`
   - Check .env file location and format

## Testing Your Configuration

Run these commands to verify your setup:
```bash
# Check Django configuration
python manage.py check

# Test database connection
python manage.py migrate

# Create a test user (optional)
python manage.py createsuperuser

# Start development server
python manage.py runserver
```

Your API should now be running with your custom configuration!
