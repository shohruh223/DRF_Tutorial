from django.urls import path
from app.views.change_password_view import ChangePasswordView
from app.views.forgot_password_view import ForgotPasswordView
from app.views.login_view import LoginAPIView
from app.views.register_view import RegisterAndVerifyEmailView
from app.views.verify_view import VerifyRegisterEmailView, VerifyForgotEmailView

# router = DefaultRouter()
# router.register(prefix="product",
#                 viewset=ProductModelViewSet)


urlpatterns = [
    # path('', include(router.urls)),
    path('register/', RegisterAndVerifyEmailView.as_view(), name='register'),
    path('login/', LoginAPIView.as_view(), name='login'),
    path('verify-register-email/', VerifyRegisterEmailView.as_view(), name='verify-register-email'),
    path('verify-forgot-email/', VerifyForgotEmailView.as_view(), name='verify-register-email'),
    path('forgot-password/', ForgotPasswordView.as_view(), name='forgot-password'),
    path('change-password/', ChangePasswordView.as_view(), name='change_password'),
    # path('forgot-change-password/', ForgotChangePasswordView.as_view(), name='forgot-change_password'),
]
