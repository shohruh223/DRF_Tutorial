from datetime import datetime, timedelta

from django.contrib.auth.hashers import make_password
from django.utils import timezone
from rest_framework.decorators import action
from rest_framework.generics import CreateAPIView, UpdateAPIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework import status
from .models import User
from .serializers import RegisterUserSerializer, VerifyUserSerializer, ForgotPasswordModelSerializer, \
    ChangeUserModelSerializer
from .utils import generate_verification_code, send_verification_email, send_forgot_password_email


class RegisterAndVerifyEmailView(CreateAPIView):
    serializer_class = RegisterUserSerializer

    def perform_create(self, serializer):
        verification_code = generate_verification_code()
        expiration_time = timezone.now() + timedelta(minutes=1)
        serializer.save(verification_code=verification_code,
                        activation_key_expires=expiration_time)
        # Emailni tasdiqlash kodini yuborish
        send_verification_email(to_email=serializer.data['email'],
                                verification_code=verification_code)

    def create(self, request, *args, **kwargs):
        response = super().create(request, *args, **kwargs)
        response.data['message'] = "Tasdiqlash kodi yuborildi. Iltimos emailga o'tib tasdiqlab yuboring"
        return response


class VerifyEmailView(CreateAPIView):
    permission_classes = [IsAuthenticated,]
    serializer_class = VerifyUserSerializer

    def post(self, request, *args, **kwargs):
        email = request.data.get('email')
        verification_code = request.data.get('verification_code')
        try:
            instance = User.objects.get(email=email,
                                    verification_code=verification_code)
            if not instance.is_active and instance.activation_key_expires > timezone.now():
                instance.is_active = True
                instance.save()
                return Response({'message': 'Email tasdiqlandi.'},
                                status=status.HTTP_200_OK)
            elif instance.is_active:
                return Response({'message': 'Email allaqachon tasdiqlangan.'},
                                status=status.HTTP_400_BAD_REQUEST)
            else:
                return Response({'message': 'Tasdiqlash kod muddati tugagan yoki noto\'g\'ri tasdiqlash kod.'},
                                status=status.HTTP_400_BAD_REQUEST)
        except User.DoesNotExist:
            return Response({'message': 'Noto\'g\'ri tasdiqlash kod yoki email.'},
                            status=status.HTTP_400_BAD_REQUEST)


class ForgotPasswordView(CreateAPIView):
    permission_classes = [IsAuthenticated,]
    serializer_class = ForgotPasswordModelSerializer

    def create(self, request, *args, **kwargs):
        email = request.data.get('email')
        try:
            instance = User.objects.get(email=email)

            # Yangi tasdiqlash kodi yaratish va saqlash
            verification_code = generate_verification_code()
            instance.verification_code = verification_code
            instance.save()

            # Emailga tasdiqlash kodi jo'natish
            send_forgot_password_email(to_email=email,
                                       verification_code=verification_code)
            return Response({'message': 'Parolni tiklash uchun tasdiqlash kodi jo\'natildi.'},
                            status=status.HTTP_200_OK)
        except User.DoesNotExist:
            return Response({'message': 'Foydalanuvchi email manzili topilmadi.'},
                            status=status.HTTP_404_NOT_FOUND)


class ChangePasswordView(UpdateAPIView):
    permission_classes = [IsAuthenticated,]
    queryset = User.objects.all()
    serializer_class = ChangeUserModelSerializer
    lookup_field = 'pk'

    def update(self, request, *args, **kwargs):
        instance = self.get_object()

        verification_code = request.data.get('verification_code')
        password = request.data.get('password')

        # Tasdiqlash kodi tekshiriladi
        if not instance.verification_code or instance.verification_code != verification_code:
            return Response({'error': 'Tasdiqlash kodi noto\'g\'ri'}, status=status.HTTP_400_BAD_REQUEST)

        # Yangi parolni saqlash
        instance.password = make_password(password)
        # instance.verification_code = None  # Tasdiqlash kodini tozalash
        instance.save()

        return Response({'message': 'Parol muvaffaqiyatli o\'zgartirildi'}, status=status.HTTP_200_OK)