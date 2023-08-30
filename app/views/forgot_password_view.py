from rest_framework import status
from rest_framework.generics import CreateAPIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from app.models import User
from app.serializers import ForgotPasswordModelSerializer
from app.utils import generate_verification_code, send_forgot_password_email


class ForgotPasswordView(CreateAPIView):
    # permission_classes = [IsAuthenticated,]
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