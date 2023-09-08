from drf_yasg.utils import swagger_auto_schema
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from app.models import User
from app.serializers import ForgotPasswordModelSerializer
from app.utils import generate_verification_code, send_forgot_password_email


class ForgotPasswordView(APIView):

    @swagger_auto_schema(
        request_body=ForgotPasswordModelSerializer,
        responses={
            status.HTTP_200_OK: "Parolni tiklash uchun tasdiqlash kodi jo'natildi.",
            status.HTTP_404_NOT_FOUND: "Foydalanuvchi topilmadi.",
        },
    )
    def post(self, request, *args, **kwargs):
        email = request.data.get('email')
        try:
            user = User.objects.get(email=email)
            verification_code = generate_verification_code()
            user.verification_code = verification_code
            user.save()
            # Emailga tasdiqlash kodi jo'natish
            send_forgot_password_email(to_email=email,
                                       verification_code=verification_code)

            return Response({'message': 'Parolni tiklash uchun tasdiqlash kodi jo\'natildi.'},
                            status=status.HTTP_200_OK)
        except User.DoesNotExist:
            return Response({'message': 'Foydalanuvchi email manzili topilmadi.'},
                            status=status.HTTP_404_NOT_FOUND)
