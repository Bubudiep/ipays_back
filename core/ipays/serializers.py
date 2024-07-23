# serializers.py
from django.contrib.auth.models import User
from rest_framework import serializers
from .models import *
from django.db import IntegrityError, transaction

class UserProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserProfile
        fields = "__all__"
class UserSerializer(serializers.ModelSerializer):
    profile = serializers.SerializerMethodField(default=None)
    def get_profile(self,obj):
        try:
            qs_profile=UserProfile.objects.get(user=obj)
            return UserProfileSerializer(qs_profile,many=False).data
        except Exception as e:
            return None
    class Meta:
      model = User
      fields = ['id', 'username', 'email', 'first_name', 'last_name', 'profile']

class UserRegistrationSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)
    zalo_key = serializers.CharField(write_only=True)
    zalo_name = serializers.CharField(write_only=True)

    class Meta:
        model = User
        fields = ['username', 'password', 'email', 'first_name', 'last_name', 'zalo_key', 'zalo_name']

    def create(self, validated_data):
        with transaction.atomic():
            username = validated_data['username']
            password = validated_data['password']
            email = validated_data.get('email', '')
            first_name = validated_data.get('first_name', '')
            last_name = validated_data.get('last_name', '')
            zalo_key = validated_data.get('zalo_key', None)
            zalo_name = validated_data.get('zalo_name', None)
            
            # Check if zalo_key already exists in UserProfile
            if zalo_key is not None and UserProfile.objects.filter(zalo_key=zalo_key).exists():
                raise TypeError("Zalo key already exists.")

            # Create the user
            user = User.objects.create_user(
                username=username,
                password=password,
                email=email,
                first_name=first_name,
                last_name=last_name
            )

            # Create UserProfile
            UserProfile.objects.create(user=user, zalo_key=zalo_key)

        return user
    
class PasswordSerializer(serializers.Serializer):
    password = serializers.CharField(max_length=255)
    logout = serializers.BooleanField(default=False)