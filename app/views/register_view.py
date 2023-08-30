from datetime import timedelta
from django.utils import timezone
from rest_framework.generics import CreateAPIView
from app.serializers import RegisterUserSerializer
from app.utils import generate_verification_code, send_verification_email


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