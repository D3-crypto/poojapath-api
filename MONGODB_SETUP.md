# MongoDB Configuration Guide

This guide explains how to configure MongoDB for the PoojaPath API.

## Current Setup
The project is currently configured to use SQLite for development. To switch to MongoDB, follow the steps below.

## Prerequisites
1. Install MongoDB on your system
2. Ensure MongoDB service is running

## Installation Options

### Option 1: Local MongoDB Installation
1. Download MongoDB from https://www.mongodb.com/try/download/community
2. Install MongoDB following the platform-specific instructions
3. Start MongoDB service:
   - Windows: Start "MongoDB" service from Services
   - macOS: `brew services start mongodb-community`
   - Linux: `sudo systemctl start mongod`

### Option 2: MongoDB Atlas (Cloud)
1. Create account at https://www.mongodb.com/atlas
2. Create a free cluster
3. Get connection string from Atlas dashboard

### Option 3: Docker MongoDB
```bash
docker run -d -p 27017:27017 --name mongodb mongo:latest
```

## Configuration Steps

### 1. Install Required Packages
The packages are already installed, but if needed:
```bash
pip install djongo pymongo
```

### 2. Update settings.py
Replace the database configuration in `poojapath_api/settings.py`:

```python
# For local MongoDB
DATABASES = {
    'default': {
        'ENGINE': 'djongo',
        'NAME': 'poojapath_db',
        'CLIENT': {
            'host': 'mongodb://localhost:27017',
        }
    }
}

# For MongoDB Atlas
DATABASES = {
    'default': {
        'ENGINE': 'djongo',
        'NAME': 'poojapath_db',
        'CLIENT': {
            'host': 'mongodb+srv://username:password@cluster.mongodb.net/poojapath_db?retryWrites=true&w=majority',
        }
    }
}

# For Docker MongoDB with authentication
DATABASES = {
    'default': {
        'ENGINE': 'djongo',
        'NAME': 'poojapath_db',
        'CLIENT': {
            'host': 'mongodb://username:password@localhost:27017',
        }
    }
}
```

### 3. Update Model Imports
Change imports in model files from:
```python
from django.db import models
```
to:
```python
from djongo import models
```

### 4. Run Migrations
```bash
python manage.py makemigrations
python manage.py migrate
```

## Connection String Examples

### Local MongoDB
```
mongodb://localhost:27017
```

### MongoDB with Authentication
```
mongodb://username:password@localhost:27017
```

### MongoDB Atlas
```
mongodb+srv://username:password@cluster.mongodb.net/database_name?retryWrites=true&w=majority
```

### MongoDB Replica Set
```
mongodb://host1:27017,host2:27017,host3:27017/database_name?replicaSet=myReplicaSet
```

## Environment Variables
For security, use environment variables:

1. Install python-decouple: `pip install python-decouple`
2. Create `.env` file:
```env
MONGODB_CONNECTION_STRING=mongodb://localhost:27017
MONGODB_DATABASE_NAME=poojapath_db
```

3. Update settings.py:
```python
from decouple import config

DATABASES = {
    'default': {
        'ENGINE': 'djongo',
        'NAME': config('MONGODB_DATABASE_NAME', default='poojapath_db'),
        'CLIENT': {
            'host': config('MONGODB_CONNECTION_STRING', default='mongodb://localhost:27017'),
        }
    }
}
```

## Troubleshooting

### Common Issues

1. **Connection Refused Error**
   - Ensure MongoDB service is running
   - Check if MongoDB is listening on the correct port (27017)

2. **Authentication Failed**
   - Verify username and password in connection string
   - Check if user has proper permissions

3. **SSL Certificate Error (Atlas)**
   - Add `ssl=true&ssl_cert_reqs=CERT_NONE` to connection string

4. **Timeout Error**
   - Increase timeout in CLIENT configuration:
   ```python
   'CLIENT': {
       'host': 'your-connection-string',
       'serverSelectionTimeoutMS': 30000,
       'connectTimeoutMS': 30000,
   }
   ```

### Testing MongoDB Connection
Create a test script:
```python
from pymongo import MongoClient

try:
    client = MongoClient('your-connection-string')
    db = client['poojapath_db2']
    print("MongoDB connection successful!")
    print("Database collections:", db.list_collection_names())
except Exception as e:
    print("MongoDB connection failed:", str(e))
```

## Production Considerations

1. **Security**
   - Use authentication
   - Enable SSL/TLS
   - Use IP whitelisting

2. **Performance**
   - Create indexes for frequently queried fields
   - Monitor connection pool settings

3. **Backup**
   - Set up regular backups
   - Test restore procedures

4. **Monitoring**
   - Monitor database performance
   - Set up alerts for issues

## Collections Structure
After migration, your MongoDB will have these collections:
- `users` - User authentication data
- `otps` - OTP verification codes
- `login_sessions` - User login sessions
- `pandits` - Pandit information
