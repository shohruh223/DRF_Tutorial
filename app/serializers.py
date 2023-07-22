from django.contrib.auth.hashers import make_password
from rest_framework import serializers
from app.models import User


class RegisterUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['email', 'password']
        extra_kwargs = {'password': {'write_only': True}}

    def create(self, validated_data):
        # Parolni xashlash
        password = validated_data.pop('password')
        hashed_password = make_password(password)

        # Model obyektini yaratib, xashlangan parolni saqlaymiz
        user = User.objects.create(**validated_data, password=hashed_password)
        return user


class VerifyUserSerializer(serializers.ModelSerializer):

    class Meta:
        model = User
        fields = ['email', 'verification_code']
        extra_kwargs = {'password': {'write_only': True}}


class ForgotPasswordModelSerializer(serializers.ModelSerializer):

    class Meta:
        model = User
        fields = ['email',]


class ChangeUserModelSerializer(serializers.ModelSerializer):

    class Meta:
        model = User
        fields = ['password', 'verification_code']
        extra_kwargs = {'password': {'write_only': True},
                        'verification_code': {'write_only': True}}






