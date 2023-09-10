from django.urls import path, include
from rest_framework.routers import DefaultRouter
from app.views import ProductModelViewSet

router = DefaultRouter()
router.register(prefix="product",
                viewset=ProductModelViewSet)


urlpatterns = [
    path('', include(router.urls))
]