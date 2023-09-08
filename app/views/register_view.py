from datetime import timedelta
from django.utils import timezone
from drf_yasg.utils import swagger_auto_schema
from rest_framework import status
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework.views import APIView
from app.serializers import RegisterUserSerializer
from app.utils import generate_verification_code, send_verification_email


class RegisterAndVerifyEmailView(APIView):
    permission_classes = [AllowAny]
    serializer_class = RegisterUserSerializer

    @swagger_auto_schema(
        request_body=RegisterUserSerializer,
        responses={
            status.HTTP_201_CREATED: "User successfully registered",
            status.HTTP_400_BAD_REQUEST: "Invalid Credentials"
        }
    )
    def post(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid():
            # Tasdiqlash kodi va amal qilish muddati hosil qilinadi
            verification_code = generate_verification_code()
            expiration_time = timezone.now() + timedelta(minutes=1)
            serializer.save(verification_code=verification_code, activation_key_expires=expiration_time)

            # Emailni tasdiqlash kodini yuborish
            send_verification_email(to_email=serializer.validated_data['email'], verification_code=verification_code)
            response_data = {"message": "Tasdiqlash kodi yuborildi. Iltimos emailga o'tib tasdiqlab yuboring"}
            return Response(response_data, status=status.HTTP_201_CREATED)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
