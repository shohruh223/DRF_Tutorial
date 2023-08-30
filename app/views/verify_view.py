from django.utils import timezone
from rest_framework import status
from rest_framework.generics import CreateAPIView
from rest_framework.response import Response
from app.models import User
from app.serializers import VerifyUserSerializer


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


class VerifyForgotEmailView(CreateAPIView):
    serializer_class = VerifyUserSerializer

    def post(self, request, *args, **kwargs):
        email = request.data.get('email')
        verification_code = request.data.get('verification_code')
        try:
            instance = User.objects.get(email=email,
                                    verification_code=verification_code)
            if instance.is_active and instance.activation_key_expires > timezone.now():
                instance.is_active = True
                instance.save()
                return Response({'message': 'Email tasdiqlandi.'},
                                status=status.HTTP_200_OK)
            elif instance.activation_key_expires < timezone.now() or instance.verification_code != verification_code:
                return Response({'message': 'Tasdiqlash kod muddati tugagan yoki noto\'g\'ri tasdiqlash kod.'},
                                status=status.HTTP_400_BAD_REQUEST)
        except User.DoesNotExist:
            return Response({'message': 'Noto\'g\'ri tasdiqlash kod yoki email.'},
                            status=status.HTTP_400_BAD_REQUEST)