from django.urls import path

from app.views import RegisterApiView, LoginAPIView

urlpatterns = [
    path('register/', RegisterApiView.as_view(), name='register'),
    path('login', LoginAPIView.as_view(), name='login'),
]