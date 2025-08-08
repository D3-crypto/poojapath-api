from rest_framework import serializers
from django.contrib.auth import authenticate
from django.conf import settings

# Dynamic model imports based on database configuration
if getattr(settings, 'USE_MONGODB', False):
    from mongo_models import MongoUser as User, MongoOTP as OTP
else:
    from .models import User, OTP


class UserSignupSerializer(serializers.Serializer):
    user_name = serializers.CharField(max_length=150)
    email = serializers.EmailField()
    password = serializers.CharField(write_only=True)
    reEnterPassword = serializers.CharField(write_only=True)

    def validate(self, data):
        if data['password'] != data['reEnterPassword']:
            raise serializers.ValidationError("Passwords do not match")
        
        # Check using appropriate model (MongoDB or Django ORM)
        if getattr(settings, 'USE_MONGODB', False):
            if User.get_by_email(data['email']):
                raise serializers.ValidationError("User with this email already exists")
        else:
            if User.objects.filter(email=data['email']).exists():
                raise serializers.ValidationError("User with this email already exists")
        
        return data

    def create(self, validated_data):
        validated_data.pop('reEnterPassword')
        user = User.objects.create_user(
            username=validated_data['user_name'],
            email=validated_data['email'],
            password=validated_data['password']
        )
        return user


class OTPVerificationSerializer(serializers.Serializer):
    email = serializers.EmailField()
    otp = serializers.CharField(max_length=6)


class UserLoginSerializer(serializers.Serializer):
    email = serializers.EmailField()
    password = serializers.CharField()
    deviceType = serializers.CharField()

    def validate(self, data):
        email = data.get('email')
        password = data.get('password')

        if email and password:
            user = authenticate(username=email, password=password)
            if not user:
                raise serializers.ValidationError("Invalid email or password")
            if not user.is_verified:
                raise serializers.ValidationError("Email not verified")
            data['user'] = user
        else:
            raise serializers.ValidationError("Email and password required")

        return data


class ForgotPasswordSerializer(serializers.Serializer):
    email = serializers.EmailField()

    def validate_email(self, value):
        # Check using appropriate model (MongoDB or Django ORM)
        if getattr(settings, 'USE_MONGODB', False):
            if not User.get_by_email(value):
                raise serializers.ValidationError("User with this email does not exist")
        else:
            if not User.objects.filter(email=value).exists():
                raise serializers.ValidationError("User with this email does not exist")
        return value


class ResetPasswordSerializer(serializers.Serializer):
    email = serializers.EmailField()
    otp = serializers.CharField(max_length=6)
    new_password = serializers.CharField(write_only=True)
    confirm_password = serializers.CharField(write_only=True)

    def validate(self, data):
        if data['new_password'] != data['confirm_password']:
            raise serializers.ValidationError("Passwords do not match")
        return data
