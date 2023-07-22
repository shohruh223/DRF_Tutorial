from django.urls import path, include
from rest_framework.routers import DefaultRouter
from app.views import RegisterAndVerifyEmailView, VerifyEmailView, ForgotPasswordView, ChangePasswordView

# router = DefaultRouter()
# router.register(prefix="product",
#                 viewset=ProductModelViewSet)


urlpatterns = [
    # path('', include(router.urls)),
    path('register/', RegisterAndVerifyEmailView.as_view(), name='register'),
    path('verify-email/', VerifyEmailView.as_view(), name='verify_email'),
    path('forgot-password/', ForgotPasswordView.as_view(), name='forgot-password'),
    path('change-password/<int:pk>/', ChangePasswordView.as_view(), name='change_password'),
]
