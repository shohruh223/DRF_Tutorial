from django.utils import timezone
from drf_yasg.utils import swagger_auto_schema
from rest_framework import status
from rest_framework.generics import CreateAPIView
from rest_framework.response import Response
from rest_framework.views import APIView

from app.models import User
from app.serializers import VerifyUserSerializer, ForgotChangeUserModelSerializer


class VerifyRegisterEmailView(CreateAPIView):
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
            elif instance.activation_key_expires < timezone.now() or instance.verification_code != verification_code:
                instance.delete()
                return Response({'message': 'Tasdiqlash kod muddati tugagan yoki noto\'g\'ri tasdiqlash kod.'},
                                status=status.HTTP_400_BAD_REQUEST)
        except User.DoesNotExist:
            return Response({'message': 'Noto\'g\'ri tasdiqlash kod yoki email.'},
                            status=status.HTTP_400_BAD_REQUEST)


class VerifyForgotEmailView(APIView):
    serializer_class = ForgotChangeUserModelSerializer

    @swagger_auto_schema(
        request_body=ForgotChangeUserModelSerializer,
        responses={
            status.HTTP_200_OK: "Email tasdiqlandi.",
            status.HTTP_400_BAD_REQUEST: "Tasdiqlash kod muddati tugagan yoki noto'g'ri tasdiqlash kod.",
            status.HTTP_400_BAD_REQUEST: "Noto'g'ri tasdiqlash kod yoki email.",
        },
    )
    def post(self, request, *args, **kwargs):
        email = request.data.get('email')
        new_password = request.data.get("new_password")
        confirm_password = request.data.get("confirm_password")
        verification_code = request.data.get('verification_code')
        try:
            user = User.objects.get(email=email,
                                    verification_code=verification_code)

            if user.is_active and user.activation_key_expires > timezone.now():
                # Yangi parolni va tasdiqlashni tekshirish
                if new_password != confirm_password:
                    return Response({'message': 'Parol va tasdiqlash mos kelmadi.'},
                                    status=status.HTTP_400_BAD_REQUEST)
                else:
                    user.set_password(new_password)
                    user.is_active = True
                    user.save()
                    return Response({'message': 'Email tasdiqlandi.'}, status=status.HTTP_200_OK)
            elif user.activation_key_expires < timezone.now() or user.verification_code != verification_code:
                return Response({'message': 'Tasdiqlash kod muddati tugagan yoki noto\'g\'ri tasdiqlash kod.'},
                                status=status.HTTP_400_BAD_REQUEST)
        except User.DoesNotExist:
            return Response({'message': 'Noto\'g\'ri tasdiqlash kod yoki email.'}, status=status.HTTP_400_BAD_REQUEST)
