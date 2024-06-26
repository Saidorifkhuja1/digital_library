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
        # instance.avatar = validated_data.get('avatar', instance.avatar)
        if 'avatar' in validated_data:
            instance.avatar = validated_data['avatar']
        elif not instance.avatar:
            instance.avatar = 'accounts/avatars/avatar.jpg'
        instance.save()
        return instance







class UserProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'phone_number', 'name', 'last_name', 'email', 'avatar']






class PasswordResetSerializer(serializers.Serializer):
    old_password = serializers.CharField(write_only=True)
    new_password = serializers.CharField(write_only=True)

    class Meta:
        fields = ['old_password', 'new_password']

    def validate(self, data):
        if data['old_password'] == data['new_password']:
            raise serializers.ValidationError("The new password cannot be the same as the old password.")
        return data


