from django.urls import path, include
from rest_framework.routers import DefaultRouter

from app.views import ProductModelViewSet

router = DefaultRouter()
router.register(prefix="product",
                viewset=ProductModelViewSet)


urlpatterns = [
    # path('create/', ProductCreateAPIView.as_view(), name='create'),
    # path('list/', ProductListAPIView.as_view(), name='list'),
    # path('product/', ProductListCreateAPIView.as_view(), name='product'),
    # path('retrieve/<int:pk>', ProductRetrieveAPIView.as_view(), name='retrieve'),
    # path('destroy/<int:pk>', ProductDestroyAPIView.as_view(), name='destroy'),
    # path('update/<int:pk>', ProductUpdateAPIView.as_view(), name='update'),
    # path('product/<int:pk>', ProductRetrieveUpdateDestroyAPIView.as_view(), name='product_id'),

    path('', include(router.urls))
]