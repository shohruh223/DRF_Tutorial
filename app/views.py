from rest_framework.generics import CreateAPIView
from datetime import timedelta
from django.utils import timezone
from app.serializer import RegisterUserSerializer, VerifyPhoneSerializer
from app.utils import generate_verification_code, send_sms


class RegisterView(CreateAPIView):
    serializer_class = RegisterUserSerializer

    def perform_create(self, serializer):
        phone_number = serializer.validated_data['phone_number']
        verification_code = generate_verification_code()
        expiration_time = timezone.now() + timedelta(minutes=1)
        serializer.save(verification_code=verification_code,
                        activation_key_expires=expiration_time)
        send_sms(body=f"Tasdiqlash kodi: {verification_code}",
                 number=phone_number)

    def create(self, request, *args, **kwargs):
        response = super().create(request, *args, **kwargs)
        response.data['message'] = "Tasdiqlash kodi yuborildi. Iltimos sms orqali tasdiqlab yuboring"
        return response


class VerifyPhoneView(CreateAPIView):
    serializer_class = VerifyPhoneSerializer

    def post(self, request, *args, **kwargs):
        phone_number = request.data.get('phone_number')
        verification_code = request.data.get('verification_code')

