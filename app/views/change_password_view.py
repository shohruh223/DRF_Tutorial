from django.contrib.auth.hashers import make_password
from drf_yasg.utils import swagger_auto_schema
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from app.serializers import ForgotChangeUserModelSerializer, ChangeUserModelSerializer


# class ForgotChangePasswordView(APIView):
#
#     @swagger_auto_schema(
#         request_body=ForgotChangeUserModelSerializer,  # Use your serializer here
#         responses={
#             200: 'Password successfully changed',
#             400: 'Bad Request',
#             401: 'Unauthorized',
#         }
#     )
#     def put(self, request, *args, **kwargs):
#         serializer = ForgotChangeUserModelSerializer(data=request.data)
#         if serializer.is_valid():
#             verification_code = serializer.validated_data.get('verification_code')
#             password = serializer.validated_data.get('password')
#             instance = self.request.user
#
#             # Tasdiqlash kodi tekshiriladi
#             if not instance.verification_code or instance.verification_code != verification_code:
#                 return Response({'error': 'Tasdiqlash kodi noto\'g\'ri'}, status=status.HTTP_400_BAD_REQUEST)
#
#             # Yangi parolni saqlash
#             instance.password = make_password(password)
#             instance.save()
#
#             return Response({'message': 'Parol muvaffaqiyatli o\'zgartirildi'}, status=status.HTTP_200_OK)
#         else:
#             return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class ChangePasswordView(APIView):
    permission_classes = [IsAuthenticated, ]

    @swagger_auto_schema(
        request_body=ChangeUserModelSerializer,  # Use your serializer here
        responses={
            200: 'Password successfully changed',
            400: 'Bad Request',
            401: 'Unauthorized',
        }
    )
    def post(self, request, *args, **kwargs):
        serializer = ChangeUserModelSerializer(data=request.data)
        if serializer.is_valid():
            password = serializer.validated_data['password']

            # Yangi parolni saqlash
            user = request.user
            user.set_password(password)
            user.save()

            return Response({'message': 'Parol muvaffaqiyatli o\'zgartirildi'}, status=status.HTTP_200_OK)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)