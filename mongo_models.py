"""
MongoDB Models for PoojaPath API

These models use MongoDB directly while Django uses SQLite for its internal operations.
"""

from datetime import datetime, timedelta
import random
import string
from bson import ObjectId
from mongodb_handler import mongo_handler
from django.contrib.auth.hashers import make_password, check_password


class MongoUserManager:
    """Django-like manager for MongoUser"""
    
    def filter(self, **kwargs):
        """Filter users by criteria"""
        collection = mongo_handler.get_collection('users')
        
        # Build filter criteria
        filter_dict = {}
        for key, value in kwargs.items():
            filter_dict[key] = value
        
        # Find matching documents
        cursor = collection.find(filter_dict)
        return MongoUserQuerySet(cursor)
    
    def get(self, **kwargs):
        """Get single user by criteria"""
        results = self.filter(**kwargs)
        if len(results) == 0:
            raise Exception("User not found")
        elif len(results) > 1:
            raise Exception("Multiple users found")
        
        # Access the actual results
        if results._results is None:
            results._results = list(results.cursor)
        
        # Create MongoUser instance from the result
        user_data = results._results[0]
        return MongoUser(**user_data)


class MongoUserQuerySet:
    """Django-like queryset for MongoUser"""
    
    def __init__(self, cursor):
        self.cursor = cursor
        self._results = None
    
    def count(self):
        """Count matching users"""
        if self._results is None:
            self._results = list(self.cursor)
        return len(self._results)
    
    def __len__(self):
        return self.count()
    
    def delete(self):
        """Delete all matching users"""
        if self._results is None:
            self._results = list(self.cursor)
        
        collection = mongo_handler.get_collection('users')
        for result in self._results:
            collection.delete_one({'_id': result['_id']})


class MongoUser:
    """MongoDB User model"""
    
    # Django-like objects manager
    objects = MongoUserManager()
    
    def __init__(self, **kwargs):
        self.collection = mongo_handler.get_collection('users')
        self.data = kwargs
    
    @classmethod
    def create_user(cls, username, email, password):
        """Create a new user"""
        user_data = {
            'username': username,
            'email': email,
            'password': make_password(password),
            'is_verified': False,
            'created_at': datetime.utcnow(),
            'updated_at': datetime.utcnow()
        }
        
        collection = mongo_handler.get_collection('users')
        
        # Check if user already exists
        if collection.find_one({'email': email}):
            raise ValueError("User with this email already exists")
        
        result = collection.insert_one(user_data)
        user_data['_id'] = result.inserted_id
        return cls(**user_data)
    
    @classmethod
    def get_by_email(cls, email):
        """Get user by email"""
        collection = mongo_handler.get_collection('users')
        user_data = collection.find_one({'email': email})
        return cls(**user_data) if user_data else None
    
    @classmethod
    def get_by_id(cls, user_id):
        """Get user by ID"""
        collection = mongo_handler.get_collection('users')
        user_data = collection.find_one({'_id': ObjectId(user_id)})
        return cls(**user_data) if user_data else None
    
    @classmethod
    def authenticate(cls, email, password):
        """Authenticate user with email and password"""
        user = cls.get_by_email(email)
        if user and user.check_password(password):
            return user
        return None
    
    def check_password(self, password):
        """Check if password is correct"""
        return check_password(password, self.data.get('password'))
    
    def set_password(self, password):
        """Set new password"""
        self.data['password'] = make_password(password)
        self.save()
    
    def verify_email(self):
        """Mark email as verified"""
        self.data['is_verified'] = True
        self.save()
    
    def save(self):
        """Save user data to MongoDB"""
        self.data['updated_at'] = datetime.utcnow()
        collection = mongo_handler.get_collection('users')
        collection.update_one(
            {'_id': self.data['_id']},
            {'$set': self.data}
        )
    
    @property
    def id(self):
        return str(self.data.get('_id'))
    
    @property
    def username(self):
        return self.data.get('username')
    
    @property
    def email(self):
        return self.data.get('email')
    
    @property
    def password(self):
        return self.data.get('password')
    
    @property
    def is_verified(self):
        return self.data.get('is_verified', False)


class MongoOTPManager:
    """Django-like manager for MongoOTP"""
    
    def filter(self, **kwargs):
        """Filter OTPs by criteria"""
        collection = mongo_handler.get_collection('otps')
        
        # Build filter criteria
        filter_dict = {}
        for key, value in kwargs.items():
            filter_dict[key] = value
        
        # Find matching documents
        cursor = collection.find(filter_dict)
        return MongoOTPQuerySet(cursor)
    
    def get(self, **kwargs):
        """Get single OTP by criteria"""
        results = self.filter(**kwargs)
        if len(results) == 0:
            from django.core.exceptions import ObjectDoesNotExist
            raise ObjectDoesNotExist("OTP matching query does not exist")
        elif len(results) > 1:
            raise Exception("Multiple OTPs found")
        return results[0]


class MongoOTPQuerySet:
    """Django-like queryset for MongoOTP"""
    
    def __init__(self, cursor):
        self.cursor = cursor
        self._results = None
    
    def latest(self, field='created_at'):
        """Get latest OTP by field"""
        if self._results is None:
            self._results = list(self.cursor.sort([(field, -1)]))
        
        if not self._results:
            from django.core.exceptions import ObjectDoesNotExist
            raise ObjectDoesNotExist("OTP matching query does not exist")
        
        return MongoOTP(**self._results[0])
    
    def count(self):
        """Count matching OTPs"""
        if self._results is None:
            self._results = list(self.cursor)
        return len(self._results)
    
    def delete(self):
        """Delete all matching OTPs"""
        if self._results is None:
            self._results = list(self.cursor)
        
        collection = mongo_handler.get_collection('otps')
        deleted_count = 0
        for result in self._results:
            collection.delete_one({'_id': result['_id']})
            deleted_count += 1
        return deleted_count
    
    def __len__(self):
        return self.count()


class MongoOTP:
    """MongoDB OTP model"""
    
    # Django-like objects manager
    objects = MongoOTPManager()
    
    def __init__(self, **kwargs):
        self.collection = mongo_handler.get_collection('otps')
        self.data = kwargs
    
    @classmethod
    def create_otp(cls, email, purpose='signup'):
        """Create a new OTP"""
        # Clean up expired OTPs first (automatic maintenance)
        cls.cleanup_expired_otps()
        
        otp_code = cls.generate_otp()
        otp_data = {
            'email': email,
            'otp': otp_code,
            'purpose': purpose,
            'is_used': False,
            'created_at': datetime.utcnow()
        }
        
        collection = mongo_handler.get_collection('otps')
        result = collection.insert_one(otp_data)
        otp_data['_id'] = result.inserted_id
        return cls(**otp_data)
    
    @classmethod
    def get_latest_unused(cls, email, purpose):
        """Get latest unused OTP for email and purpose"""
        collection = mongo_handler.get_collection('otps')
        otp_data = collection.find_one(
            {'email': email, 'purpose': purpose, 'is_used': False},
            sort=[('created_at', -1)]
        )
        return cls(**otp_data) if otp_data else None
    
    @staticmethod
    def generate_otp():
        """Generate a 6-digit OTP"""
        return ''.join(random.choices(string.digits, k=6))
    
    def is_valid(self):
        """Check if OTP is still valid (within 10 minutes)"""
        if self.data.get('is_used'):
            return False
        
        created_at = self.data.get('created_at')
        if not created_at:
            return False
        
        return (datetime.utcnow() - created_at).total_seconds() < 600  # 10 minutes
    
    def mark_as_used(self):
        """Mark OTP as used"""
        self.data['is_used'] = True
        collection = mongo_handler.get_collection('otps')
        collection.update_one(
            {'_id': self.data['_id']},
            {'$set': {'is_used': True}}
        )
    
    def delete(self):
        """Delete OTP from database (security best practice after verification)"""
        print(f"🗑️ DEBUG: Deleting OTP with ID: {self.data.get('_id')}")
        collection = mongo_handler.get_collection('otps')
        result = collection.delete_one({'_id': self.data['_id']})
        print(f"🗑️ DEBUG: Delete result - Deleted count: {result.deleted_count}")
        return result
    
    @classmethod
    def cleanup_expired_otps(cls):
        """Delete all expired OTPs (older than 10 minutes)"""
        collection = mongo_handler.get_collection('otps')
        expiry_time = datetime.utcnow() - timedelta(minutes=10)
        result = collection.delete_many({'created_at': {'$lt': expiry_time}})
        return result.deleted_count
    
    @property
    def otp(self):
        return self.data.get('otp')
    
    @property
    def email(self):
        return self.data.get('email')
    
    @property  
    def purpose(self):
        return self.data.get('purpose')
    
    @property
    def is_used(self):
        return self.data.get('is_used', False)
    
    @property
    def created_at(self):
        return self.data.get('created_at')


class MongoPandit:
    """MongoDB Pandit model"""
    
    def __init__(self, **kwargs):
        self.collection = mongo_handler.get_collection('pandits')
        self.data = kwargs
    
    @classmethod
    def create_pandit(cls, pandit_name, phone, location):
        """Create a new pandit"""
        collection = mongo_handler.get_collection('pandits')
        
        # Check if pandit already exists
        if collection.find_one({'Pandit_name': pandit_name, 'Location': location}):
            raise ValueError("Pandit with this name and location already exists")
        
        pandit_data = {
            'Pandit_name': pandit_name,
            'phone': phone,
            'Location': location,
            'created_at': datetime.utcnow(),
            'updated_at': datetime.utcnow()
        }
        
        result = collection.insert_one(pandit_data)
        pandit_data['_id'] = result.inserted_id
        return cls(**pandit_data)
    
    @classmethod
    def get_by_name_and_location(cls, pandit_name, location):
        """Get pandit by name and location"""
        collection = mongo_handler.get_collection('pandits')
        pandit_data = collection.find_one({
            'Pandit_name': pandit_name,
            'Location': location
        })
        return cls(**pandit_data) if pandit_data else None
    
    @classmethod
    def get_all(cls):
        """Get all pandits"""
        collection = mongo_handler.get_collection('pandits')
        pandits = []
        for pandit_data in collection.find():
            pandits.append(cls(**pandit_data))
        return pandits
    
    @classmethod
    def get_by_location(cls, location):
        """Get pandits by location"""
        collection = mongo_handler.get_collection('pandits')
        pandits = []
        for pandit_data in collection.find({'Location': {'$regex': location, '$options': 'i'}}):
            pandits.append(cls(**pandit_data))
        return pandits
    
    def delete(self):
        """Delete pandit"""
        collection = mongo_handler.get_collection('pandits')
        collection.delete_one({'_id': self.data['_id']})
    
    def to_dict(self):
        """Convert to dictionary"""
        data = self.data.copy()
        data['id'] = str(data.pop('_id'))
        return data
    
    @property
    def id(self):
        return str(self.data.get('_id'))
    
    @property
    def pandit_name(self):
        return self.data.get('Pandit_name')
    
    @property
    def phone(self):
        return self.data.get('phone')
    
    @property
    def location(self):
        return self.data.get('Location')


class MongoLoginSession:
    """MongoDB Login Session model"""
    
    def __init__(self, **kwargs):
        self.collection = mongo_handler.get_collection('login_sessions')
        self.data = kwargs
    
    @classmethod
    def create_session(cls, user_id, device_type):
        """Create a new login session"""
        session_data = {
            'user_id': user_id,
            'device_type': device_type,
            'login_time': datetime.utcnow(),
            'is_active': True
        }
        
        collection = mongo_handler.get_collection('login_sessions')
        result = collection.insert_one(session_data)
        session_data['_id'] = result.inserted_id
        return cls(**session_data)
