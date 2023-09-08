from django.contrib.auth import authenticate
from django.contrib.auth.hashers import make_password
from django.core.validators import EmailValidator
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


class LoginSerializer(serializers.ModelSerializer):
    email = serializers.EmailField(validators=[EmailValidator()])  # Email manzili tekshiriladi
    password = serializers.CharField(write_only=True)

    class Meta:
        model = User
        fields = ['email', 'password']

    # def validate(self, data):
    #     email = data.get("email")
    #     password = data.get("password")
    #
    #     if email and password:
    #         user = authenticate(username=email, password=password)
    #         if not user:
    #             raise serializers.ValidationError("Noto'g'ri kirish ma'lumotlari")
    #     else:
    #         raise serializers.ValidationError("Foydalanuvchi nomi va parol majburiy")
    #
    #     data['user'] = user
    #     return data


class ForgotPasswordModelSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['email', ]


class ForgotChangeUserModelSerializer(serializers.ModelSerializer):
    new_password = serializers.CharField(max_length=155)
    confirm_password = serializers.CharField(max_length=155)

    class Meta:
        model = User
        fields = ['email', 'new_password', 'confirm_password', 'verification_code']
        extra_kwargs = {'new_password': {'write_only': True},
                        'confirm_password': {'write_only': True},
                        'verification_code': {'write_only': True}}


class ChangeUserModelSerializer(serializers.ModelSerializer):
    confirm_password = serializers.CharField(max_length=55)

    class Meta:
        model = User
        fields = ['password', 'confirm_password']
        extra_kwargs = {'password': {'write_only': True},
                        'confirm_password': {'write_only': True}}
