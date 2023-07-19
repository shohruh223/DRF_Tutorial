from django.urls import path

from app.views import ProductView

urlpatterns = [
    path('product/', ProductView.as_view(), name='product-list'),
    path('product/<int:product_id>', ProductView.as_view(), name='product-detail'),
]