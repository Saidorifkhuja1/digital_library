from rest_framework import serializers
from django.contrib.auth.hashers import make_password
from .models import User



class UserRegistrationSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)
    confirm_password = serializers.CharField(write_only=True)
    is_admin = serializers.BooleanField(write_only=False,default=False, required=False)

    class Meta:
        model = User
        fields = ['name', 'last_name', 'family_name', 'id_card', 'education_level',
                  'work_place', 'education_place', 'home', 'phone_number', 'email', 'password', 'confirm_password', 'is_admin', 'avatar']

    def validate(self, data):
        if data['password'] != data['confirm_password']:
            raise serializers.ValidationError('Passwords do not match')
        return data

    def create(self, validated_data):
        validated_data.pop('confirm_password')
        user = User.objects.create_user(**validated_data)
        return user





class UserUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['name', 'last_name', 'family_name', 'id_card', 'education_level',
                  'work_place', 'education_place', 'home', 'email', 'avatar']
        read_only_fields = ['phone_number']

    def update(self, instance, validated_data):
        instance.name = validated_data.get('name', instance.name)
        instance.last_name = validated_data.get('last_name', instance.last_name)
        instance.family_name = validated_data.get('family_name', instance.family_name)
        instance.id_card = validated_data.get('id_card', instance.id_card)
        instance.education_level = validated_data.get('education_level', instance.education_level)
        instance.work_place = validated_data.get('work_place', instance.work_place)
        instance.education_place = validated_data.get('education_place', instance.education_place)
        instance.home = validated_data.get('home', instance.home)
        instance.email = validated_data.get('email', instance.email)
        if 'avatar' in validated_data:
            instance.avatar = validated_data['avatar']
        elif not instance.avatar:
            instance.avatar = 'accounts/avatars/avatar.jpg'
        instance.save()
        return instance







class UserProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'phone_number', 'name', 'last_name', 'family_name', 'id_card', 'education_level',
                  'work_place', 'education_place', 'home', 'email', 'avatar']






class PasswordResetSerializer(serializers.Serializer):
    old_password = serializers.CharField(write_only=True)
    new_password = serializers.CharField(write_only=True)

    class Meta:
        fields = ['old_password', 'new_password']

    def validate(self, data):
        if data['old_password'] == data['new_password']:
            raise serializers.ValidationError("The new password cannot be the same as the old password.")
        return data


