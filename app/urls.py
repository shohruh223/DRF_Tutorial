from django.urls import path, include
from rest_framework.routers import DefaultRouter

from app.views import ProductView

router = DefaultRouter()
router.register(prefix='product',
                viewset=ProductView)


urlpatterns = [
    path('', include(router.urls))
]