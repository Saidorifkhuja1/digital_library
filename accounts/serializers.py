from .models import *
from django.contrib.auth import get_user_model
from rest_framework import serializers
from django.contrib.auth.hashers import make_password

class UserRegistrationSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)
    confirm_password = serializers.CharField(write_only=True)
    is_admin = serializers.BooleanField(write_only=True, required=False)

    class Meta:
        model = User
        fields = ['name', 'last_name', 'phone_number', 'email', 'password', 'confirm_password', 'is_admin', 'avatar']

    def validate(self, data):
        if data['password'] != data['confirm_password']:
            raise serializers.ValidationError('Passwords do not match')
        else:
            make_password(data['password'])
        return data

    def create(self, validated_data):
        validated_data.pop('confirm_password')
        is_admin = validated_data.pop('is_admin', False)
        user = User.objects.create_user(**validated_data)
        user.is_admin = is_admin
        user.save()
        return user

class UserUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['name', 'last_name', 'phone_number', 'email', 'avatar']
        read_only_fields = ['phone_number']

    def update(self, instance, validated_data):
        instance.name = validated_data.get('name', instance.name)
        instance.last_name = validated_data.get('last_name', instance.last_name)
        instance.email = validated_data.get('email', instance.email)
        instance.avatar = validated_data.get('avatar', instance.avatar)
        instance.save()
        return instance



class UserProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'phone_number', 'name', 'last_name', 'email', 'avatar']


# class NotificationSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = Notification
#         fields = ['id', 'user', 'message', 'is_read', 'timestamp']
#         read_only_fields = ['user', 'timestamp']






